import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import * as s3 from 'aws-cdk-lib/aws-s3';
import * as ecr from 'aws-cdk-lib/aws-ecr';
import * as iam from 'aws-cdk-lib/aws-iam';

export interface MlopsStackProps extends cdk.StackProps {
  environment: 'dev' | 'staging' | 'prod';
}

export class MlopsStack extends cdk.Stack {
  public readonly dataBucket: s3.Bucket;
  public readonly modelBucket: s3.Bucket;
  public readonly trainingRepo: ecr.Repository;

  constructor(scope: Construct, id: string, props: MlopsStackProps) {
    super(scope, id, props);

    const isprod = props.environment === 'prod';

    // S3: data and model artefacts
    this.dataBucket = new s3.Bucket(this, 'DataBucket', {
      bucketName: `claude-central-mlops-data-${props.environment}-${this.account}`,
      versioned: true,
      encryption: s3.BucketEncryption.S3_MANAGED,
      removalPolicy: isprod ? cdk.RemovalPolicy.RETAIN : cdk.RemovalPolicy.DESTROY,
      autoDeleteObjects: !isprod,
    });

    this.modelBucket = new s3.Bucket(this, 'ModelBucket', {
      bucketName: `claude-central-mlops-models-${props.environment}-${this.account}`,
      versioned: true,
      encryption: s3.BucketEncryption.S3_MANAGED,
      removalPolicy: cdk.RemovalPolicy.RETAIN, // Always retain model artefacts
    });

    // ECR: custom training container images
    this.trainingRepo = new ecr.Repository(this, 'TrainingRepo', {
      repositoryName: `claude-central/training-${props.environment}`,
      removalPolicy: isprod ? cdk.RemovalPolicy.RETAIN : cdk.RemovalPolicy.DESTROY,
    });

    // SageMaker execution role
    const sagemakerRole = new iam.Role(this, 'SageMakerRole', {
      roleName: `claude-central-sagemaker-${props.environment}`,
      assumedBy: new iam.ServicePrincipal('sagemaker.amazonaws.com'),
    });

    sagemakerRole.addManagedPolicy(
      iam.ManagedPolicy.fromAwsManagedPolicyName('AmazonSageMakerFullAccess')
    );
    this.dataBucket.grantReadWrite(sagemakerRole);
    this.modelBucket.grantReadWrite(sagemakerRole);
    this.trainingRepo.grantPull(sagemakerRole);

    new cdk.CfnOutput(this, 'DataBucketName', { value: this.dataBucket.bucketName });
    new cdk.CfnOutput(this, 'ModelBucketName', { value: this.modelBucket.bucketName });
    new cdk.CfnOutput(this, 'SageMakerRoleArn', { value: sagemakerRole.roleArn });

    cdk.Tags.of(this).add('Project', 'claude-central');
    cdk.Tags.of(this).add('Environment', props.environment);
    cdk.Tags.of(this).add('Owner', 'platform-team');
    cdk.Tags.of(this).add('CostCentre', 'ai-platform');
  }
}

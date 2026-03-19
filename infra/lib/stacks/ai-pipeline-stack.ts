import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import * as lambda from 'aws-cdk-lib/aws-lambda';
import * as sqs from 'aws-cdk-lib/aws-sqs';
import * as s3 from 'aws-cdk-lib/aws-s3';
import * as lambdaEventSources from 'aws-cdk-lib/aws-lambda-event-sources';

export interface AiPipelineStackProps extends cdk.StackProps {
  environment: 'dev' | 'staging' | 'prod';
}

export class AiPipelineStack extends cdk.Stack {
  public readonly inputQueue: sqs.Queue;
  public readonly outputBucket: s3.Bucket;

  constructor(scope: Construct, id: string, props: AiPipelineStackProps) {
    super(scope, id, props);

    // Dead letter queue for failed pipeline runs
    const dlq = new sqs.Queue(this, 'PipelineDlq', {
      queueName: `claude-central-pipeline-dlq-${props.environment}`,
      retentionPeriod: cdk.Duration.days(14),
    });

    // Input queue — messages trigger pipeline execution
    this.inputQueue = new sqs.Queue(this, 'PipelineInputQueue', {
      queueName: `claude-central-pipeline-input-${props.environment}`,
      visibilityTimeout: cdk.Duration.seconds(300),
      deadLetterQueue: { queue: dlq, maxReceiveCount: 3 },
    });

    // Output bucket for pipeline results
    this.outputBucket = new s3.Bucket(this, 'PipelineOutputBucket', {
      bucketName: `claude-central-pipeline-output-${props.environment}-${this.account}`,
      versioned: true,
      encryption: s3.BucketEncryption.S3_MANAGED,
      removalPolicy: props.environment === 'prod'
        ? cdk.RemovalPolicy.RETAIN
        : cdk.RemovalPolicy.DESTROY,
      autoDeleteObjects: props.environment !== 'prod',
    });

    // Pipeline Lambda (placeholder — replace with real handler)
    const pipelineFn = new lambda.Function(this, 'PipelineHandler', {
      functionName: `claude-central-pipeline-${props.environment}`,
      runtime: lambda.Runtime.PYTHON_3_12,
      handler: 'handler.main',
      code: lambda.Code.fromInline(`
def main(event, context):
    # TODO: implement pipeline trigger
    return {"statusCode": 200}
`),
      timeout: cdk.Duration.seconds(300),
      memorySize: 512,
      environment: {
        OUTPUT_BUCKET: this.outputBucket.bucketName,
        ENVIRONMENT: props.environment,
      },
    });

    pipelineFn.addEventSource(
      new lambdaEventSources.SqsEventSource(this.inputQueue, { batchSize: 1 })
    );
    this.outputBucket.grantWrite(pipelineFn);

    new cdk.CfnOutput(this, 'InputQueueUrl', { value: this.inputQueue.queueUrl });
    new cdk.CfnOutput(this, 'OutputBucketName', { value: this.outputBucket.bucketName });

    cdk.Tags.of(this).add('Project', 'claude-central');
    cdk.Tags.of(this).add('Environment', props.environment);
    cdk.Tags.of(this).add('Owner', 'platform-team');
    cdk.Tags.of(this).add('CostCentre', 'ai-platform');
  }
}

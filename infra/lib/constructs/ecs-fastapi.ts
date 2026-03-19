import * as cdk from 'aws-cdk-lib';
import * as ecs from 'aws-cdk-lib/aws-ecs';
import * as ecsPatterns from 'aws-cdk-lib/aws-ecs-patterns';
import * as ecr from 'aws-cdk-lib/aws-ecr';
import * as logs from 'aws-cdk-lib/aws-logs';
import { Construct } from 'constructs';

export interface EcsFastApiProps {
  /** ECR repository containing the FastAPI image */
  repository: ecr.IRepository;
  /** Image tag to deploy (default: 'latest') */
  imageTag?: string;
  /** Container port (default: 8000) */
  containerPort?: number;
  /** CPU units (default: 512) */
  cpu?: number;
  /** Memory in MiB (default: 1024) */
  memoryMiB?: number;
  /** Number of tasks (default: 1) */
  desiredCount?: number;
  /** Environment variables passed to the container */
  environment?: Record<string, string>;
}

/**
 * FastAPI service on ECS Fargate with ALB.
 * Opinionated defaults: health check at /health, structured logging to CloudWatch.
 */
export class EcsFastApi extends Construct {
  public readonly service: ecsPatterns.ApplicationLoadBalancedFargateService;

  constructor(scope: Construct, id: string, props: EcsFastApiProps) {
    super(scope, id);

    const logGroup = new logs.LogGroup(this, 'Logs', {
      retention: logs.RetentionDays.ONE_MONTH,
      removalPolicy: cdk.RemovalPolicy.DESTROY,
    });

    this.service = new ecsPatterns.ApplicationLoadBalancedFargateService(this, 'Service', {
      taskImageOptions: {
        image: ecs.ContainerImage.fromEcrRepository(
          props.repository,
          props.imageTag ?? 'latest'
        ),
        containerPort: props.containerPort ?? 8000,
        environment: {
          LOG_LEVEL: 'INFO',
          ...props.environment,
        },
        logDriver: ecs.LogDrivers.awsLogs({
          logGroup,
          streamPrefix: id,
        }),
      },
      cpu: props.cpu ?? 512,
      memoryLimitMiB: props.memoryMiB ?? 1024,
      desiredCount: props.desiredCount ?? 1,
      healthCheckGracePeriod: cdk.Duration.seconds(60),
    });

    // Health check at /health
    this.service.targetGroup.configureHealthCheck({
      path: '/health',
      healthyHttpCodes: '200',
      interval: cdk.Duration.seconds(30),
      timeout: cdk.Duration.seconds(10),
      healthyThresholdCount: 2,
      unhealthyThresholdCount: 3,
    });
  }
}

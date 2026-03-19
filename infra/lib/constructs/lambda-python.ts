import * as cdk from 'aws-cdk-lib';
import * as lambda from 'aws-cdk-lib/aws-lambda';
import * as logs from 'aws-cdk-lib/aws-logs';
import { Construct } from 'constructs';

export interface PythonLambdaProps {
  /** Handler in module.function format */
  handler: string;
  /** Path to the Lambda code directory */
  codePath: string;
  /** Function description */
  description?: string;
  /** Memory in MB (default: 256) */
  memoryMiB?: number;
  /** Timeout in seconds (default: 30) */
  timeoutSeconds?: number;
  /** Environment variables */
  environment?: Record<string, string>;
}

/**
 * Opinionated Python 3.12 Lambda construct.
 * Enforces: structured logging, X-Ray tracing, CloudWatch log retention.
 */
export class PythonLambda extends Construct {
  public readonly fn: lambda.Function;

  constructor(scope: Construct, id: string, props: PythonLambdaProps) {
    super(scope, id);

    this.fn = new lambda.Function(this, 'Fn', {
      runtime: lambda.Runtime.PYTHON_3_12,
      handler: props.handler,
      code: lambda.Code.fromAsset(props.codePath),
      description: props.description,
      memorySize: props.memoryMiB ?? 256,
      timeout: cdk.Duration.seconds(props.timeoutSeconds ?? 30),
      tracing: lambda.Tracing.ACTIVE,
      environment: {
        LOG_LEVEL: 'INFO',
        POWERTOOLS_SERVICE_NAME: id,
        ...props.environment,
      },
      logRetention: logs.RetentionDays.ONE_MONTH,
    });
  }
}

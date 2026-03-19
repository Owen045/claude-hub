import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import * as ecs from 'aws-cdk-lib/aws-ecs';
import * as ecsPatterns from 'aws-cdk-lib/aws-ecs-patterns';
import * as ecr from 'aws-cdk-lib/aws-ecr';

export interface McpServerStackProps extends cdk.StackProps {
  environment: 'dev' | 'staging' | 'prod';
}

export class McpServerStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props: McpServerStackProps) {
    super(scope, id, props);

    const repository = new ecr.Repository(this, 'McpServerRepo', {
      repositoryName: `claude-central/mcp-knowledge-base-${props.environment}`,
      removalPolicy: props.environment === 'prod'
        ? cdk.RemovalPolicy.RETAIN
        : cdk.RemovalPolicy.DESTROY,
    });

    const service = new ecsPatterns.ApplicationLoadBalancedFargateService(
      this, 'McpServerService',
      {
        taskImageOptions: {
          image: ecs.ContainerImage.fromEcrRepository(repository, 'latest'),
          containerPort: 8080,
          environment: {
            TRANSPORT: 'sse',
            PORT: '8080',
          },
          secrets: {
            // ANTHROPIC_API_KEY: ecs.Secret.fromSecretsManager(apiKeySecret),
          },
        },
        cpu: 512,
        memoryLimitMiB: 1024,
        desiredCount: props.environment === 'prod' ? 2 : 1,
      }
    );

    new cdk.CfnOutput(this, 'ServiceUrl', {
      value: service.loadBalancer.loadBalancerDnsName,
      description: 'MCP Server load balancer URL',
    });

    cdk.Tags.of(this).add('Project', 'claude-central');
    cdk.Tags.of(this).add('Environment', props.environment);
    cdk.Tags.of(this).add('Owner', 'platform-team');
    cdk.Tags.of(this).add('CostCentre', 'ai-platform');
  }
}

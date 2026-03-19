# Infra

AWS CDK infrastructure (TypeScript) for the claude-central monorepo.

## Stacks

| Stack | Description |
|---|---|
| `AiPipelineStack` | Core AI pipeline infrastructure (queues, lambdas) |
| `McpServerStack` | Containerised MCP server on ECS Fargate |
| `MlopsStack` | SageMaker + S3 + ECR for MLOps |

## Prerequisites

```bash
npm install -g pnpm
pnpm install
npx cdk bootstrap aws://ACCOUNT_ID/eu-west-2
```

## Commands

```bash
pnpm cdk synth          # Synthesise CloudFormation templates
pnpm cdk diff           # Show changes vs deployed stack
pnpm cdk deploy --all   # Deploy all stacks
```

## Conventions

See `context/aws-conventions.md` for tagging, IAM, and naming rules.
All stacks require `environment: 'dev' | 'staging' | 'prod'` in props.

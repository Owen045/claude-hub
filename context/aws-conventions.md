# AWS Conventions

## Tagging Strategy
Every resource must have these tags (enforced via CDK aspects):

| Tag | Values | Example |
|---|---|---|
| `Project` | repo/project name | `claude-central` |
| `Environment` | `dev`, `staging`, `prod` | `dev` |
| `Owner` | team or individual | `platform-team` |
| `CostCentre` | billing code | `ai-platform` |

```typescript
// Apply to every stack
cdk.Tags.of(this).add('Project', 'claude-central');
cdk.Tags.of(this).add('Environment', props.environment);
cdk.Tags.of(this).add('Owner', 'platform-team');
cdk.Tags.of(this).add('CostCentre', 'ai-platform');
```

## IAM Principles
- **Least privilege**: grant only actions required, on specific resources.
- No `"Resource": "*"` in prod IAM policies.
- No inline policies — use managed policies attached to roles.
- Use `aws-cdk-lib/aws-iam` constructs, never raw CloudFormation JSON.
- Rotate access keys every 90 days. Prefer IRSA / instance profiles over long-lived keys.

## Naming Conventions
- Resources: `{project}-{component}-{environment}` (e.g., `claude-central-mcp-server-prod`)
- S3 buckets: globally unique — append account ID suffix.
- SSM parameters: `/{project}/{environment}/{key}` (e.g., `/claude-central/prod/anthropic-api-key`)
- Secrets Manager: `{project}/{environment}/{secret-name}`

## Service Preferences
| Use Case | Preferred Service | Avoid |
|---|---|---|
| Containerised apps | ECS Fargate | EC2 |
| Short-running functions | Lambda | EC2 |
| ML training/inference | SageMaker | EC2 + manual |
| Object storage | S3 | EFS for static |
| Secrets | Secrets Manager | SSM SecureString (for secrets) |
| Queues | SQS | Self-managed Redis queues |

## CDK Best Practices
- One stack per logical component (don't put everything in one stack).
- Use `cdk.Environment` with explicit `account` and `region` — no implicit env.
- `cdk diff` before every `cdk deploy` in CI.
- Stateful resources (RDS, S3, ECR) get `RemovalPolicy.RETAIN` in prod.
- Outputs exported with `CfnOutput` for cross-stack references.

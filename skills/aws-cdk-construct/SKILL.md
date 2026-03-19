---
name: aws-cdk-construct
description: >
  Use when creating or modifying AWS CDK stacks, constructs, or infra code.
  Triggers on: CDK, AWS infrastructure, CloudFormation, stack, construct, Fargate,
  Lambda, SageMaker, ECS, S3, IAM, deploy infra.
triggers:
  - CDK
  - AWS infrastructure
  - CloudFormation
  - new stack
  - new construct
  - Fargate
  - Lambda
  - SageMaker
  - "*.ts in infra/"
---

# AWS CDK Construct Skill

## When to Use This Skill
When writing or modifying any CDK TypeScript code in `infra/`.

## Pre-Flight Checklist
- [ ] Read `context/aws-conventions.md`
- [ ] Identify the stack this belongs to (or create a new one)
- [ ] Confirm environment-specific behaviour needed (dev vs prod)

## Step-by-Step Process
1. Define props interface with `environment: 'dev' | 'staging' | 'prod'`
2. Implement the stack/construct using typed CDK constructs
3. Apply resource tags at the stack level
4. Set environment-appropriate removal policies
5. Export outputs with `CfnOutput`
6. Run `cdk synth` to validate — fix all warnings

## Patterns and Examples

### Stack template
```typescript
import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { z } from 'zod';

const StackPropsSchema = z.object({
  environment: z.enum(['dev', 'staging', 'prod']),
});

export interface MyStackProps extends cdk.StackProps {
  environment: 'dev' | 'staging' | 'prod';
}

export class MyStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props: MyStackProps) {
    super(scope, id, props);

    // ... resources ...

    cdk.Tags.of(this).add('Project', 'claude-central');
    cdk.Tags.of(this).add('Environment', props.environment);
    cdk.Tags.of(this).add('Owner', 'platform-team');
    cdk.Tags.of(this).add('CostCentre', 'ai-platform');
  }
}
```

### Removal policy pattern
```typescript
const removalPolicy = props.environment === 'prod'
  ? cdk.RemovalPolicy.RETAIN
  : cdk.RemovalPolicy.DESTROY;
```

## Common Mistakes to Avoid
- Never use `RemovalPolicy.DESTROY` for prod stateful resources.
- Never use `"Resource": "*"` in IAM policies.
- Don't skip tagging — it's how billing is attributed.
- Don't use `cdk.Fn.importValue` across stacks unless necessary — use construct refs.

## Quality Gates
- [ ] `cdk synth` completes without errors or warnings
- [ ] All resources tagged
- [ ] Prod resources use RETAIN removal policy
- [ ] IAM policies grant only required actions on specific resources
- [ ] `CfnOutput` for any values needed by other stacks or users

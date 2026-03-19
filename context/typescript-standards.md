# TypeScript Standards

## Compiler Config
- `"strict": true` in all tsconfig.json files — no exceptions.
- `"noUncheckedIndexedAccess": true` to catch array/object access bugs.
- `"exactOptionalPropertyTypes": true` to distinguish missing vs undefined.
- Target ES2022+. Use Node20+ for CDK and server-side code.

## Runtime Validation
- Use **Zod** for all external data: API responses, environment variables, CDK props.
- Never `as SomeType` a value that came from outside your module.
- Parse env vars at startup with a Zod schema — fail fast if misconfigured.

```typescript
import { z } from 'zod';

const EnvSchema = z.object({
  ANTHROPIC_API_KEY: z.string().startsWith('sk-ant-'),
  AWS_REGION: z.string().default('eu-west-2'),
});

export const env = EnvSchema.parse(process.env);
```

## Code Style
- ESLint + Prettier enforced. Config inherited from repo root.
- Prefer `interface` over `type` for object shapes that may be extended.
- Prefer `type` for unions, intersections, and mapped types.
- No `var`. Prefer `const` over `let`.
- Async/await over `.then()` chains.

## Testing
- **Vitest** for unit tests. Co-locate with source: `foo.test.ts` next to `foo.ts`.
- Mock external services at the module boundary (not deep in implementation).
- Use `vi.spyOn` rather than replacing entire modules.

## CDK-Specific
- All construct props interfaces extend `cdk.StackProps` or define explicit prop types.
- Use `RemovalPolicy.RETAIN` for stateful resources in prod.
- Tag all constructs at the Stack level via `cdk.Tags.of(this).add(...)`.
- Avoid `cdk.Fn` string manipulation — prefer typed CDK constructs.

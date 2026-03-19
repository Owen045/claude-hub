---
name: temporal-workflow
description: >
  Use when creating, modifying, or debugging Temporal.io workflows and activities.
  Triggers on: Temporal, durable workflow, workflow definition, activity, worker,
  long-running process, retry logic, saga pattern.
---

# Temporal.io Workflow Skill

## Key Concepts to Apply
- **Workflows are deterministic**: No random, no datetime.now(), no direct I/O.
  All non-deterministic operations live in Activities.
- **Activities are the side-effects**: API calls, DB writes, LLM calls go here.
- **Workflows are resumable**: They can sleep for days. Design accordingly.

## Python Boilerplate

### Workflow Definition
```python
import asyncio
from datetime import timedelta
from temporalio import workflow
from temporalio.common import RetryPolicy

@workflow.defn
class AIPipelineWorkflow:
    @workflow.run
    async def run(self, input: PipelineInput) -> PipelineResult:
        # Activities called via workflow.execute_activity
        result = await workflow.execute_activity(
            call_llm_activity,
            input.prompt,
            start_to_close_timeout=timedelta(seconds=30),
            retry_policy=RetryPolicy(maximum_attempts=3),
        )
        return PipelineResult(output=result)
```

### Activity Definition
```python
from temporalio import activity

@activity.defn
async def call_llm_activity(prompt: str) -> str:
    # All real I/O here — this is retryable
    client = anthropic.AsyncAnthropic()
    message = await client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}],
    )
    return message.content[0].text
```

### Worker Registration
```python
from temporalio.client import Client
from temporalio.worker import Worker

async def main() -> None:
    client = await Client.connect("localhost:7233")
    worker = Worker(
        client,
        task_queue="ai-pipeline",
        workflows=[AIPipelineWorkflow],
        activities=[call_llm_activity],
    )
    await worker.run()
```

## Common Mistakes to Avoid
- Never import or call non-deterministic code in workflow body.
- Always set `start_to_close_timeout` — no default means infinite hang.
- Don't share state between workflow instances — use workflow parameters.
- Don't forget to register BOTH workflows and activities in the Worker.

## Quality Gates
- [ ] Workflow contains zero I/O calls
- [ ] All activities have explicit timeout + retry policy
- [ ] Worker registers both workflow and activity types
- [ ] Integration test covers happy path and at least one retry scenario

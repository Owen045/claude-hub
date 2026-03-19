"""
Temporal worker entrypoint.
Registers all workflows and activities, then polls the task queue.
"""
from __future__ import annotations

import asyncio
import os

import structlog
from temporalio.client import Client
from temporalio.worker import Worker

from workflows.activities import call_llm, store_result
from workflows.ai_pipeline_workflow import (
    AIPipelineWorkflow,
    critique_summary,
    summarise_document,
)

log = structlog.get_logger()

TASK_QUEUE = "ai-pipeline"


async def main() -> None:
    host = os.getenv("TEMPORAL_HOST", "localhost:7233")
    namespace = os.getenv("TEMPORAL_NAMESPACE", "default")

    log.info("worker_starting", host=host, namespace=namespace, task_queue=TASK_QUEUE)

    client = await Client.connect(host, namespace=namespace)

    worker = Worker(
        client,
        task_queue=TASK_QUEUE,
        workflows=[AIPipelineWorkflow],
        activities=[
            summarise_document,
            critique_summary,
            call_llm,
            store_result,
        ],
    )

    log.info("worker_running")
    await worker.run()


if __name__ == "__main__":
    asyncio.run(main())

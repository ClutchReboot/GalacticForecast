import uuid
import pytest
from unittest.mock import Mock, patch

from temporalio.client import WorkflowFailureError
from temporalio.testing import WorkflowEnvironment
from temporalio.worker import Worker

from activities.weather_api_activities import WeatherApiActivities
from shared import CurrentDetails
from workflows import OhioCurrent


class TestOhioCurrent:
    @pytest.mark.asyncio
    async def test_current_success(self) -> None:
        task_queue_name: str = str(uuid.uuid4())
        async with await WorkflowEnvironment.start_time_skipping() as env:
            data: CurrentDetails = CurrentDetails(
                location="London",
            )
            activities = WeatherApiActivities()
            async with Worker(
                env.client,
                task_queue=task_queue_name,
                workflows=[OhioCurrent],
                activities=[activities.current],
            ):
                result: str = await env.client.execute_workflow(
                    OhioCurrent.run,
                    data,
                    id=str(uuid.uuid4()),
                    task_queue=task_queue_name,
                )
                assert result.get("name") == "London"

    @pytest.mark.asyncio
    async def test_workflow_failure_exception(self) -> None:
        task_queue_name: str = str(uuid.uuid4())
        async with await WorkflowEnvironment.start_time_skipping() as env:
            data: CurrentDetails = CurrentDetails(
                location="London",
            )

            activities = WeatherApiActivities()
            async with Worker(
                env.client,
                task_queue=task_queue_name,
                workflows=[OhioCurrent],
                activities=[activities.current],
            ):
                with patch(
                    "temporalio.client.Client.execute_workflow",
                    side_effect=WorkflowFailureError(),
                ):
                    with pytest.raises(WorkflowFailureError):
                        await env.client.execute_workflow(
                            OhioCurrent.run,
                            data,
                            id=str(uuid.uuid4()),
                            task_queue=task_queue_name,
                        )

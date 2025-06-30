# @@@SNIPSTART money-transfer-project-template-python-tests
import uuid

import pytest
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
                print(f"{result=}")
                assert result.get("name") == "London"

    @pytest.mark.asyncio
    async def test_money_transfer_withdraw_insufficient_funds(self) -> None:
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
                with pytest.raises(WorkflowFailureError) as excinfo:
                    await env.client.execute_workflow(
                        OhioCurrent.run,
                        data,
                        id=str(uuid.uuid4()),
                        task_queue=task_queue_name,
                    )


    @pytest.mark.asyncio
    async def test_money_transfer_withdraw_invalid_account(self) -> None:
        task_queue_name: str = str(uuid.uuid4())
        async with await WorkflowEnvironment.start_time_skipping() as env:
            data: CurrentDetails = CurrentDetails(
                location="London234",
            )

            activities = WeatherApiActivities()
            async with Worker(
                env.client,
                task_queue=task_queue_name,
                workflows=[OhioCurrent],
                activities=[activities.current],
            ):
                with pytest.raises(WorkflowFailureError) as excinfo:
                    await env.client.execute_workflow(
                        OhioCurrent.run,
                        data,
                        id=str(uuid.uuid4()),
                        task_queue=task_queue_name,
                    )


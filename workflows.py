from datetime import timedelta

from temporalio import workflow
from temporalio.common import RetryPolicy
from temporalio.exceptions import ActivityError

with workflow.unsafe.imports_passed_through():
    from weather_api_app.activities import WeatherApiActivities
    from weather_api_app.shared import CurrentDetails


@workflow.defn
class OhioCurrent:
    @workflow.run
    async def run(self, current_details: CurrentDetails) -> dict:
        retry_policy = RetryPolicy(
            maximum_attempts=3,
            maximum_interval=timedelta(seconds=2),
            non_retryable_error_types=["InvalidLocationError"],
        )

        # Get Current weather
        try:
            result = await workflow.execute_activity_method(
                WeatherApiActivities.current,
                current_details,
                start_to_close_timeout=timedelta(seconds=5),
                retry_policy=retry_policy,
            )
            print(f"{result=}")
            return result
        except ActivityError as current_err:
            workflow.logger.error(f"Unable to get weather info: {current_err}")
        except Exception:
            raise

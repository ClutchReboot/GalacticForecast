import asyncio

from temporalio.client import Client
from temporalio.worker import Worker

from shared import WEATHER_API_CURRENT_QUEUE_NAME
from activities.weather_api_activities import WeatherApiActivities
from workflows import OhioCurrent


async def main() -> None:
    client: Client = await Client.connect("192.168.0.50:7233", namespace="default")
    # Run the worker
    activities = WeatherApiActivities()
    worker: Worker = Worker(
        client,
        task_queue=WEATHER_API_CURRENT_QUEUE_NAME,
        workflows=[OhioCurrent],
        activities=[activities.current],
    )
    await worker.run()


if __name__ == "__main__":
    asyncio.run(main())

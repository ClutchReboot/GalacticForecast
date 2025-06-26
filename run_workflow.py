import asyncio
import traceback

from temporalio.client import Client, WorkflowFailureError

from shared import CurrentDetails, WEATHER_API_CURRENT_QUEUE_NAME
from workflows import OhioCurrent


async def main() -> None:
    # Create client connected to server at the given address
    client: Client = await Client.connect("192.168.0.50:7233")

    data: CurrentDetails = CurrentDetails(location="Ohio")

    try:
        result = await client.execute_workflow(
            OhioCurrent.run,
            data,
            id="ohio-100",
            task_queue=WEATHER_API_CURRENT_QUEUE_NAME,
        )

        print(f"Result: {result}")

    except WorkflowFailureError:
        print("Got expected exception: ", traceback.format_exc())


if __name__ == "__main__":
    asyncio.run(main())

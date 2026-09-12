import asyncio
import websockets


async def main():
    uri = "ws://127.0.0.1:8000/ws/shops/"

    print("Connecting to WebSocket...")

    async with websockets.connect(uri) as websocket:
        print("WebSocket connected!")
        print("Waiting for shop updates...")

        while True:
            message = await websocket.recv()
            print("Received:", message)


asyncio.run(main())

import asyncio
import websockets

async def echo(websocket, path):
    # This function echoes back messages received from the client
    async for message in websocket:
        print(f"Received: {message}")  # Print received data
        await websocket.send(message)  # Echo the received data back

async def start_server():
    # Start the WebSocket server
    async with websockets.serve(echo, "localhost", 8765):
        await asyncio.Future()  # Keep the server running indefinitely

# Run the server
asyncio.run(start_server())


async def printing_bill(websocket):
    async for message in websocket:
        print(f"Received: {message}")

        await websocket.send('message received')
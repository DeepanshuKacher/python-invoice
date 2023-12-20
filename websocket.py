import asyncio
import websockets
import json
from invoice import print_with_margins_and_cut
from kotprint import kotPrint

def print_bill(message):
    message_dict = json.loads(message)
    printer_name = 'RETSOL RTP-80'
    print_with_margins_and_cut(printer_name,message_dict)

def print_kot(message):
    message_dict = json.loads(message)
    printer_name = 'RETSOL RTP-80'
    return  kotPrint(printer_name,message_dict)

    
async def echo(websocket, path):
    # This function echoes back messages received from the client
    async for message in websocket:
        if path == '/bill':
            response =  print_bill(message)  # Print received data
            await websocket.send('OK')  # Echo the received data back
        elif path == '/kot':
            response =  print_kot(message)  # Print received data
            data_to_send = {
                "status": "OK",
                "response":response
            }
            await websocket.send(json.dumps(data_to_send))  # Echo the received data back

async def start_server():
    # Start the WebSocket server
    async with websockets.serve(echo, "localhost", 8765):
        await asyncio.Future()  # Keep the server running indefinitely

# Run the server
asyncio.run(start_server())

import json
from services.trading.tradingService import trading_service


# Example methods
async def handle_trade(stock_type, action):
    result = f"Trade executed for {stock_type} with action {action}."
    print(result)
    return result  # Return the result to the client


async def handle_alert(stock_type, action):
    result = f"Alert generated for {stock_type} with action {action}."
    print(result)
    return result  # Return the result to the client


# WebSocket handler
async def handle_client(websocket):
    async for message in websocket:
        try:
            # Parse incoming JSON payload
            data = json.loads(message)
            message_type = data.get('message_type')
            stock_type = data.get('stock_type')
            action = data.get('action')

            print(f"Received: {data}")
            print(message_type)

            # Dynamically call methods based on message type
            if message_type == "trade":
                response = trading_service(data.get('payload'))
            else:
                response = f"Unknown message type: {message_type}"
            response["message_type"] = message_type
            # Send the method's response back to the client
            await websocket.send(json.dumps(response))

        except Exception as e:
            error_message = f"Error occurred: {str(e)}"
            print(error_message)
            await websocket.send(error_message)


# Start WebSocket server
# async def start_server():
#     server = await websockets.serve(handle_client, "localhost", 8765)
#     print("WebSocket server is running on ws://localhost:8765")
#     await server.wait_closed()


# Run server
# asyncio.run(start_server())

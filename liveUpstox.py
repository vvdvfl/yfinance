from upstox_client import upstoxclient
from upstox_client.websocket import WebSocket
import asyncio
# import websocket

API_KEY = '055f802e-bb63-4e1f-93d3-b86aad059e5c'
ACCESS_TOKEN = 'eyJ0eXAiOiJKV1QiLCJrZXlfaWQiOiJza192MS4wIiwiYWxnIjoiSFMyNTYifQ.eyJzdWIiOiI0WUFQTjIiLCJqdGkiOiI2ODE5ODkzNTlmMzI1YjVjM2Y0NTUzYTciLCJpc011bHRpQ2xpZW50IjpmYWxzZSwiaXNQbHVzUGxhbiI6ZmFsc2UsImlhdCI6MTc0NjUwMzk4OSwiaXNzIjoidWRhcGktZ2F0ZXdheS1zZXJ2aWNlIiwiZXhwIjoxNzQ2NTY4ODAwfQ.eJJaCYl6DPp89w-sPcQ1Qh_oX3wEnAK17fGHUAaAWy0'  # Must be fresh

# 1. Create client (you must have already fetched access_token via OAuth flow)
client = UpstoxClient(api_key=api_key, access_token=access_token)

# 2. Create WebSocket client
ws = WebSocket(api_key=api_key, access_token=access_token)

# 3. Define callbacks
def on_connect():
    print("WebSocket connected")

    # Example: NSE_EQ_TATAMOTORS token
    ws.subscribe('NSE_EQ|INE155A01022', 'ltp')

def on_message(msg):
    print("Tick:", msg)

def on_error(e):
    print("Error:", e)

# 4. Bind events
ws.on_connect = on_connect
ws.on_message = on_message
ws.on_error = on_error

# 5. Start WebSocket loop
asyncio.run(ws.connect())
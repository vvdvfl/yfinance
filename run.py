import threading
import asyncio
# import websockets
from flask import Flask

import main
from my_socket import handle_client

app = Flask(__name__)
# app.config['DEBUG'] = True
app.secret_key = 'your_super_secret_key_here'
app.add_url_rule('/', view_func=main.getUpstoxCode, methods=['GET'])
app.add_url_rule('/get_historic_data', view_func=main.get_historic_data, methods=['GET'])
app.add_url_rule('/getUpstoxCode', view_func=main.getUpstoxCode, methods=['GET'])
app.add_url_rule('/upstoxlogin', view_func=main.upstoxlogin, methods=['GET'])
app.add_url_rule('/checkToken', view_func=main.trading, methods=['GET'])
app.add_url_rule('/trading', view_func=main.trading, methods=['GET'])


def run_flask():
    # app.run(debug=True, use_reloader=False)
    app.run('localhost', '8000')


# if __name__ == '__main__':
#     # Start Flask in a separate thread
#     flask_thread = threading.Thread(target=run_flask)
#     flask_thread.start()
#
#     # Start WebSocket server in the main thread
#     asyncio.run(start_server())

#
# async def start_server():
#     server = await websockets.serve(handle_client, "localhost", 8765)
#     print("WebSocket server is running on ws://localhost:8765")
#     await server.wait_closed()

if __name__ == '__main__':
    # try:
        # Start Flask in a separate thread
    # flask_thread = threading.Thread(target=run_flask, daemon=True)
    # flask_thread.start()
    #
    # # Run WebSocket server inside an asyncio event loop
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(start_server())

    # except KeyboardInterrupt:
    #     print("\nReceived CTRL + C, shutting down...")
    #
    #     # Gracefully cancel all pending tasks
    #     loop.run_until_complete(shutdown(loop))
    #
    #     loop.close()
    #
    #     flask_thread.join()
    #     print("Server terminated successfully.")


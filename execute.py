from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import main
import json

from services.trading.tradingService import trading_service, plain_intraday_stratagy
from services.upstox.upstoxService import get_trades_of_day

app = Flask(__name__)
socketio = SocketIO(app)

app.config['SECRET_KEY'] = 'your_super_secret_key_here'
# socketio = SocketIO(app, async_mode='eventlet')

socketio = SocketIO(app, cors_allowed_origins='*')
app.secret_key = 'your_super_secret_key_here'
app.add_url_rule('/', view_func=main.getUpstoxCode, methods=['GET'])
app.add_url_rule('/get_historic_data', view_func=main.get_historic_data, methods=['GET'])
app.add_url_rule('/getUpstoxCode', view_func=main.getUpstoxCode, methods=['GET'])
app.add_url_rule('/upstoxlogin', view_func=main.upstoxlogin, methods=['GET'])
app.add_url_rule('/trading', view_func=main.trading, methods=['GET'])





@socketio.on('message')
def handle_message(message):
    # print(f"Received message: {message}")

    try:
        # Parse incoming JSON payload
        data = json.loads(message)
        print(data)
        payload = data.get('payload')
        message_type = data.get('message_type')
        stock_type = payload.get('stock_type')
        action = data.get('action')

        # print(f"Received: {data}")
        # print(message_type)

        # Dynamically call methods based on message type
        if message_type == "plain_intraday_stratagy":
            intradayResponse = plain_intraday_stratagy(stock_type)
            print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
            response = {
                "message": action,
                "message_type": message_type,
                "intraday_decission": intradayResponse
            }
            print(response)
            socketio.send(response)
        elif message_type == "trade":
            response = trading_service(data.get('payload'))
            response["message_type"] = message_type
            socketio.send(response)
        elif message_type == "dayOrders":
            print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
            api_response = get_trades_of_day('instruments_code', 'ALL')
            print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
            print(api_response)
            html_content = render_template('day_order_details.html', trade_data=api_response)
            socketio.emit('response_html', {'html': html_content, 'message_type': message_type})
        else:
            response = f"Unknown message type: {message_type}"
            socketio.send(response)
        # Send the method's response back to the client

    except Exception as e:
        error_message = f"Error occurred: {str(e)}"
        print(error_message)
        socketio.send(error_message)

if __name__ == '__main__':
    socketio.run(app, port=8000, debug=True)

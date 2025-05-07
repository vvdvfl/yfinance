const intervalMap = {};
const host = window.location.hostname;



 var socket = io("http://"+host+":8000");

        socket.on('connect', function() {
            console.log('Connected to server');
            socket.send('Hello, Server!');
        });

        socket.on('message', function(msg) {
            const messageType = msg.message_type;
            if(messageType == "trade") {
                handleTradeResponse(msg);
            } else if(messageType == "plain_intraday_stratagy") {
                handlePlanIntraDayStratagyResponse(msg);
            }
        });

        socket.on('response_html', function(msg) {

                    console.log(msg.message_type);
                    if(msg.message_type == "dayOrders"){
                        handleDayOrdersResponse(msg);
                    }
        });

function handleDayOrdersResponse(jsonResponse) {
    document.getElementById("overlay-content").innerHTML = jsonResponse.html;
    openOverlay();
}


function startInterval(key, duration) {
    if (intervalMap[key]) {
        console.log(`Interval with key "${key}" already exists!`);
        return;
    }

    const intervalId = setInterval(() => startPlainIntradayStratagyTrading("auto"), duration);
    intervalMap[key] = intervalId; // Store interval ID with the key
}
// Clear a specific interval by key
function clearIntervalByKey(key) {
    if (intervalMap[key]) {
        clearInterval(intervalMap[key]); // Clear interval
        delete intervalMap[key]; // Remove the key from the map
    } else {
        console.log(`No interval found with key: "${key}"`);
    }
}
// Clear all intervals
function clearAllIntervals() {
    for (const key in intervalMap) {
        clearInterval(intervalMap[key]);
        delete intervalMap[key];
    }
}

function startTrading(type){
        const stock_type = document.getElementById("StockType").value;
        const quantity = document.getElementById("StockQuantity").value;
        const action = document.getElementById("TradeAction").value;
        const automated = document.getElementById("tradeAutomated").checked;
        // Construct payload
        const message_type = "trade";
        const payload = JSON.stringify({
            message_type,
            "payload": {
                stock_type,
                quantity,
                action,
                automated
            }
        });
        document.getElementById("stockName").innerHTML = stock_type;
        // Send to WebSocket server
//        ws.send(payload);
        socket.emit('message', payload);
        if(typeof intervalMap[stock_type] == 'undefined' && type =="button") {
            startInterval(stock_type, 10000)
        }
        disableEnableFields(true)
}
function startPlainIntradayStratagyTrading(type){
        const stock_type = document.getElementById("StockType").value;
        const quantity = document.getElementById("StockQuantity").value;
        const action = document.getElementById("TradeAction").value;
        const automated = document.getElementById("tradeAutomated").checked;
        // Construct payload
        const message_type = "plain_intraday_stratagy";
        const payload = JSON.stringify({
            message_type,
            "payload": {
                stock_type,
                quantity,
                action,
                automated
            }
        });
        document.getElementById("stockName").innerHTML = stock_type;
        // Send to WebSocket server
//        ws.send(payload);
        socket.emit('message', payload);
        if(typeof intervalMap[stock_type] == 'undefined' && type =="button") {
            startInterval(stock_type, 5000)
        }
        disableEnableFields(true)
}



function getDayOrders() {
    const message_type = "dayOrders"
    const payload = JSON.stringify({
                message_type
            });
//    document.getElementById("stockName").innerHTML = stock_type;
    // Send to WebSocket server
//        ws.send(payload);
    socket.emit('message', payload);
}
function handleTradeResponse(jsonResponse) {
    if(typeof jsonResponse.dateTime != 'undefined') {
        const responseDiv = document.getElementById("response");
        if(jsonResponse.order_status != "") {
            const order_status = `Order palaced for ${jsonResponse.stock_name} and status is ${jsonResponse.order_status}.`;
            responseDiv.insertAdjacentHTML('afterbegin', `<p>${order_status}</p>`);
        }
        const displayMessage = `@${jsonResponse.dateTime} |  ${jsonResponse.currentPrice}(CP)|  ${jsonResponse.stock_name} | ${jsonResponse.message}` ;
        responseDiv.insertAdjacentHTML('afterbegin', `<p>${displayMessage}</p>`);
        document.getElementById("stockCurrentPrice").innerHTML = jsonResponse.intraday_decission.currentPrice;
        document.getElementById("stockBuyPrice").innerHTML = jsonResponse.buy_levels?.["61.8%"] || "N/A";
        document.getElementById("stockBuyPrice50").innerHTML = jsonResponse.buy_levels?.["50%"] || "N/A";
        document.getElementById("stockSellPrice").innerHTML = jsonResponse.sell_levels?.["61.8%"] || "N/A";
    }

}

function handlePlanIntraDayStratagyResponse(jsonResponse){
}
function stopTrading() {
    const stock_type = document.getElementById("StockType").value;
    disableEnableFields(false)
    clearIntervalByKey(stock_type)
}

function clearHistory() {
    const responseDiv = document.getElementById("response");
    responseDiv.innerHTML = ``;
}

function disableEnableFields(action) {
    document.getElementById("StockType").disabled = action;
    document.getElementById("tradeStartButton").disabled = action;
}


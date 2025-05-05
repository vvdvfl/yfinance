    // Object to store interval IDs with unique keys

function startInterval(key, duration) {
    if (intervalMap[key]) {
        console.log(`Interval with key "${key}" already exists!`);
        return;
    }

    const intervalId = setInterval(() => startTrading("auto"), duration);
    intervalMap[key] = intervalId; // Store interval ID with the key
    console.log(`Started interval with key: "${key}" and ID: ${intervalId}`);
}
// Clear a specific interval by key
function clearIntervalByKey(key) {
    if (intervalMap[key]) {
        clearInterval(intervalMap[key]); // Clear interval
        console.log(`Cleared interval with key: "${key}" and ID: ${intervalMap[key]}`);
        delete intervalMap[key]; // Remove the key from the map
    } else {
        console.log(`No interval found with key: "${key}"`);
    }
}
// Clear all intervals
function clearAllIntervals() {
    for (const key in intervalMap) {
        clearInterval(intervalMap[key]);
        console.log(`Cleared interval with key: "${key}" and ID: ${intervalMap[key]}`);
        delete intervalMap[key];
    }
}

function startTrading(type){


        alert("invoked");



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
        if(!intervalMap[stock_type] && type =="button") {
            startInterval(stock_type, 5000)
        }
        disableEnableFields(true)
}
function handleTradeResponse(jsonResponse) {
    const responseDiv = document.getElementById("response");
    const displayMessage = `@${jsonResponse.dateTime} |  ${jsonResponse.currentPrice}(CP)|  ${jsonResponse.stockName} | ${jsonResponse.message}` ;
    responseDiv.insertAdjacentHTML('afterbegin', `<p>${displayMessage}</p>`);
    console.log(jsonResponse);
    document.getElementById("stockCurrentPrice").innerHTML = jsonResponse.currentPrice;
    document.getElementById("stockBuyPrice").innerHTML = jsonResponse.buy_levels['61.8%'];
    document.getElementById("stockBuyPrice50").innerHTML = jsonResponse.buy_levels['50%'];
    document.getElementById("stockSellPrice").innerHTML = jsonResponse.sell_levels['61.8%'];

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
import webbrowser
from datetime import time
import yfinance as yf
import pandas as pd
import requests
from flask import request, redirect, url_for, session, render_template
from selenium import webdriver
import time
from services.yfinance.service import *
from stratagy.Fibonacci import *
from util.DisplayUtil import *


api_version = '2.0'
code = 'eyJ0eXAiOiJKV1QiLCJrZXlfaWQiOiJza192MS4wIiwiYWxnIjoiSFMyNTYifQ.eyJzdWIiOiI0WUFQTjIiLCJqdGkiOiI2ODA5OWM3NDkyYjAxNjYzNTNmM2NiZTkiLCJpc011bHRpQ2xpZW50IjpmYWxzZSwiaWF0IjoxNzQ1NDYwMzQwLCJpc3MiOiJ1ZGFwaS1nYXRld2F5LXNlcnZpY2UiLCJleHAiOjE3NDU1MzIwMDB9._pz8aXsG26wnH19OS_WHUKtA2vNTMCMX2N_GEwrUv4E'
client_id = '055f802e-bb63-4e1f-93d3-b86aad059e5c'
client_secret = 'vebx96wu4d'
redirect_uri = 'http://localhost:8000/upstoxlogin'
grant_type = 'authorization_code'


def get_historic_data(days: int = 7) -> pd.DataFrame:
    """
    Get historic data for a given stock for the last 'days' days.
    """
    stock = request.args['stock']
    data = get_historic_data_service(days, stock)
    df = pd.DataFrame(data)

    # Convert DataFrame to HTML
    table_html = df.to_html(classes='table table-bordered')
    clickHereForAlgoTrade = "<a href='/trading?stock=" + stock + "'>Start algo trade</a>"
    # Render the HTML directly
    return displayHtml("Historic Data", f"Historic data for {stock} {clickHereForAlgoTrade}", table_html)


def getUpstoxCode():
    auth_url = (
        f"https://api.upstox.com/v2/login/authorization/dialog?"
        f"response_type=code&client_id={client_id}&redirect_uri={redirect_uri}"
    )
    webbrowser.open(auth_url)
    # Initialize the WebDriver (e.g., Chrome WebDriver)
    driver = webdriver.Chrome()
    # Perform any actions, then close the browser
    driver.quit()  # This will close the browser entirely


def upstoxlogin():
    code = request.args['code']
    url = 'https://api.upstox.com/v2/login/authorization/token'
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    data = {
        'code': code,
        'client_id': client_id,
        'client_secret': client_secret,
        'redirect_uri': redirect_uri,
        'grant_type': grant_type
    }

    response = requests.post(url, headers=headers, data=data)
    # write code to store access token in cookies
    if response.status_code == 200:
        response_data = response.json()
        access_token = response_data.get('access_token')
        # Store access token in session
        session['access_token'] = access_token
        return redirect(url_for("trading"))
    else:
        return f"Login failed: {response.text}", 400


def trading():
    # get access token from cookies
    access_token = session.get('access_token')
    print(access_token)
    return render_template('stock.html')


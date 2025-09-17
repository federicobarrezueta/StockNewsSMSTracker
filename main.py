import requests
from datetime import datetime, timedelta
import os
from twilio.rest import Client
import time

# The stock you want to track
STOCK = "TSLA"
COMPANY_NAME = "Tesla"
# Secrets
AV_API_KEY = "YOUR KEY"
AV_END_POINT = "https://www.alphavantage.co/query"
NEWS_API_KEY = "YOUR KEY"
NEWS_END_POINT = "https://newsapi.org/v2/top-headlines"
TWILIO_AUTH_TOKEN = "YOUR TOKEN"
TWILIO_ACCOUNT_SID = "YOUR SID"
FUNCTION = "TIME_SERIES_DAILY"
INTERVAL = "60min"
MY_TWILIO_NUMBER = "YOUR_TWILIO_NUMBER"
MY_NUMBER = "YOUR NUMBER"

# Yesterday's date using timedelta
yesterday = datetime.strftime(datetime.now() - timedelta(1), '%Y-%m-%d')

# day before Yesterday's date using timedelta
before_yesterday = datetime.strftime(datetime.now() - timedelta(2), '%Y-%m-%d')

# Alpha Vantage API usage
stock_params = {
    "function": FUNCTION,
    "symbol": STOCK,
    "api_key": AV_API_KEY,
}
av_request = requests.get(AV_END_POINT, params=stock_params)
av_data = av_request.json()

# News API usage
news_params = {
    "apiKey": NEWS_API_KEY,
    "q": COMPANY_NAME,
}

news_request = requests.get(NEWS_END_POINT, params=news_params)
news_data = news_request.json()

# Gets the rounded values of the closing values for yesterday and the day before
before_yesterday_close_val = round(float(av_data["Time Series (Daily)"][before_yesterday]['4. close']), 2)
yesterday_close_val = round(float(av_data["Time Series (Daily)"][yesterday]['4. close']), 2)

# Calculates the differences and the percentage delta
delta_value = round(yesterday_close_val - before_yesterday_close_val, 2)
percentage_delta = round((delta_value / yesterday_close_val) * 100, 2)

# If the absolute value of delta is greater than 5% then it prints
if abs(percentage_delta) > 5:
    print("Get news")

# initializes the lists
headlines = []
briefs = []

# gets the data to the lists
for i in range(3):
    headlines.append(news_data["articles"][i]["title"])
    briefs.append(news_data["articles"][i]["description"])

# gets the appropriate symbol if increase or decrease in stock value
if percentage_delta > 0:
    symbol = "+"
else:
    symbol = "-"

# Sends the 3 latest headlines for the selected stock

for i in range(3):
    # Formats the messages
    message_to_send = f"""

    {STOCK}: {symbol}{abs(percentage_delta)}%
    Headline: {headlines[i]}
    Brief: {briefs[i]}

    """

    # Creates the client for Twilio messaging and send the message
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    message = client.messages.create(
        body=message_to_send,
        from_=MY_TWILIO_NUMBER,
        to=MY_NUMBER,
    )

    print(message.status)


#import data from here, trying out visual studio code
import pandas as pd
pd.__version__
a = pd.read_csv("data.txt")
print(a.head(10))
print(a.shape)
a.columns.values
a["Theme"].value_counts()

# Going for some text analytics.
import requests
# pprint is used to format the JSON response
from pprint import pprint

import os
from dotenv import load_dotenv
load_dotenv()
subscription_key = os.getenv('SUBSCRIPTION_KEY')
endpoint = os.getenv('ENDPOINT')

from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

def authenticate_client():
    ta_credential = AzureKeyCredential(subscription_key)
    text_analytics_client = TextAnalyticsClient(
            endpoint=endpoint, credential=ta_credential)
    return text_analytics_client

client = authenticate_client()

# Detecting Languages:
language_api_url = endpoint + "/text/analytics/v3.0/languages"
documents = {"documents": [
    {"id": "1", "text": "This is a document written in English."},
    {"id": "2", "text": "Este es un document escrito en Español."},
    {"id": "3", "text": "这是一个用中文写的文件"}
]}
headers = {"Ocp-Apim-Subscription-Key": subscription_key}
response = requests.post(language_api_url, headers=headers, json=documents)
languages = response.json()
pprint(languages)

# Analyzing Sentiment:
sentiment_url = endpoint + "/text/analytics/v3.0/sentiment"
documents = {"documents": [
    {"id": "1", "language": "en",
        "text": "I really enjoy the new XBox One S. It has a clean look, it has 4K/HDR resolution and it is affordable."},
    {"id": "2", "language": "es",
        "text": "Este ha sido un dia terrible, llegué tarde al trabajo debido a un accidente automobilistico."}
]}
headers = {"Ocp-Apim-Subscription-Key": subscription_key}
response = requests.post(sentiment_url, headers=headers, json=documents)
sentiments = response.json()
pprint(sentiments)
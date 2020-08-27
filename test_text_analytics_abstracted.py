import os
import requests
from pprint import pprint
import pandas as pd
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

from dotenv import load_dotenv
load_dotenv()
subscription_key = os.getenv('SUBSCRIPTION_KEY')
endpoint = os.getenv('ENDPOINT')

def authenticate_client():
    ta_credential = AzureKeyCredential(subscription_key)
    text_analytics_client = TextAnalyticsClient(
            endpoint= endpoint, credential=ta_credential)
    return text_analytics_client


def sentiment_analysis_example(client, documents):
    sentiment_url = endpoint + "/text/analytics/v3.0/sentiment"
    headers = {"Ocp-Apim-Subscription-Key": subscription_key}
    response = requests.post(sentiment_url, headers=headers, json=documents)
    sentiments = response.json()

    print("Printing sentiments ... \n")
    pprint(sentiments)
    return sentiments


def extract_key_phrases(client, documents):
    keyphrase_url = endpoint + "/text/analytics/v3.0/keyphrases"
    headers = {"Ocp-Apim-Subscription-Key": subscription_key}
    response = requests.post(keyphrase_url, headers=headers, json=documents)
    key_phrases = response.json()

    print("Printing key phrases ... \n")
    pprint(key_phrases)
    return key_phrases

def identify_entities(client, documents):
    entities_url = endpoint + "/text/analytics/v3.0/entities/recognition/general"
    headers = {"Ocp-Apim-Subscription-Key": subscription_key}
    response = requests.post(entities_url, headers=headers, json=documents)
    entities = response.json()
    pprint(entities)

          

if __name__ == "__main__":
    data = pd.read_csv("data.txt")
    # data.columns.values
    # summary = data["Theme"].tolist() <-- this is the list of "themes" which will be replaced by the text ticket
    # print(type(summary))
    documents = {"documents": [
        {"id": "1", "language": "en",
            "text": "I do not like this hammer made by Black & Decker. It does not work correctly. I want to request a return."},
        {"id": "2", "language": "es",
            "text": "I've been trying to talk to someone about my sink problem. It won't hold all of my fish."}
    ]}

    client = authenticate_client()
    sentiments = sentiment_analysis_example(client, documents)
    key_phrases = extract_key_phrases(client, documents)
    identify_entities(client, documents)


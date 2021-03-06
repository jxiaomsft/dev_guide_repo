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

subscription_key = "499d0d54bea14b519a53d0c2148f797f"
endpoint = "https://devguidetextanalytics.cognitiveservices.azure.com/"

from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

def authenticate_client():
    ta_credential = AzureKeyCredential(subscription_key)
    text_analytics_client = TextAnalyticsClient(
            endpoint=endpoint, credential=ta_credential)
    return text_analytics_client

client = authenticate_client()
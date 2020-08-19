from azure.cognitiveservices.language.luis.authoring import LUISAuthoringClient
from azure.cognitiveservices.language.luis.runtime import LUISRuntimeClient
from msrest.authentication import CognitiveServicesCredentials
from functools import reduce

import json, time




def quickstart(): 

    # add calls here, remember to indent properly
    ...
# Creating and storing standard app variables

authoringKey = '6b5970f522cc4c81bbba49cb1aa22940'
authoringResourceName = "devguideluis-authoring"
predictionResourceName = "devguideluis-prediction"

authoringEndpoint = f'https://{authoringResourceName}.cognitiveservices.azure.com/'
predictionEndpoint = f'https://{predictionResourceName}.cognitiveservices.azure.com/'

appName = "Contoso Pizza Company"
versionId = "0.1"
intentName = "OrderPizzaIntent"

client = LUISAuthoringClient(authoringEndpoint, CognitiveServicesCredentials(authoringKey))

quickstart()
from azure.cognitiveservices.language.luis.authoring import LUISAuthoringClient
from azure.cognitiveservices.language.luis.runtime import LUISRuntimeClient
from msrest.authentication import CognitiveServicesCredentials
from functools import reduce
import pandas as pd
import numpy as np
import json, time
import os
from dotenv import load_dotenv
load_dotenv()


# Pull up data into data frame and convert structure to JSON.
data = pd.read_csv("data-output.csv")
short_data = data.head(5).loc[:, ["Text", "Theme"]]
# def text_to_JSON(row):
#     theme = row["Theme"]
#     text = row["Text"]
#     temp_json = {
#         "text": text,
#     "intentName": theme
#     }
#     return 
intents = []
for index, row in short_data.iterrows():        
    intents.append({"intentName":row["Theme"], 'text':row["Text"]})

print(intents)



# def quickstart(): 

#     # add calls here, remember to indent properly
#     ...
# # Creating and storing standard app variables

authoringKey = os.getenv('AUTHORINGKEY')
authoringResourceName = os.getenv('AUTHORINGRESOURCENAME')
predictionResourceName = os.getenv('PREDICTIONRESOURCENAME')
print(type(authoringResourceName))
print(authoringResourceName)
print(predictionResourceName)
authoringEndpoint = 'https://' + authoringResourceName +  '.cognitiveservices.azure.com/'
predictionEndpoint = 'https://' + predictionResourceName + '.cognitiveservices.azure.com/'

print(authoringEndpoint)

appName = "Tailwind Traders"
versionId = "0.2"
intentName = "Speed"

client = LUISAuthoringClient(authoringEndpoint, CognitiveServicesCredentials(authoringKey))
print(type(client))


# define app basics
appDefinition = {
    "name": appName,
    "initial_version_id": versionId,
    "culture": "en-us"
}

# create app
app_id = client.apps.add(appDefinition)

# get app id - necessary for all other changes
print("Created LUIS app with ID {}".format(app_id))

client.model.add_intent(app_id, versionId, intentName)
# # Add Prebuilt entity
# client.model.add_prebuilt(app_id, versionId, prebuilt_extractor_names=["number"])

# # define machine-learned entity
# mlEntityDefinition = [
# {
#     "name": "Pizza",
#     "children": [
#         { "name": "Quantity" },
#         { "name": "Type" },
#         { "name": "Size" }
#     ]
# },
# {
#     "name": "Toppings",
#     "children": [
#         { "name": "Type" },
#         { "name": "Quantity" }
#     ]
# }]

# # add entity to app
# modelId = client.model.add_entity(app_id, versionId, name="Pizza order", children=mlEntityDefinition)

# # define phraselist - add phrases as significant vocabulary to app
# phraseList = {
#     "enabledForAllModels": False,
#     "isExchangeable": True,
#     "name": "QuantityPhraselist",
#     "phrases": "few,more,extra"
# }

# def get_grandchild_id(model, childName, grandChildName):
    
#     theseChildren = next(filter((lambda child: child.name == childName), model.children))
#     theseGrandchildren = next(filter((lambda child: child.name == grandChildName), theseChildren.children))
    
#     grandChildId = theseGrandchildren.id
    
#     return grandChildId

# # add phrase list to app
# phraseListId = client.features.add_phrase_list(app_id, versionId, phraseList)

# # Get entity and subentities
# modelObject = client.model.get_entity(app_id, versionId, modelId)
# toppingQuantityId = get_grandchild_id(modelObject, "Toppings", "Quantity")
# pizzaQuantityId = get_grandchild_id(modelObject, "Pizza", "Quantity")

# # add model as feature to subentity model
# prebuiltFeatureRequiredDefinition = { "model_name": "number", "is_required": True }
# client.features.add_entity_feature(app_id, versionId, pizzaQuantityId, prebuiltFeatureRequiredDefinition)

# # add model as feature to subentity model
# prebuiltFeatureNotRequiredDefinition = { "model_name": "number" }
# client.features.add_entity_feature(app_id, versionId, toppingQuantityId, prebuiltFeatureNotRequiredDefinition)

# # add phrase list as feature to subentity model
# phraseListFeatureDefinition = { "feature_name": "QuantityPhraselist", "model_name": None }
# client.features.add_entity_feature(app_id, versionId, toppingQuantityId, phraseListFeatureDefinition)



# Define labeled example
# labeledExampleUtteranceWithMLEntity = {
#     "text": "This delivery time for my goose is really long, I am annoyed.",
#     "intentName": intentName
# }

# print("Labeled Example Utterance:", labeledExampleUtteranceWithMLEntity)

# Add an example for the entity.
# Enable nested children to allow using multiple models with the same name.
# The quantity subentity and the phraselist could have the same exact name if this is set to True
# client.examples.add(app_id, versionId, labeledExampleUtteranceWithMLEntity, { "enableNestedChildren": True })
for i in intents:
    client.examples.add(app_id, versionId, i)
# Train the app
client.train.train_version(app_id, versionId)
waiting = True
while waiting:
    info = client.train.get_status(app_id, versionId)

    # get_status returns a list of training statuses, one for each model. Loop through them and make sure all are done.
    waiting = any(map(lambda x: 'Queued' == x.details.status or 'InProgress' == x.details.status, info))
    if waiting:
        print ("Waiting 10 seconds for training to complete...")
        time.sleep(10)
    else: 
        print ("trained")
        waiting = False
# Publish a Language Understanding app
responseEndpointInfo = client.apps.publish(app_id, versionId, is_staging=False)
# Authenticate the prediction runtime client
runtimeCredentials = CognitiveServicesCredentials(authoringKey)
clientRuntime = LUISRuntimeClient(endpoint=predictionEndpoint, credentials=runtimeCredentials)

# Get prediction from runtime
# Production == slot name
predictionRequest = { "query" : "I want two small pepperoni pizzas with more salsa" }

predictionResponse = clientRuntime.prediction.get_slot_prediction(app_id, "Production", predictionRequest)
print("Top intent: {}".format(predictionResponse.prediction.top_intent))
print("Sentiment: {}".format (predictionResponse.prediction.sentiment))
print("Intents: ")

for intent in predictionResponse.prediction.intents:
    print("\t{}".format (json.dumps (intent)))
print("Entities: {}".format (predictionResponse.prediction.entities))
# quickstart()

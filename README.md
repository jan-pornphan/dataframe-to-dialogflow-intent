# csv-to-dialogflow-intent

csv-to-dialogflow-intent helps create intents in Dialogflow by uploading csv or excel file. 

# Quickstart
1.  Create a bot in [Dialogflow](https://dialogflow.com/) and select a Google Cloud [Project](https://console.cloud.google.com/cloud-resource-manager) for your bot
2.  Enable [Dialogflow API](https://console.cloud.google.com/flows/enableapi?apiid=dialogflow.googleapis.com) for your Google Project 
3.  [Enable billing](https://cloud.google.com/billing/docs/how-to/modify-project?visit_id=1-636680888290109380-2595139068&rd=1#enable-billing) for your project
4. [Create a service account](https://cloud.google.com/docs/authentication/getting-started) for your project in your GCP console
5. Set up authentication in your terminal
```sh
$ gcloud auth activate-service --key-file=KEY_FILE
```
- **KEY_FILE**
path to the private key file (JSON file obtained from creating a service account key)

6. Set up your configuration in config.py 
```sh
config = {
    'project_id':   '<YOUR DIALOGFLOW PROJECT ID>',
    'env':  '<YOUR KEY FILE>',
    'filename': '<YOUR FILENAME.xlsx>',
    'sheetname':    '<SHEET NAME>',
    'platform_default_custom_payload': 'line'
}
```
7. Run main function to create intents in dialogflow
```sh
df = pd.read_excel(config['filename'])
ib = IntentBuilder(project_id, session_id)
ib.create_intents(df)
```
------------
## Sample excel file description

- **root_intent** 
Root intent in the chain of followup intents
- **parent_intent**
Intent preceding each followup intents
- **intent_name**
The name of each intent
- **training_phrases**
Training phrases in dialogflow for the intent. Each cell represents a single user expression
- **response_type**
Facebook: text, quick reply, card, image, payload
Line: text, payload
- **response**
Text response variations are separated by comma in the same cell
Different block of text responses are filled in different cells
Facebook payload format can be found in the [documentation](https://developers.facebook.com/docs/messenger-platform/send-messages)
Line custom payload [documentation](https://developers.line.me/en/docs/messaging-api/message-types/)
- **platform**
facebook, default (use 'default' for line platform)
- **fallback**
TRUE if the intent is fallback intent, otherwise FALSE








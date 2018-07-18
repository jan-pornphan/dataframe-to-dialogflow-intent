import pandas as pd
from intent_builder import IntentBuilder
import os
import uuid

# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "dialogflow-sdk-test-f7fbd9c66588.json"

# project_id = 'dialogflow-sdk-test'

project_id = 'testagent-379ff'
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="testagent-379ff-d76830023068.json"
session_id = uuid.uuid4()
# df = pd.read_csv('BookTest.csv')




import json
df = pd.read_csv('BookTest.csv')

# df1 = df.iloc[:1,:]
# print('df1\n', df1)
# #df1 = pd.read_excel('SCBAM_intent_rec.xlsx')
ib = IntentBuilder(project_id, session_id)
ib.create_intents(df)


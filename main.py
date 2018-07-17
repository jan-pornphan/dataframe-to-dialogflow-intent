import pandas as pd
from intent_builder import IntentBuilder
import os
import uuid

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "dialogflow-sdk-test-f7fbd9c66588.json"

project_id = 'dialogflow-sdk-test'
session_id = uuid.uuid4()
df = pd.read_csv('BookTest.csv')

ib = IntentBuilder(project_id, session_id)
ib.create_intents(df)

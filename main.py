import pandas as pd
from intent_builder.intent_builder import IntentBuilder
import os
import uuid
from config import config
import xlrd

project_id = config['project_id']
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = config['env']
session_id = uuid.uuid4()

df = pd.read_excel(config['filename'], sheet_name = config['sheetname'])
ib = IntentBuilder(project_id, session_id)
ib.create_intents(df)

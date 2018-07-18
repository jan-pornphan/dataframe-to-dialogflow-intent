import dialogflow_v2 as dialogflow
import json
from dialogflow_v2.types import Intent
from message_handler import handle_message


def dataframe_to_intent(display_name, df, root_id, parent_id, input_context_names, output_contexts, action):
    # TODO: Add fallback as option
    training_phrases = _get_training_phrases(df['training_phrases'].dropna())
    messages = _get_messages(df[['response_type', 'response','platform']].dropna())
    fallback = _get_fallback(df['fallback'].dropna().values[0])
    intent = Intent(
        display_name=display_name,
        training_phrases=training_phrases,
        messages=messages,
        root_followup_intent_name=root_id,
        parent_followup_intent_name=parent_id,
        output_contexts=output_contexts,
        input_context_names=input_context_names,
        action=action,
        is_fallback=fallback
    )
    return intent


def _get_training_phrases(series):
    training_phrases = []
    for text in series:
        part = Intent.TrainingPhrase.Part(text=text)  # text: "hi"
        training_phrase = Intent.TrainingPhrase(
            parts=[part])  # parts{text: "hi"}
        training_phrases.append(training_phrase)  # [parts{},parts{}]
    return training_phrases


def _get_messages(series):
    messages = []
    for _, row in series.iterrows():
        message = handle_message(row['response'], row['response_type'], row['platform'])
        messages.append(message)
    return messages

def _get_fallback(boolean):
    if boolean == 'True':
        return True
    elif boolean == 'False':
        return False
    else:
        return boolean
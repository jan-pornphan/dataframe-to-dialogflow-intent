import dialogflow_v2 as dialogflow
from dialogflow_v2.types import Intent
import json
from .message_handler import handle_message


def dataframe_to_intent(display_name, df, root_id, parent_id, input_context_names, output_contexts, action):
    """ Convert the intent dataframe to Dialogflow intent """
    training_phrases = _get_training_phrases(df['training_phrases'].dropna())
    messages = _get_messages(
        df[['response_type', 'response', 'platform']].dropna())
    fallback = _get_fallback(df['fallback'].dropna())
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
        part = Intent.TrainingPhrase.Part(text=text)
        training_phrase = Intent.TrainingPhrase(parts=[part])
        training_phrases.append(training_phrase)
    return training_phrases


def _get_messages(series):
    messages = []
    for _, row in series.iterrows():
        message = handle_message(
            row['response'], row['response_type'], row['platform'])
        messages.append(message)
    return messages

def _get_fallback(series):
    return bool(series.values[0])
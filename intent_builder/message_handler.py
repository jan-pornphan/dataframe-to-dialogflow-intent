from dialogflow_v2.types import Intent
import json
from google.protobuf.struct_pb2 import Struct, Value
from config import config

platform_type = {'default': 0, 'facebook': 1}
platform_default_custom_payload = config['platform_default_custom_payload']


def handle_message(response, response_type, platform):
    """ Convert response to Dialogflow intent response """
    if platform == 'facebook':
        return _handle_facebook_message(response, response_type)
    return _handle_default_message(response, response_type)


#
# Facebook Message Handle
#
def _handle_facebook_message(response, response_type):
    if response_type == 'quick reply':
        return _handle_quick_reply(response)
    elif response_type == 'card':
        return _handle_card(response)
    elif response_type == 'image':
        return _handle_image(response)
    elif response_type == 'payload':
        return _handle_facebook_custom_payload(response)
    return _handle_facebook_text(response)


def _handle_facebook_text(response):
    return Intent.Message(
        platform=platform_type['facebook'],
        text=Intent.Message.Text(text=response.split(','))
    )


def _handle_quick_reply(response):
    obj = json.loads(response)
    return Intent.Message(
        platform=platform_type['facebook'],
        quick_replies=Intent.Message.QuickReplies(
            title=obj['title'],
            quick_replies=obj['quick_replies'].split(',')
        )
    )


def _handle_card(response):
    obj = json.loads(response)
    button_texts = obj['button'].split(',')
    buttons = []
    for button in button_texts:
        text = Intent.Message.Card.Button(text=button)
        buttons.append(text)

    return Intent.Message(
        platform=platform_type['facebook'],
        card=Intent.Message.Card(
            title=obj['title'],
            subtitle=obj['subtitle'],
            image_uri=obj['image_uri'],
            buttons=buttons
        )
    )


def _handle_image(response):
    obj = json.loads(response)
    return Intent.Message(
        platform=platform_type['facebook'],
        image=Intent.Message.Image(
            image_uri=obj['image_uri']
        )
    )


def _handle_facebook_custom_payload(response):
    obj = json.loads(response)
    payload = Struct()
    payload['facebook'] = obj
    return Intent.Message(
        platform=platform_type['facebook'],
        payload=payload
    )

#
# Default Message Handle
#
def _handle_default_message(response, response_type):
    if response_type == 'payload':
        return _handle_default_custom_payload(response)
    return _handle_default_text(response)


def _handle_default_text(response):
    return Intent.Message(
        platform=platform_type['default'],
        text=Intent.Message.Text(text=response.split(','))
    )


def _handle_default_custom_payload(response):
    obj = json.loads(response)
    payload = Struct()
    payload[platform_default_custom_payload] = obj
    return Intent.Message(
        platform=platform_type['default'],
        payload=payload
    )

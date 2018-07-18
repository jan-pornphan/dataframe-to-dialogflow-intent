from dialogflow_v2.types import Intent
import json
from google.protobuf.struct_pb2 import Struct, Value

platform_type = {
    'default':   0,
    'facebook':   1
}


def handle_message(response, response_type, platform):    
    if response_type == 'quick reply':
        return _handle_quick_reply(response, platform)
    elif response_type == 'card':
        return _handle_card(response, platform)
    elif response_type == 'payload':
        return _handle_custom_payload(response, platform)

    return _handle_text(response, platform)


def _handle_text(response, platform):
    return Intent.Message(
        platform=platform_type[platform],
        text=Intent.Message.Text(text=response.split(','))
    )


def _handle_quick_reply(response, platform):
    obj = json.loads(response)
    return Intent.Message(
        platform=platform_type[platform],
        quick_replies=Intent.Message.QuickReplies(
            title=obj['title'],
            quick_replies=obj['quick_replies'].split(',')
        )
    )

def _handle_card(response, platform):
    obj = json.loads(response)
    button_texts = obj['button'].split(',')
    buttons = []
    for button in button_texts:
        text = Intent.Message.Card.Button(text=button)
        buttons.append(text)

    return Intent.Message(
        platform=platform_type[platform],
        card=Intent.Message.Card(
            title=obj['title'],
            subtitle=obj['subtitle'],
            image_uri=obj['image_uri'],
            buttons=buttons
        )
    )


def _handle_custom_payload(response, platform):
    obj = json.loads(response)
    payload = Struct()    
    payload[platform] = obj
    print(payload)
    return Intent.Message(
        platform = platform_type[platform],
        payload = payload
    )

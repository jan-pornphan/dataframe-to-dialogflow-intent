from dialogflow_v2.types import Intent
import json

platform = {
    'default':   0,
    'facebook':   1
}

def handle_message(response, response_type):
    #TODO: - handle custom payload Facebook
    #TODO: - handle text, custom payload Default
    if response_type == 'quick reply':
        return _handle_quick_reply(response)
    elif response_type == 'card':
        return _handle_card(response)

    return _handle_text(response)


def _handle_text(response):
    return Intent.Message(
        platform=platform['facebook'],
        text=Intent.Message.Text(text=response.split(','))
    )


def _handle_quick_reply(response):
    obj = json.loads(response)
    return Intent.Message(
        platform=platform['facebook'],
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
        platform=platform['facebook'],
        card=Intent.Message.Card(
            title=obj['title'],
            subtitle=obj['subtitle'],
            image_uri=obj['image_uri'],
            buttons=buttons
        )
    )

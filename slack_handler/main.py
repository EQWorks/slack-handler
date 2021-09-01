import os
from logging import Handler, WARNING, INFO, DEBUG
from time import time
from typing import Callable
import base64
import json

import requests


HOOK = os.getenv('SLACK_WEBHOOK', '')


def get_user(eq_jwt: str) -> dict:
    _, payload, _ = eq_jwt.split('.')
    payload += '=' * ((4 - len(payload) % 4) % 4)  # apply padding ='s
    return json.loads(base64.b64decode(payload))


# WARNING: mutating
def add_user_context(context, user, key):
    if user.get(key):
        context['elements'].append({
            'type': 'mrkdwn',
            'text': f'{key}: {user.get(key)}',
        })


def get_color(levelno: int) -> str:
    if levelno > WARNING:
        return '#f00'  # red
    if levelno == WARNING:
        return '#ff0'  # yellow
    if levelno == INFO:
        return '#0f0'  # green
    if levelno == DEBUG:
        return '#eee'  # gray
    return '#DA70D6'  # some sort of purple


class SlackHandler(Handler):
    """logging.Handler that logs to Slack through an incoming webhook."""

    def __init__(
        self,
        title: str,
        hook: str = HOOK,
        channel: str = None,
        get_color: Callable = get_color,
        eq_jwt: str = None,
        client: requests.Session = requests.Session(),
    ):
        Handler.__init__(self)
        self.title = title
        self.hook = hook
        self.channel = channel
        self.user = get_user(eq_jwt) if eq_jwt else None
        self.get_color = get_color
        self.client = client

    def emit(self, record):
        try:
            stack_trace = self.format(record)
            attachment = {
                'color': self.get_color(record.levelno),
                'blocks': [
                    {
                        'type': 'header',
                        'text': {
                            'type': 'plain_text',
                            'text': f'[{record.levelname}] {self.title}',
                            'emoji': True,
                        },
                    },
                    {
                        'type': 'section',
                        'text': {
                            'type': 'mrkdwn',
                            'text': record.message,
                        },
                    },
                ],
            }

            if record.levelno > WARNING:
                attachment['blocks'] += [
                    {
                        'type': 'section',
                        'text': {
                            'type': 'mrkdwn',
                            'text': f'```{stack_trace}```',
                        },
                    },
                    {'type': 'divider'},
                ]

            trail = record.filename
            if record.funcName != '<module>':
                trail += f'/{record.funcName}'

            if record.levelno <= WARNING:
                trail += f' line {record.lineno}'

            context = {
                'type': 'context',
                'elements': [
                    {
                        'type': 'mrkdwn',
                        'text': '<!date^{0}^{{date_num}} {{time_secs}}|{0}>'.format(int(time())),
                    },
                    {
                        'type': 'plain_text',
                        'text': f':feelsobserve: {trail}',
                        'emoji': True,
                    },
                ],
            }
            # enrich with EQ JWT user info
            if self.user:
                for key in ['email', 'product']:
                    add_user_context(context, self.user, key)

            attachment['blocks'].append(context)

            payload = dict(attachments=[attachment])
            if self.channel:
                payload['channel'] = self.channel

            r = self.client.post(self.hook, json=payload)
            r.raise_for_status()
        except Exception as e:
            self.handleError(e)

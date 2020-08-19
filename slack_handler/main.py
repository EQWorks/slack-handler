import os
from logging import Handler, WARNING, INFO, DEBUG
from time import time
from typing import Callable

import requests


HOOK = os.getenv('SLACK_WEBHOOK', '')


def get_color(levelno: int):
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
    ):
        Handler.__init__(self)
        self.title = title
        self.hook = hook
        self.channel = channel

    def emit(self, record):
        try:
            stack_trace = self.format(record)
            attachment = {
                'color': get_color(record.levelno),
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
            attachment['blocks'].append(context)

            payload = dict(attachments=[attachment])
            if self.channel:
                payload['channel'] = self.channel

            r = requests.post(self.hook, json=payload)
            r.raise_for_status()
        except Exception as e:
            self.handleError(e)

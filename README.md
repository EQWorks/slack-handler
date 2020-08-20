# slack-handler

Slack :tm: handler for the [standard Python logging facility](https://docs.python.org/3/library/logging.html).

## Installation

```shell
% pipenv install git+https://github.com/EQWorks/slack-handler.git@master#egg=slack-handler
% python -m pip install git+https://github.com/EQWorks/slack-handler.git@master#egg=slack-handler
```

Depending on the environment setup, one may need to perform `python3 -m pip` for the `pip` installation option.

## Usage

```python
from logging import getLogger

from slack_handler import SlackHandler

logger = getLogger(__name__)
sh = SlackHandler(
    # required identifier
    title='my awesome app',
    # default to environment variable
    # os.getenv('SLACK_WEBHOOK')
    hook='SLACK_WEBHOOK',
    # optional channel ID to override webhook's default channel
    channel='SLACK_CHANNEL_ID',
    # optional color function, see Customizations section
    get_color='color_function',
)
logger.addHandler(sh)

try:
    1 / 0
except Exception as e:
    logger.exception(e)

try:
    1 + {}
except Exception as e:
    logger.warning(e)
```

![ss](https://user-images.githubusercontent.com/2837532/90812996-f5aee980-e2f4-11ea-966c-dd68bf049e78.png)

## Customizations

logging level dependent colors.

```python
import logging

def custom_colors(levelno: int):
    if levelno > logging.WARNING:
        return '#f00'  # Slack message attachments supported color format

    # any number of different colors based on logging levels

    return '#ccc'  # default color


sh = SlackHandler(
    title='my awesome app with custom colors',
    get_color=custom_colors,
)
```

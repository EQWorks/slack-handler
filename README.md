# slack-handler

Slack :tm: handler for the [standard Python logging facility](https://docs.python.org/3/library/logging.html).

## Installation

```shell
% pipenv install git+https://github.com/EQWorks/slack-handler.git@master
% python -m pip install git+https://github.com/EQWorks/slack-handler.git@master
```

Depending on the environment setup, one may need to perform `python3 -m pip` for the `pip` installation option.

## Usage

```python
from logging import getLogger

from slack_handler import SlackHandler

logger = getLogger(__name__)
sh = SlackHandler(title='my awesome app')
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

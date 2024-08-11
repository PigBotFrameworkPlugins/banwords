import requests
from base64 import b64encode

from pbf.utils import MetaData
from pbf.setup import logger
from pbf.utils.Register import Message
from pbf.controller.Data import Event
from pbf.controller.Client import Msg


banwords_enable_message_handler = True
banwords_server = "https://banwords.xzynb.top"
banwords_user = "root"
banwords_key = "banwords"

meta_data = MetaData(
    name="Banwords",
    version="0.0.1",
    versionCode=1,
    description="A banwords plugin",
    author="XzyStudio",
    license="MIT",
    keywords=["pbf", "plugin", "banwords"],
    readme="""
# Banwords
违禁词检测，使用[Gingmzmzx/Banwords](https://github.com/Gingmzmzx/Banwords)
    """
)


def basic_auth(username, password):
    token = b64encode(f"{username}:{password}".encode('utf-8')).decode("ascii")
    return f'Basic {token}'


class Api:
    @staticmethod
    def check(message: str):  # 可以在其他插件中通过 `pbf.pluginsManager.require("banwords").check()` 调用
        data = requests.get(f"{banwords_server}/check/{message}", headers={ 'Authorization' : basic_auth(banwords_user, banwords_key)})
        try:
            return data.json()
        except Exception:
            return {}


@Message(name="banwords message handler", enabled=banwords_enable_message_handler)
def messageHandler(event: Event):
    logger.info(f"Checking banwords inside the message...")
    logger.debug(Api.check(event.raw_message))
    if Api.check(event.raw_message).get("result"):
        logger.info("Message contains banwords")
        # do something

import logging
from . import ChannelSender

logger = logging.getLogger(__name__)


class StderrSender(ChannelSender):
    @classmethod
    def is_available(cls) -> bool:
        return True

    async def send(self, chat_id: str, text: str) -> None:
        logger.error("[StderrSender] No channel configured. Message lost. chat_id=%s text=%r", chat_id, text)

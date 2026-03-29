from abc import ABC, abstractmethod


class ChannelSender(ABC):
    @abstractmethod
    async def send(self, chat_id: str, text: str) -> None: ...

    @classmethod
    @abstractmethod
    def is_available(cls) -> bool: ...


def get_sender() -> ChannelSender:
    import logging
    from .slack import SlackChannel
    from .chorus import ChorusChannel
    from .stderr import StderrSender
    if SlackChannel.is_available():
        return SlackChannel()
    if ChorusChannel.is_available():
        return ChorusChannel()
    logging.getLogger(__name__).error(
        "SLACK_WEBHOOK_URL and CHORUS_API_KEY are not set. Outbound messages will not be delivered. "
        "Falling back to StderrSender."
    )
    return StderrSender()


def get_background_tasks(queue) -> list:
    import logging
    from .slack import SlackChannel
    from .chorus import ChorusChannel
    tasks = []
    if SlackChannel.is_receiving_available():
        tasks.append(SlackChannel.start_socket_mode(queue))
    if ChorusChannel.is_receiving_available():
        tasks.append(ChorusChannel.start_socket_mode(queue))
    if not tasks:
        logging.getLogger(__name__).error(
            "Neither SLACK_APP_TOKEN nor (CHORUS_API_URL + CHORUS_API_KEY) are set. "
            "Inbound messages will not be received."
        )
    return tasks

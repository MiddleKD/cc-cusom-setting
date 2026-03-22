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
    from .stderr import StderrSender
    if SlackChannel.is_available():
        return SlackChannel()
    logging.getLogger(__name__).error(
        "SLACK_WEBHOOK_URL is not set. Outbound messages will not be delivered. "
        "Falling back to StderrSender."
    )
    return StderrSender()


def get_background_tasks(queue) -> list:
    import logging
    from .slack import SlackChannel
    tasks = []
    if SlackChannel.is_receiving_available():
        tasks.append(SlackChannel.start_socket_mode(queue))
    else:
        logging.getLogger(__name__).error(
            "SLACK_APP_TOKEN is not set. Inbound Slack messages will not be received."
        )
    return tasks

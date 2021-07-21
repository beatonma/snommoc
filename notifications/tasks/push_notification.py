import logging

log = logging.getLogger(__name__)


def push_notification(
    title: str,
    content: str,
    tag: str = "snommoc.org",
    important: bool = False,
):
    try:
        from bmanotify import EventNotifier

    except ImportError:
        log.warning("bmanotify is not available")
        return

    try:
        if important:
            sound = "important"
        else:
            sound = "none"

        EventNotifier(
            title=title,
            body=content,
            tag=tag,
            sound=sound,
            icon="snommoc.org",
            color="#48406e",
        ).send()
    except Exception as e:
        log.warning(f"Failed to push notification: {e}")

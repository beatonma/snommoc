import logging

log = logging.getLogger(__name__)

def push_notification(title: str, content: str, tag: str = 'snommoc.org'):
    try:
        from bmanotify import EventNotifier

    except ImportError:
        log.warning('bmanotify is not available')
        return

    try:
        EventNotifier(
            title=title,
            body=content,
            tag=tag,
        ).send()
    except Exception as e:
        log.warning(f'Failed to push notification: {e}')

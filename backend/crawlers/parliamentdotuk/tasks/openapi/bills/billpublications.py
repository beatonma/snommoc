from typing import Optional

from crawlers.network import JsonResponseCache
from crawlers.parliamentdotuk.tasks.openapi import endpoints, openapi_client
from crawlers.parliamentdotuk.tasks.openapi.bills import schema
from notifications.models import TaskNotification
from repository.models import House
from repository.models.bill import (
    BillPublication,
    BillPublicationLink,
    BillPublicationType,
)


def _update_or_create_bill_type(data: schema.BillPublicationType):
    pub_type, _ = BillPublicationType.objects.update_or_create(
        parliamentdotuk=data.id,
        defaults={
            "name": data.name,
            "description": data.description,
        },
    )
    return pub_type


def _update_bill_publication(
    data: dict,
    notification: Optional[TaskNotification],
    func_kwargs: dict,
):
    """Signature: openapi_client.ItemFunc"""
    api_pub = schema.BillPublication(**data)
    bill_id = func_kwargs["bill_id"]

    house, _ = House.objects.get_or_create(name=api_pub.house.name)
    pub_type = _update_or_create_bill_type(api_pub.publicationType)

    pub, _ = BillPublication.objects.update_or_create(
        parliamentdotuk=api_pub.id,
        bill_id=bill_id,
        defaults={
            "title": api_pub.title,
            "display_date": api_pub.displayDate,
            "publication_type": pub_type,
            "house": house,
        },
    )

    links = api_pub.links
    for link in links:
        BillPublicationLink.objects.update_or_create(
            parliamentdotuk=link.id,
            defaults={
                "publication": pub,
                "title": link.title,
                "url": link.url,
                "content_type": link.contentType,
            },
        )


def fetch_and_update_bill_publications(
    bill_id: int,
    cache: Optional[JsonResponseCache],
    notification: Optional[TaskNotification],
) -> None:
    openapi_client.foreach(
        endpoints.bill_publications(bill_id),
        items_key="publications",
        item_func=_update_bill_publication,
        cache=cache,
        notification=notification,
        func_kwargs={
            "bill_id": bill_id,
        },
    )

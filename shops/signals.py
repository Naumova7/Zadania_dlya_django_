from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Shop


@receiver(post_save, sender=Shop)
def shop_saved(sender, instance, created, **kwargs):
    channel_layer = get_channel_layer()

    async_to_sync(channel_layer.group_send)(
        "shops",
        {
            "type": "shop_updated",
            "shop": {
                "id": instance.id,
                "name": instance.name,
                "description": instance.description,
                "address": instance.address,
                "index": instance.index,
                "is_deleted": instance.is_deleted,
            },
        },
    )

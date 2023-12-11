from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from purchase_order.models import Purchase_order
import purchase_order.helpers as helpers


@receiver([post_save], sender=Purchase_order)
def update_on_time_delivery_rate(sender, instance, **kwargs):
    """
    Update on time delivery rate for vendor.
    when PO status is updated to completed.
    """

    if instance.status == Purchase_order.COMPLETED:
        vendor = instance.vendor
        rate = helpers.calculate_on_time_delivery_rate(instance.vendor)
        vendor.on_time_delivery_rate = rate

        if instance.quality_rating:
            qual_rate = helpers.calculate_quality_rating_average(vendor)
            vendor.quality_rating_avg = qual_rate

        if instance.acknowledgment_date:
            vendor.average_response_time = \
                helpers.calculate_average_response_time(vendor)

        vendor.save()


@receiver([post_delete, post_save], sender=Purchase_order)
def update_fulfilment_rate(sender, instance, **kwargs):
    """
    Update fulfilment rate when data PO status changed.
    """

    vendor = instance.vendor
    vendor.fulfilment_rate = helpers.calculate_fulfilment_rate(vendor)
    vendor.save()

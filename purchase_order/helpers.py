from django.db.models import (Count, Case, F, When,
                              fields, Sum, Avg,
                              ExpressionWrapper)
from django.utils import timezone

from purchase_order.models import Purchase_order


def calculate_on_time_delivery_rate(vendor):
    """
    Calculate the On-Time Delivery Rate for a specific vendor.

    Parameters:
        vendor (Vendor): A Vendor instance for which to
                         calculate the On-Time Delivery Rate.

    Returns:
        float: The On-Time Delivery Rate as a percentage rounded
               to two decimal places.
    """

    completed_orders = vendor.purchase_order_set\
        .filter(status=Purchase_order.COMPLETED)

    if not completed_orders:
        return 0.0

    on_time_delivery_rate = (
        completed_orders.annotate(
            on_time=Case(
                When(delivery_date__lte=F('acknowledgment_date'), then=1),
                default=0,
                output_field=fields.FloatField(),
            )
        ).aggregate(
            total_orders=Count('id'),
            on_time_deliveries=Sum('on_time')
        )
    )

    if not on_time_delivery_rate['total_orders']:
        return 0.0

    on_time_delivery_rate = (
        (on_time_delivery_rate['on_time_deliveries'] /
         on_time_delivery_rate['total_orders']) * 100
    )

    return round(on_time_delivery_rate, 2)


def calculate_quality_rating_average(vendor):
    """
    Calculate the average quality rating for completed
    purchase orders of a specific vendor.

    Parameters:
        vendor (Vendor): A Vendor instance for which to
        calculate the average quality rating.

    Returns:
        float or 0.0: The average quality rating or 0.0 if
        there are no completed orders with quality ratings.
    """

    completed_orders = vendor.purchase_order_set.filter(
        status='completed', quality_rating__isnull=False
    ).only('quality_rating')

    # Return 0.0 if there are no completed orders with quality ratings
    if not completed_orders.exists():
        return 0.0

    # Use aggregation only for the necessary field
    average_quality_rating = completed_orders.aggregate(
        average_rating=Avg('quality_rating'))

    return average_quality_rating['average_rating']


def calculate_average_response_time(vendor):
    """
    Calculate the Average Response Time for completed
    purchase orders of a specific vendor.

    Parameters:
        vendor (Vendor): A Vendor instance for which
        to calculate the Average Response Time.

    Returns:
        float: The Average Response Time in seconds.
    """

    completed_orders = vendor.purchase_order_set.filter(
        acknowledgment_date__isnull=False)

    if not completed_orders.exists():
        # Return 0 if there are no completed orders with acknowledgment dates
        return 0.0

    total_response_time = completed_orders.annotate(
        response_time=ExpressionWrapper(
            F('acknowledgment_date') - F('issue_date'),
            output_field=fields.DurationField()
        )
    ).aggregate(total_time=Sum('response_time'))['total_time']

    if total_response_time is not None:
        total_seconds = total_response_time.total_seconds()
        total_orders = completed_orders.count()
        average_response_time = total_seconds / total_orders
        return average_response_time

    return 0.0


def calculate_fulfilment_rate(vendor):
    """
    Calculate the Fulfilment Rate for a specific vendor.

    Parameters:
        vendor (Vendor): A Vendor instance for which
        to calculate the Fulfilment Rate.

    Returns:
        float: The Fulfilment Rate as a percentage rounded
        to two decimal places.
    """

    total_orders = vendor.purchase_order_set.count()

    # Check if there are no orders issued to the vendor
    # Return 0 if there are no orders
    if total_orders == 0:
        return 0

    fulfilled_orders = vendor.purchase_order_set\
        .filter(status='completed').count()

    fulfilment_rate = (fulfilled_orders / total_orders) * 100

    return round(fulfilment_rate, 2)

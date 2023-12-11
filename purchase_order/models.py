from django.db import models
from django.utils import timezone
from vendor.models import Vendor
# Create your models here.


class Purchase_order(models.Model):
    """
    Purchase Order Table entity.
    """

    PENDING = "PENDING"
    COMPLETED = "COMPLETED"
    CANCELED = "CANCELED"

    STATUS_CHOICES = [
        (PENDING, "PENDING"),
        (COMPLETED, "COMPLETED"),
        (CANCELED, "CANCELED")
    ]

    # Model Help Text
    po_number_help_text = "Unique po number of purhcase order"
    vendor_help_text = "Link to the Vendor model."
    order_date_help_text = "Date when the order was placed."
    delivery_date_help_text = "Expected or actual delivery date of the order."
    items_help_text = "Details of items ordered."
    quantity_help_text = "Total quantity of items in the PO."
    status_help_text = "Current status of the PO (e.g., pending, completed,"\
                       " canceled)."
    quality_rating_help_text = "Rating given to the vendor for this PO"\
                               " (nullable)."
    issue_date_help_text = "Timestamp when the PO was issued to the vendor."
    acknowledgment_date_help_text = "Timestamp when the vendor"\
                                    " acknowledged the PO."

    # Model columns
    po_number = models.CharField(unique=True, max_length=200,
                                 help_text=po_number_help_text)
    vendor = models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True,
                               help_text=vendor_help_text)
    order_date = models.DateTimeField(default=timezone.now,
                                      help_text=order_date_help_text)
    delivery_date = models.DateTimeField(default=timezone.now, 
                                         help_text=delivery_date_help_text)
    items = models.JSONField(help_text=items_help_text)
    quantity = models.PositiveIntegerField(default=0,
                                           help_text=quantity_help_text)
    status = models.CharField(choices=STATUS_CHOICES, max_length=100,
                              default=PENDING, help_text=status_help_text)
    quality_rating = models.FloatField(null=True,
                                       help_text=quality_rating_help_text)
    issue_date = models.DateTimeField(default=timezone.now,
                                      help_text=issue_date_help_text)
    acknowledgment_date = models.DateTimeField(
        default=timezone.now, help_text=acknowledgment_date_help_text)

    def __str__(self):
        """
        Object identify string.
        """

        return f"Order {self.po_number} from vendor {self.vendor.name}"


class HistoricalPerformance(models.Model):
    """
    Store HistoricalPerformance related to vendor.
    """

    # Help Text
    vendor_help_text = "Vendor."
    date_help_text = "Date of the performance record."
    on_time_delivery_rate_help_text = "Historical record of the on-time"\
                                      " delivery rate."
    quality_rating_avg_help_text = "Historical record of the quality rating"\
                                   " average."
    average_response_time_help_text = "Historical record of the average"\
                                      " response time."
    fulfillment_rate_help_text = "Historical record of the fulfilment rate."

    # Fields

    vendor = models.ForeignKey(Vendor, models.SET_NULL, null=True,
                               help_text=vendor_help_text)
    date = models.DateTimeField(default=timezone.now,
                                help_text=date_help_text)
    on_time_delivery_rate = models.FloatField(
        default=0.00, help_text=on_time_delivery_rate_help_text)
    quality_rating_avg = models.FloatField(
        default=0.00, help_text=quality_rating_avg_help_text)
    average_response_time = models.FloatField(
        default=0.00, help_text=average_response_time_help_text)
    fulfillment_rate = models.FloatField(
        default=0.00, help_text=fulfillment_rate_help_text)

    def __str__(self):
        """
        Object identify string.
        """
        return f" Vendor {self.vendor.name} HistoricalPerformance."

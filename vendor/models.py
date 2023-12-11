from django.db import models

# Create your models here.


class Vendor(models.Model):
    """
    Store information related to Vendor
    """

    # Fields Help Text
    contact_details_help_text = "Contact information of the vendor."
    address_help_text = "Physical address of the vendor."
    vendor_code_help_text = "A unique identifier for the vendor."
    on_time_delivery_rate_help_text = "Tracks the percentage of on-time"\
                                      " deliveries."
    quality_rating_avg_help_text = "Average rating of quality based on"\
                                   " purchase orders."
    average_response_time_help_text = "Average time taken to acknowledge"\
                                      " purchase orders."
    fulfillment_rate_help_text = "Percentage of purchase orders fulfilled"\
                                 " successfully."

    # Model Fields
    name = models.CharField(max_length=200, db_index=True,
                            help_text="Vendor's name.")
    contact_details = models.TextField(help_text=contact_details_help_text)
    address = models.TextField(help_text=address_help_text)
    vendor_code = models.CharField(unique=True, db_index=True, max_length=200,
                                   help_text=vendor_code_help_text)
    on_time_delivery_rate = models.FloatField(
        default=0.00, help_text=on_time_delivery_rate_help_text)
    quality_rating_avg = models.FloatField(
        default=0.00, help_text=quality_rating_avg_help_text)
    average_response_time = models.FloatField(
        default=0.00, help_text=average_response_time_help_text)
    fulfillment_rate = models.FloatField(default=0.00,
                                         help_text=fulfillment_rate_help_text)

    def __str__(self):
        """
        Object identify string.
        """
        return f"Vendor : {self.name} code {str(self.vendor_code)}"

from rest_framework import serializers
from purchase_order.models import Purchase_order


class PurchaseOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purchase_order
        fields = '__all__'
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from vendor.models import Vendor
from vendor.api.serializers import VendorSerializer
from purchase_order.helpers import (calculate_average_response_time,
                                    calculate_fulfilment_rate,
                                    calculate_on_time_delivery_rate,
                                    calculate_quality_rating_average)


class VendorViewSet(viewsets.ModelViewSet):
    permission_class = (IsAuthenticated,)
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    lookup_field = 'vendor_code'

    def create(self, request, *args, **kwargs):
        """
        Create new vendor from provided data.

        api: POST /api/vendors/
        """

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=201)

    def update(self, request, *args, **kwargs):
        """
        Update vendor information from provided data.

        api: PUT /api/vendors/{vendor_id}/
        """

        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data,
                                         partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        """
        Delete vendor information from vendor_id.
        """

        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=204)

    @action(detail=True, methods=['get'])
    def performance(self, request, vendor_id=None):
        """
        Retrieve a vendor's performance metrics.

        Parameters:
            request: The HTTP request object.
            vendor_id: The unique identifier of the vendor.

        Returns:
            Response: A JSON response containing the calculated
            performance metrics.
        """

        vendor = self.get_object()
        on_time_delivery_rate = calculate_on_time_delivery_rate(vendor)
        quality_rating_avg = calculate_quality_rating_average(vendor)
        average_response_time = calculate_average_response_time(vendor)
        fulfilment_rate = calculate_fulfilment_rate(vendor)

        performance_metrics = {
            'on_time_delivery_rate': on_time_delivery_rate,
            'quality_rating_avg': quality_rating_avg,
            'average_response_time': average_response_time,
            'fulfilment_rate': fulfilment_rate,
        }

        return Response(performance_metrics)

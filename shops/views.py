import csv
import logging

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from django.http import HttpResponse
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Organization, Shop
from .serializers import OrganizationSerializer, ShopSerializer
from .tasks import send_shop_email

logger = logging.getLogger("shops")

class OrganizationListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        logger.info("GET organizations")
        organizations = Organization.objects.all()
        serializer = OrganizationSerializer(organizations, many=True)
        return Response(serializer.data)

class ShopUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=ShopSerializer)
    def put(self, request, id):
        logger.info(f"PUT shop {id}")
        shop = Shop.objects.get(id=id)

        serializer = ShopSerializer(shop, data=request.data)

        if serializer.is_valid():
            serializer.save()

            channel_layer = get_channel_layer()

            async_to_sync(channel_layer.group_send)(
                "shops",
                {
                    "type": "shop_updated",
                    "shop": serializer.data,
                },
            )

            send_shop_email(serializer.instance.name)

            return Response(serializer.data)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )

class OrganizationShopsFileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        logger.info(f"GET shops file for organization {id}")
        organization = Organization.objects.get(id=id)
        shops = Shop.objects.filter(organization=organization)

        response = HttpResponse(
            content_type="text/csv"
        )
        response["Content-Disposition"] = (
            f'attachment; filename="shops_{id}.csv"'
        )

        writer = csv.writer(response)

        writer.writerow([
            "id",
            "name",
            "description",
            "address",
            "index",
            "is_deleted",
        ])

        for shop in shops:
            writer.writerow([
                shop.id,
                shop.name,
                shop.description,
                shop.address,
                shop.index,
                shop.is_deleted,
            ])

        return response
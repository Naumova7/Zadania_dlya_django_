import csv
import logging

from django.http import HttpResponse
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import Organization, Shop
from .serializers import OrganizationSerializer, ShopSerializer
from .tasks import send_shop_email

logger = logging.getLogger("shops")


class OrganizationListView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Получить список организаций с активными магазинами.",
        responses={
            200: OrganizationSerializer(many=True),
            401: "Authentication credentials were not provided.",
        },
    )
    def get(self, request):
        logger.info("GET organizations")
        organizations = Organization.objects.all()
        serializer = OrganizationSerializer(organizations, many=True)
        return Response(serializer.data)


class ShopUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Обновить магазин.",
        request_body=ShopSerializer,
        responses={
            200: ShopSerializer,
            400: "Invalid data.",
            404: "Shop not found.",
            401: "Authentication credentials were not provided.",
        },
    )
    def put(self, request, id):
        logger.info(f"PUT shop {id}")
        shop = get_object_or_404(Shop, id=id)

        serializer = ShopSerializer(shop, data=request.data)

        if serializer.is_valid():
            serializer.save()

            send_shop_email(serializer.instance.name)

            return Response(serializer.data)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )


class OrganizationShopsFileView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Скачать CSV-файл со всеми магазинами организации.",
        responses={
            200: openapi.Response(
                description="CSV-файл со списком магазинов."
            ),
            404: "Organization not found.",
            401: "Authentication credentials were not provided.",
        },
    )
    def get(self, request, id):
        logger.info(f"GET shops file for organization {id}")
        organization = get_object_or_404(Organization, id=id)
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
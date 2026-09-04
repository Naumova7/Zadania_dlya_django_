from rest_framework import serializers

from .models import Organization, Shop

class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = ["name", "description", "address", "index"]

class OrganizationSerializer(serializers.ModelSerializer):
    shops = serializers.SerializerMethodField()

    class Meta:
        model = Organization
        fields = ["name", "description", "shops"]

    def get_shops(self, organization):
        shops = organization.shops.filter(is_deleted=False)
        return ShopSerializer(shops, many=True).data
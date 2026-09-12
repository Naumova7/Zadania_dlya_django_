from django.urls import path

from .views import (OrganizationListView, ShopUpdateView, OrganizationShopsFileView,)

urlpatterns = [
    path(
        "organizations/",
        OrganizationListView.as_view(),
        name="organizations_list",
    ),
    path(
        "shops/<int:id>/",
        ShopUpdateView.as_view(),
        name="shop_update",
    ),
    path(
        "organizations/<int:id>/shops_file/",
        OrganizationShopsFileView.as_view(),
        name="organization_shops_file",
    ),
]
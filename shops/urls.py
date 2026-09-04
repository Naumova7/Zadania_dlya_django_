from django.urls import path

from .views import (OrganizationListView, ShopUpdateView, OrganizationShopsFileView,)

urlpatterns = [
    path("organizations/", OrganizationListView.as_view()),
    path("shops/<int:id>/", ShopUpdateView.as_view()),
    path("organizations/<int:id>/shops_file/",OrganizationShopsFileView.as_view()),
]
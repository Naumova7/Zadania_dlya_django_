from django.contrib import admin

from .models import Organization, Shop

class ShopInline(admin.TabularInline):
    model = Shop

@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ["name", "description"]
    inlines = [ShopInline]

# Register your models here.

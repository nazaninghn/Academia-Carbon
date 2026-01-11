from django.urls import path
from .views import inventory_preview, inventory_pdf

app_name = 'reporting'

urlpatterns = [
    path("inventory/", inventory_preview, name="inventory"),
    path("inventory.pdf", inventory_pdf, name="inventory_pdf"),
]
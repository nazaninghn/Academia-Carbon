from django.urls import path
from .views import inventory_preview, inventory_pdf

urlpatterns = [
    path("inventory", inventory_preview, name="inventory_preview"),
    path("inventory.pdf", inventory_pdf, name="inventory_pdf"),
]
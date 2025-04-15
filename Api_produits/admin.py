from django.contrib import admin
from .models import Produits

class ProductInfoAdmin(admin.ModelAdmin):
    list_display = ('nom', 'site_marchand', 'prix','indice_ecolo')
    search_fields = ('nom', 'prix')
    list_filter = ('nom',)
# Register your models here.
admin.site.register(Produits,ProductInfoAdmin)
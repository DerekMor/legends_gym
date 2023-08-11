from django.contrib import admin
from .models import Order, OrderLineItem


class OrderLineItemInline(admin.TabularInline):
    model = OrderLineItem
    readonly_fields = ('lineitem_total',)


class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'full_name', 'date', 'order_total')
    list_filter = ('date',)
    inlines = (OrderLineItemInline,)


admin.site.register(Order, OrderAdmin)

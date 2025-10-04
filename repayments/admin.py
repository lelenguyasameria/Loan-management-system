from django.contrib import admin
from .models import Repayment

@admin.register(Repayment)
class RepaymentAdmin(admin.ModelAdmin):
    list_display = ['id', 'loan', 'amount_paid', 'payment_date']
    list_filter = ['payment_date', 'loan__status']
    search_fields = ['loan__user__username', 'loan__id']
    readonly_fields = ['payment_date']

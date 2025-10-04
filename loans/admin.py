from django.contrib import admin
from .models import Loan

@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'amount', 'interest_rate', 'status', 'created_at', 'due_date']
    list_filter = ['status', 'created_at', 'due_date']
    search_fields = ['user__username', 'user__email']
    list_editable = ['status']
    actions = ['approve_loans', 'reject_loans']
    
    def approve_loans(self, request, queryset):
        updated = queryset.update(status='approved')
        self.message_user(request, f'{updated} loan(s) approved successfully.')
    approve_loans.short_description = "Approve selected loans"
    
    def reject_loans(self, request, queryset):
        updated = queryset.update(status='rejected')
        self.message_user(request, f'{updated} loan(s) rejected.')
    reject_loans.short_description = "Reject selected loans"

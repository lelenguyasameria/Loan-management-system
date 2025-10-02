from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum
from datetime import datetime
from decimal import Decimal

from .models import Loan
from .serializers import LoanSerializer
from .permissions import IsLoanOwnerOrAdmin


class LoanViewSet(viewsets.ModelViewSet):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer
    permission_classes = [permissions.IsAuthenticated, IsLoanOwnerOrAdmin]

    def perform_create(self, serializer):
        # user is always the logged-in user
        serializer.save(user=self.request.user)

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Loan.objects.all() 
        return Loan.objects.filter(user=user)

    @action(detail=True, methods=["post"], permission_classes=[permissions.IsAdminUser])
    def approve(self, request, pk=None):
        loan = get_object_or_404(Loan, pk=pk)
        loan.status = "approved"
        loan.save()
        return Response({"status": "loan approved"})


# Web Views for HTML Templates
@login_required
def loan_apply_view(request):
    if request.method == 'POST':
        amount = request.POST.get('amount')
        interest_rate = request.POST.get('interest_rate', 10)
        due_date = request.POST.get('due_date')
        
        try:
            loan = Loan.objects.create(
                user=request.user,
                amount=Decimal(str(amount)),
                interest_rate=Decimal(str(interest_rate)),
                due_date=datetime.strptime(due_date, '%Y-%m-%d').date(),
                status='pending'
            )
            messages.success(request, f'Loan application submitted successfully! Application ID: #{loan.id}')
            return redirect('loan_detail', pk=loan.id)
        except Exception as e:
            messages.error(request, f'Error submitting loan application: {str(e)}')
    
    return render(request, 'loans/apply.html')

@login_required
def loan_list_view(request):
    loans = Loan.objects.filter(user=request.user).order_by('-created_at')
    total_amount = loans.aggregate(Sum('amount'))['amount__sum'] or 0
    
    context = {
        'loans': loans,
        'total_amount': total_amount,
    }
    return render(request, 'loans/list.html', context)

@login_required
def loan_detail_view(request, pk):
    loan = get_object_or_404(Loan, pk=pk, user=request.user)
    repayments = loan.repayments_set.all().order_by('-payment_date')
    
    total_paid = sum(repayment.amount_paid for repayment in repayments)
    remaining_balance = float(loan.amount) - total_paid
    
    context = {
        'loan': loan,
        'repayments': repayments,
        'total_paid': total_paid,
        'remaining_balance': max(0, remaining_balance),
    }
    return render(request, 'loans/detail.html', context)

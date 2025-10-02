from rest_framework import viewsets, permissions
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Sum
from decimal import Decimal
from .models import Repayment
from .serializers import RepaymentSerializer
from loans.models import Loan

class RepaymentViewSet(viewsets.ModelViewSet):
    queryset = Repayment.objects.all()
    serializer_class = RepaymentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # Get loan from request data
        loan_id = self.request.data.get("loan")
        loan = get_object_or_404(Loan, id=loan_id, user=self.request.user)
        serializer.save(loan=loan)

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Repayment.objects.all()
        return Repayment.objects.filter(loan__user=user)
        # Filter repayments to only those related to the user's loans


# Web Views for HTML Templates
@login_required
def repayment_make_view(request, loan_id):
    loan = get_object_or_404(Loan, pk=loan_id, user=request.user)
    
    if loan.status != 'approved':
        messages.error(request, 'You can only make payments on approved loans.')
        return redirect('loan_detail', pk=loan_id)
    
    # Calculate current balance
    total_paid = sum(repayment.amount_paid for repayment in loan.repayments_set.all())
    remaining_balance = loan.amount - total_paid
    
    if remaining_balance <= 0:
        messages.info(request, 'This loan has already been fully repaid.')
        return redirect('loan_detail', pk=loan_id)
    
    if request.method == 'POST':
        amount_paid = request.POST.get('amount_paid')
        payment_method = request.POST.get('payment_method')
        notes = request.POST.get('notes', '')
        
        try:
            amount_paid = Decimal(str(amount_paid))
            if amount_paid <= 0:
                messages.error(request, 'Payment amount must be greater than zero.')
            elif amount_paid > remaining_balance:
                messages.error(request, f'Payment amount cannot exceed remaining balance of ${remaining_balance:.2f}.')
            else:
                repayment = Repayment.objects.create(
                    loan=loan,
                    amount_paid=amount_paid
                )
                
                # Check if loan is fully repaid
                new_total_paid = total_paid + amount_paid
                if new_total_paid >= loan.amount:
                    loan.status = 'repaid'
                    loan.save()
                    messages.success(request, 'Congratulations! Your loan has been fully repaid!')
                else:
                    messages.success(request, f'Payment of ${amount_paid:.2f} processed successfully!')
                
                return redirect('repayment_success', payment_id=repayment.id)
        except ValueError:
            messages.error(request, 'Please enter a valid payment amount.')
        except Exception as e:
            messages.error(request, f'Error processing payment: {str(e)}')
    
    context = {
        'loan': loan,
        'total_paid': total_paid,
        'remaining_balance': remaining_balance,
    }
    return render(request, 'repayments/make_payment.html', context)

@login_required
def repayment_history_view(request):
    repayments = Repayment.objects.filter(loan__user=request.user).order_by('-payment_date')
    
    paginator = Paginator(repayments, 20)  # 20 payments per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    total_amount = repayments.aggregate(Sum('amount_paid'))['amount_paid__sum'] or 0
    active_loans = Loan.objects.filter(user=request.user, status='approved').count()
    recent_payments = repayments[:5]
    
    context = {
        'repayments': page_obj,
        'total_amount': total_amount,
        'active_loans': active_loans,
        'recent_payments': recent_payments,
    }
    return render(request, 'repayments/history.html', context)

@login_required
def repayment_success_view(request, payment_id):
    payment = get_object_or_404(Repayment, pk=payment_id, loan__user=request.user)
    
    # Calculate totals
    total_paid = sum(repayment.amount_paid for repayment in payment.loan.repayments_set.all())
    remaining_balance = float(payment.loan.amount) - total_paid
    
    context = {
        'payment': payment,
        'total_paid': total_paid,
        'remaining_balance': max(0, remaining_balance),
    }
    return render(request, 'repayments/success.html', context)   
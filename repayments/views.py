from rest_framework import viewsets, permissions
from django.shortcuts import get_object_or_404
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
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404

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

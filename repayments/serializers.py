from rest_framework import serializers
from .models import Repayment

class RepaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Repayment
        fields = ['id', 'loan', 'amount_paid', 'payment_date']
        read_only_fields = ['payment_date']
        # Assuming 'loan' is a ForeignKey field in Repayment model          
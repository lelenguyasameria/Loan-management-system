from rest_framework import serializers
from .models import Loan


class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = [
            "id",
            "user",
            "amount",
            "interest_rate",
            "status",
            "created_at",
            "due_date",
        ]
        read_only_fields = ["id", "status", "created_at"]
        extra_kwargs = {
            "user": {"write_only": True},
        }
from django.test import TestCase
from accounts.models import CustomUser
from loans.serializers import LoanSerializer
from datetime import date, timedelta

class LoanSerializerTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username="borrower_serializer",
            password="TestPass123",
            phone_number="0733000000",
            national_id="33333333"
        )

    def test_valid_loan_serializer(self):
        data = {
            "user": self.user.id,
            "amount": "5000.00",
            "interest_rate": "5.0",
            "due_date": (date.today() + timedelta(days=30)).isoformat(),
        }
        serializer = LoanSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_invalid_loan_serializer_missing_field(self):
        data = {
            "user": self.user.id,
            "amount": "5000.00",
            # Missing interest_rate and due_date
        }
        serializer = LoanSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("interest_rate", serializer.errors)
        self.assertIn("due_date", serializer.errors)

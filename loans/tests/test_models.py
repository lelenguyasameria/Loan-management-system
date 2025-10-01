from django.test import TestCase
from django.utils import timezone
from datetime import date, timedelta
from accounts.models import CustomUser
from loans.models import Loan, Repayment

class LoanModelTestCase(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username="borrower1",
            password="TestPass123",
            phone_number="0711111111",
            national_id="11111111"
        )

    def test_create_loan(self):
        loan = Loan.objects.create(
            user=self.user,
            amount=5000.00,
            interest_rate=12.5,
            due_date=date.today() + timedelta(days=30)
        )
        self.assertEqual(loan.user, self.user)
        self.assertEqual(float(loan.amount), 5000.00)
        self.assertEqual(float(loan.interest_rate), 12.5)
        self.assertEqual(loan.status, "pending")

    def test_create_repayment(self):
        loan = Loan.objects.create(
            user=self.user,
            amount=5000.00,
            interest_rate=12.5,
            due_date=date.today() + timedelta(days=30)
        )
        repayment = Repayment.objects.create(
            loan=loan,
            amount_paid=1000.00,
            payment_date=timezone.now()
        )
        self.assertEqual(repayment.loan, loan)
        self.assertEqual(float(repayment.amount_paid), 1000.00)
        self.assertEqual(repayment.loan.user.username, "borrower1")

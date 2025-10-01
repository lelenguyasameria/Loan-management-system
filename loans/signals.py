from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Loan, Repayment
from .services import calculate_total_payable

@receiver(post_save, sender=Loan)
def set_total_amount_on_create(sender, instance, created, **kwargs):
    """
    When a Loan is created, ensure total payable is calculated
    and update the due_date if not set.
    """
    if created:
        total = calculate_total_payable(instance.amount, instance.interest_rate)
        # You could add a field in Loan like total_payable if needed
        print(f"Loan {instance.id} created → Total payable: {total}")


@receiver(post_save, sender=Repayment)
def update_loan_status_after_repayment(sender, instance, created, **kwargs):
    """
    When a repayment is made, check if the loan is fully repaid.
    """
    if created:
        loan = instance.loan
        total_repaid = sum(r.amount_paid for r in loan.repayments.all())

        total_payable = calculate_total_payable(loan.amount, loan.interest_rate)

        if total_repaid >= total_payable:
            loan.status = "repaid"
            loan.save()
            print(f"Loan {loan.id} fully repaid ✅")
        else:
            print(f"Loan {loan.id} repayment made. Total repaid: {total_repaid}/{total_payable}")
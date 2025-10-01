from decimal import Decimal

def calculate_total_payable(amount: Decimal, interest_rate: Decimal) -> Decimal:
    """
    Calculate the total amount payable for a loan based on principal + interest.
    Example: If amount = 1000, interest_rate = 10 → total = 1100
    """
    return amount + (amount * (interest_rate / Decimal("100")))

def generate_repayment_schedule(loan, months: int):
    """
    Generate a repayment schedule (simple fixed installments).
    Returns a list of dicts with month number and installment amount.
    """
    total = calculate_total_payable(loan.amount, loan.interest_rate)
    monthly_payment = total / Decimal(str(months))
    return [{"month": i + 1, "amount": round(monthly_payment, 2)} for i in range(months)]
def is_loan_fully_repaid(loan) -> bool:
    """
    Check if the loan is fully repaid by comparing total repayments to loan amount.
    """
    total_repaid = sum(repayment.amount_paid for repayment in loan.repayments.all())
    return total_repaid >= loan.amount
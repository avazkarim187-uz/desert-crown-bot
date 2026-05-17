"""Pul, son va matn formatlash yordamchilari."""


def format_money(amount: int | float, currency: str = "so'm") -> str:
    """Pul summasini chiroyli ko'rinishga keltirish.

    Misol: 402_750_000 → '402 750 000 so'm'
    """
    if amount is None:
        return "—"
    return f"{int(amount):,}".replace(",", " ") + (f" {currency}" if currency else "")


def format_money_short(amount: int | float) -> str:
    """Qisqartirilgan ko'rinish.

    Misol: 402_750_000 → '402.75 mln so'm'
    """
    if amount is None:
        return "—"
    amount = float(amount)
    if amount >= 1_000_000_000:
        return f"{amount / 1_000_000_000:.2f} mlrd so'm"
    if amount >= 1_000_000:
        return f"{amount / 1_000_000:.1f} mln so'm"
    if amount >= 1_000:
        return f"{amount / 1_000:.0f} ming so'm"
    return f"{amount:.0f} so'm"


def format_area(area: float) -> str:
    """m² ko'rinishida."""
    return f"{area:.1f} m²"


def calculate_monthly_payment_zero_interest(
    price: int, down_payment_percent: int, term_months: int
) -> dict:
    """0% foizsiz nasiya — bo'lib to'lash hisoblanadi.

    Returns:
        dict: down_payment, financed_amount, monthly_payment
    """
    down_payment = int(price * down_payment_percent / 100)
    financed = price - down_payment
    monthly = financed // term_months if term_months > 0 else 0
    return {
        "down_payment": down_payment,
        "financed_amount": financed,
        "monthly_payment": monthly,
        "total_paid": down_payment + (monthly * term_months),
    }


def calculate_monthly_payment_interest(
    price: int, down_payment_percent: int, term_months: int, annual_rate: float
) -> dict:
    """Foizli ipoteka (annuitet formulasi)."""
    down_payment = int(price * down_payment_percent / 100)
    financed = price - down_payment

    if annual_rate == 0:
        monthly = financed // term_months if term_months > 0 else 0
        total_interest = 0
    else:
        monthly_rate = annual_rate / 12 / 100
        # Annuitet
        if monthly_rate > 0:
            monthly = int(
                financed
                * monthly_rate
                * (1 + monthly_rate) ** term_months
                / ((1 + monthly_rate) ** term_months - 1)
            )
        else:
            monthly = financed // term_months
        total_interest = (monthly * term_months) - financed

    return {
        "down_payment": down_payment,
        "financed_amount": financed,
        "monthly_payment": monthly,
        "total_paid": down_payment + (monthly * term_months),
        "total_interest": total_interest,
        "annual_rate": annual_rate,
    }

"""A tiny policy knowledge base + eval cases for the capstone."""
DOCS = {
    "refunds": (
        "Refunds. Customers may request a refund within 30 days of purchase. Digital goods "
        "are refundable only if unopened. Refunds are issued to the original payment method "
        "within 5 business days. Shipping fees are non-refundable."
    ),
    "security": (
        "Security. All data is encrypted in transit and at rest. Passwords must be at least "
        "12 characters. Enable two-factor authentication from Account > Security. Report "
        "incidents to security@example.com within 24 hours."
    ),
    "support": (
        "Support hours are Monday to Friday, 9am to 6pm Pacific. Priority 1 incidents are "
        "acknowledged within 1 hour, around the clock. Use the in-app widget or email "
        "help@example.com."
    ),
}

EVAL_CASES = [
    ("How long do I have to ask for a refund?", "Within 30 days of purchase."),
    ("How are refunds paid back?", "To the original payment method within 5 business days."),
    ("What is the minimum password length?", "At least 12 characters."),
    ("Where do I turn on 2FA?", "Account > Security."),
    ("What are the support hours?", "Monday to Friday, 9am to 6pm Pacific."),
    ("Do you offer a free hardware trial?", "I don't know."),
]

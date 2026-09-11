from llmlab import FakeLLM

def kb_fake():
    """A FakeLLM that answers the capstone KB questions with a citation, else 'I don\'t know'."""
    def responder(messages, **kw):
        raw = messages[-1]["content"]
        user = (raw.split("Q:", 1)[-1] if "Q:" in raw else raw).lower()
        if "paid back" in user or "issued" in user or "payment method" in user:
            return "Refunds go to the original payment method within 5 business days [1]."
        if "refund" in user:
            return "You can request a refund within 30 days of purchase [1]."
        if "password" in user:
            return "Passwords must be at least 12 characters [1]."
        if "2fa" in user or "two-factor" in user:
            return "Turn it on from Account > Security [1]."
        if "support hours" in user:
            return "Monday to Friday, 9am to 6pm Pacific [1]."
        return "I don't know"
    return FakeLLM(responder)

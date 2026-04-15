# =============================================================================
# ADAPTER PATTERN
# Converts the interface of a class into another interface that clients expect.
# Lets incompatible interfaces work together without changing existing code.
# =============================================================================


# =============================================================================
# WITHOUT Adapter — Problem
# A new third-party payment gateway has a different interface than what the
# rest of the system expects. Every call site must be updated to use the
# new interface, and you can't swap providers without touching all callers.
# =============================================================================

class LegacyPaymentProcessor_NoPattern:
    def pay(self, amount: float):
        print(f"[Legacy] Processing payment of ${amount:.2f}")


class StripeGateway_NoPattern:
    def charge(self, cents: int, currency: str):
        print(f"[Stripe] Charging {cents} {currency}")


def without_adapter():
    print("--- WITHOUT Adapter ---")
    legacy = LegacyPaymentProcessor_NoPattern()
    legacy.pay(49.99)

    stripe = StripeGateway_NoPattern()
    # Callers must know Stripe's interface — can't treat them uniformly.
    stripe.charge(4999, "USD")


# =============================================================================
# WITH Adapter — Solution
# The StripeAdapter wraps the incompatible gateway and exposes the unified
# `pay(amount)` interface. Callers only know the target interface.
# =============================================================================

from abc import ABC, abstractmethod


class PaymentProcessor(ABC):
    @abstractmethod
    def pay(self, amount: float):
        pass


class LegacyPaymentProcessor(PaymentProcessor):
    def pay(self, amount: float):
        print(f"[Legacy] Processing payment of ${amount:.2f}")


class StripeGateway:
    """Third-party class we cannot modify."""
    def charge(self, cents: int, currency: str):
        print(f"[Stripe] Charging {cents} {currency}")


class StripeAdapter(PaymentProcessor):
    """Adapts StripeGateway to the PaymentProcessor interface."""
    def __init__(self, gateway: StripeGateway):
        self._gateway = gateway

    def pay(self, amount: float):
        cents = int(amount * 100)
        self._gateway.charge(cents, "USD")


def with_adapter():
    print("\n--- WITH Adapter ---")
    processors: list[PaymentProcessor] = [
        LegacyPaymentProcessor(),
        StripeAdapter(StripeGateway()),
    ]
    # Callers use the uniform `pay` interface regardless of the underlying provider.
    for processor in processors:
        processor.pay(49.99)


if __name__ == "__main__":
    without_adapter()
    with_adapter()

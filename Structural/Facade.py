# =============================================================================
# FACADE PATTERN
# Provides a simplified, unified interface to a complex subsystem.
# Clients talk to the facade instead of a tangle of subsystem classes.
# =============================================================================


# =============================================================================
# WITHOUT Facade — Problem
# To place an order, the client must orchestrate four separate subsystems in
# the correct order, knowing each one's API. Any change to a subsystem
# ripples out to every caller.
# =============================================================================

class InventoryService_NoPattern:
    def check_stock(self, item_id: str) -> bool:
        print(f"[Inventory] Checking stock for {item_id}")
        return True   # assume in stock

class PaymentService_NoPattern:
    def charge(self, account: str, amount: float) -> bool:
        print(f"[Payment] Charging ${amount:.2f} to {account}")
        return True

class ShippingService_NoPattern:
    def schedule(self, item_id: str, address: str):
        print(f"[Shipping] Scheduling delivery of {item_id} to {address}")

class NotificationService_NoPattern:
    def send_confirmation(self, email: str, item_id: str):
        print(f"[Notification] Sending confirmation for {item_id} to {email}")


def without_facade():
    print("--- WITHOUT Facade ---")
    # Client must know all four services and the exact orchestration order.
    inventory    = InventoryService_NoPattern()
    payment      = PaymentService_NoPattern()
    shipping     = ShippingService_NoPattern()
    notification = NotificationService_NoPattern()

    item_id = "ITEM-42"
    if inventory.check_stock(item_id):
        if payment.charge("acc-001", 59.99):
            shipping.schedule(item_id, "123 Main St")
            notification.send_confirmation("user@example.com", item_id)


# =============================================================================
# WITH Facade — Solution
# OrderFacade hides all orchestration behind one simple method.
# Clients call `place_order()` and know nothing about the subsystems.
# =============================================================================

class InventoryService:
    def check_stock(self, item_id: str) -> bool:
        print(f"[Inventory] Checking stock for {item_id}")
        return True

class PaymentService:
    def charge(self, account: str, amount: float) -> bool:
        print(f"[Payment] Charging ${amount:.2f} to {account}")
        return True

class ShippingService:
    def schedule(self, item_id: str, address: str):
        print(f"[Shipping] Scheduling delivery of {item_id} to {address}")

class NotificationService:
    def send_confirmation(self, email: str, item_id: str):
        print(f"[Notification] Sending confirmation for {item_id} to {email}")


class OrderFacade:
    """Single entry point for placing an order."""
    def __init__(self):
        self._inventory    = InventoryService()
        self._payment      = PaymentService()
        self._shipping     = ShippingService()
        self._notification = NotificationService()

    def place_order(self, item_id: str, account: str,
                    amount: float, address: str, email: str) -> bool:
        if not self._inventory.check_stock(item_id):
            print("Order failed: item out of stock.")
            return False
        if not self._payment.charge(account, amount):
            print("Order failed: payment declined.")
            return False
        self._shipping.schedule(item_id, address)
        self._notification.send_confirmation(email, item_id)
        print("Order placed successfully.")
        return True


def with_facade():
    print("\n--- WITH Facade ---")
    facade = OrderFacade()
    facade.place_order(
        item_id="ITEM-42",
        account="acc-001",
        amount=59.99,
        address="123 Main St",
        email="user@example.com",
    )


if __name__ == "__main__":
    without_facade()
    with_facade()

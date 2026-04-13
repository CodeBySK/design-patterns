# =============================================================================
# SINGLETON PATTERN
# Ensures a class has only one instance and provides a global access point.
# =============================================================================


# =============================================================================
# WITHOUT SINGLETON — Problem
# Every call to get the config creates a new object. State is not shared,
# leading to inconsistent config and wasted resources.
# =============================================================================

class DatabaseConfig_NoPattern:
    def __init__(self):
        self.host = "localhost"
        self.port = 5432
        self.name = "mydb"
        print(f"[NoPattern] New DatabaseConfig created at id={id(self)}")


def without_singleton():
    print("--- WITHOUT Singleton ---")
    config1 = DatabaseConfig_NoPattern()
    config2 = DatabaseConfig_NoPattern()

    config1.host = "prod-server"

    # config2 is completely unaware of the change made on config1
    print(f"config1.host = {config1.host}")   # prod-server
    print(f"config2.host = {config2.host}")   # localhost  ← inconsistency
    print(f"Same object? {config1 is config2}")  # False


# =============================================================================
# WITH SINGLETON — Solution
# One shared instance is created on first access and reused thereafter.
# =============================================================================

class DatabaseConfig:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.host = "localhost"
            cls._instance.port = 5432
            cls._instance.name = "mydb"
            print(f"[Singleton] DatabaseConfig created at id={id(cls._instance)}")
        return cls._instance


def with_singleton():
    print("\n--- WITH Singleton ---")
    config1 = DatabaseConfig()
    config2 = DatabaseConfig()

    config1.host = "prod-server"

    # config2 reflects the same state because it IS config1
    print(f"config1.host = {config1.host}")   # prod-server
    print(f"config2.host = {config2.host}")   # prod-server ← consistent
    print(f"Same object? {config1 is config2}")  # True


if __name__ == "__main__":
    without_singleton()
    with_singleton()

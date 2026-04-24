# =============================================================================
# PROXY PATTERN
# Provides a surrogate or placeholder for another object to control access,
# add lazy initialization, caching, logging, or access control.
# =============================================================================


# =============================================================================
# WITHOUT Proxy — Problem
# The expensive database query runs on every call, even for repeated lookups
# of the same data. There is no caching, no access control, and no logging
# — all concerns that would have to be duplicated at every call site.
# =============================================================================

class UserRepository_NoPattern:
    def get_user(self, user_id: int) -> dict:
        print(f"[DB] Executing expensive query for user {user_id} ...")
        return {"id": user_id, "name": f"User_{user_id}", "role": "member"}


def without_proxy():
    print("--- WITHOUT Proxy ---")
    repo = UserRepository_NoPattern()

    # Same user fetched twice — hits the database both times.
    print(repo.get_user(1))
    print(repo.get_user(1))
    print(repo.get_user(2))


# =============================================================================
# WITH Proxy — Solution
# CachingProxy sits in front of the real repository and intercepts calls.
# It adds caching transparently; callers use the same interface and are
# completely unaware that a proxy is in the way.
# =============================================================================

from abc import ABC, abstractmethod


class IUserRepository(ABC):
    @abstractmethod
    def get_user(self, user_id: int) -> dict: pass


class UserRepository(IUserRepository):
    """Real subject — performs the actual database query."""
    def get_user(self, user_id: int) -> dict:
        print(f"[DB] Executing expensive query for user {user_id} ...")
        return {"id": user_id, "name": f"User_{user_id}", "role": "member"}


class CachingProxy(IUserRepository):
    """Proxy — adds caching and logging without changing the real subject."""
    def __init__(self, repository: IUserRepository):
        self._repository = repository
        self._cache: dict[int, dict] = {}

    def get_user(self, user_id: int) -> dict:
        if user_id in self._cache:
            print(f"[Cache] Returning cached result for user {user_id}")
            return self._cache[user_id]
        print(f"[Proxy] Cache miss — delegating to real repository")
        result = self._repository.get_user(user_id)
        self._cache[user_id] = result
        return result


def with_proxy():
    print("\n--- WITH Proxy ---")
    repo: IUserRepository = CachingProxy(UserRepository())

    # First call hits the DB; subsequent calls for the same ID are cached.
    print(repo.get_user(1))
    print(repo.get_user(1))   # served from cache
    print(repo.get_user(2))
    print(repo.get_user(2))   # served from cache


if __name__ == "__main__":
    without_proxy()
    with_proxy()

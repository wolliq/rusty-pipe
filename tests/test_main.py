from src.main import get_greeting


def test_get_greeting() -> None:
    """Test the get_greeting function."""
    assert get_greeting("Alice") == "Hello, Alice!"
    assert get_greeting("Bob") == "Hello, Bob!"

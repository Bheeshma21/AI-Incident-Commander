from app.checkout import process_checkout


def test_checkout_success():
    result = process_checkout("user-123", "order-456")

    assert result["status"] == "success"
    assert result["user_id"] == "user-123"
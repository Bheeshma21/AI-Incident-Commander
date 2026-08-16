from .db import get_connection


def process_checkout(user_id, order_id):
    connection = get_connection()

    try:
        result = connection.execute(
            f"SELECT * FROM orders WHERE id = '{order_id}'"
        )

        return {
            "status": "success",
            "user_id": user_id,
            "order": result,
        }

    except Exception as error:
        return {
            "status": "error",
            "message": str(error),
        }

    finally:
        connection.close()
class DatabaseConnection:
    def __init__(self):
        self.connected = True

    def execute(self, query):
        if not self.connected:
            raise RuntimeError("Database connection is closed")

        return {"status": "success", "query": query}

    def close(self):
        self.connected = False


def get_connection():
    return DatabaseConnection()
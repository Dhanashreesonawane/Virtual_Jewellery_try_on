class AppError(Exception):
    """Expected, user-facing failure. Becomes the JSON error envelope."""
    def __init__(self, code: str, message: str, status: int = 400):
        self.code, self.message, self.status = code, message, status


def ok(data):
    return {"success": True, "data": data, "error": None}


def fail(code: str, message: str):
    return {"success": False, "data": None, "error": {"code": code, "message": message}}

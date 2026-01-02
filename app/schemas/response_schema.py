class AppResponse:
    def __init__(self, status: int, data: object = None, message: str =None):
        self.status = status
        self.data = data
        self.message = message

    def to_dict(self):
        return {
            "status": self.status,
            "data": self.data,
            "message": self.message,
        }
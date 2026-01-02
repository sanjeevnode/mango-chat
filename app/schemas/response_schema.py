from fastapi.responses import JSONResponse


class AppResponse:
    def __init__(self, status: int, data: object = None, message: str = None):
        self.status = status
        self.data = data
        self.message = message

    def send(self):
        return JSONResponse(
            status_code=self.status,
            content={
                "status": self.status,
                "data": self.data,
                "message": self.message,
            }
        )
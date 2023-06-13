from typing import Any, Dict


class Result:
    def __init__(self, code: int, msg: str, data: Any = None):
        self.code = code
        self.msg = msg
        self.data = data

    def build(self) -> Dict:
        if self.data is None:
            return {"code": self.code, "msg": self.msg}

        return {"code": self.code, "msg": self.msg, "data": self.data}


def OK(data: Any = None):
    return Result(200, "OK", data).build()


def Created(data: Any = None):
    return Result(201, "Created", data).build()


def Err(code: int, msg: str, data: Any = None):
    return Result(code, msg, data).build()


def InternalErr():
    return Result(500, "Internal Error").build()

def BadInput(field: dict):
    resp = {"code": 422, "msg": "Unprocessable Entity", "errors": field}
    return resp


from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

def validation_body_exception_handler(app: FastAPI) -> callable:
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        try:    
            raw_err = exc.raw_errors
            error_wrapper = raw_err[0]
            validation_error = error_wrapper.exc

            overwritten_errors = validation_error.errors()

            resp = {
                "code": 422,
                "msg": "Unprocessable Entity",
                "errors": {}
            }

            for e in overwritten_errors:
                resp["errors"][e['loc'][0]] = e['msg']

            return JSONResponse(status_code=422, content=jsonable_encoder(resp))        
        except AttributeError:
            resp = {
                "code": 422,
                "msg": "Please fill all the field",
            }

            return JSONResponse(status_code=422, content=jsonable_encoder(resp))        

    
    return validation_exception_handler

def http_customize_handler(app: FastAPI) -> callable:
    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        resp = {
            "code": exc.status_code,
            "msg": exc.detail
        }

        return JSONResponse(status_code=exc.status_code, content=jsonable_encoder(resp))
    
    return http_exception_handler
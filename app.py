from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI



@app.route("/")
def get():
    return JSONResponse(
        {
            "data" : "hello world"
        }
    )

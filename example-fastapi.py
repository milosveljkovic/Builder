import numbers
from fastapi import FastAPI
import uvicorn
import os


app = FastAPI()


@app.get("/")
def read_root():
    target = os.environ.get("TARGET", "World")
    return "This is function deployed by builder!"


@app.get("/other_route")
def read_root():
    return "WOW! This is a new ROUTE!"


if __name__ == "__main__":
    uvicorn.run(app, debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

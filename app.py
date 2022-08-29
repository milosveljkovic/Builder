from re import sub
from typing import Union
from fastapi import FastAPI, status, HTTPException
import uvicorn
import os
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import subprocess
import time


class ServerlessFunction(BaseModel):
    name: str
    description: str
    code: str
    version: str


class FunctionDefinision(BaseModel):
    message: str
    access_point: str


app = FastAPI()


@app.get("/")
def read_root():
    subprocess.check_call(["ls"])
    return "Hello"


@app.get("/kubeinfo")
def getKubeInfo():
    kubeconfig = os.environ.get("KUBECONFIG")
    if kubeconfig is None:
        raise HTTPException(
            status_code=status.HTTP_424_FAILED_DEPENDENCY,
            detail="Kubeconfig is not specified",
        )
    subprocess.check_call(["kubectl", "config", "get-contexts"])
    return "Hello {}!\n".format(kubeconfig)


@app.post("/code")
def depoloyFuntion(ServerlessFunction: ServerlessFunction):

    subprocess.check_call(
        [
            "buildah",
            "login",
            "-u",
            os.environ.get("USERNAME"),
            "-p",
            os.environ.get("PASSWORD"),
            "docker.io",
        ]
    )

    app_py = open("./app/app.py", "x")
    app_py.write(ServerlessFunction.code)
    app_py.close()

    subprocess.check_call(
        [
            "buildah",
            "bud",
            "-t",
            "docker.io/{}/{}:{}".format(
                os.environ.get("USERNAME"),
                ServerlessFunction.name,
                ServerlessFunction.version,
            ),
            "./app/Dockerfile",
        ]
    )
    print(
        "Function {}:{} haas been successfully built".format(
            ServerlessFunction.name, ServerlessFunction.version
        )
    )

    subprocess.check_call(
        [
            "buildah",
            "push",
            "docker.io/{}/{}:{}".format(
                os.environ.get("USERNAME"),
                ServerlessFunction.name,
                ServerlessFunction.version,
            ),
        ]
    )
    print(
        "Function docker.io/{}/{}:{} haas been successfully pushed to registry.".format(
            os.environ.get("USERNAME"),
            ServerlessFunction.name,
            ServerlessFunction.version,
        )
    )

    generateTempFile(ServerlessFunction)
    deployFunction()
    cleanUp()
    msg = "Function {}:{} haas been successfully deployed".format(
        ServerlessFunction.name, ServerlessFunction.version
    )
    address = getFunctionDefinision(ServerlessFunction)
    return {"msg": msg, "address": address}


def getFunctionDefinision(ServerlessFunction: ServerlessFunction):
    print("Waiting for resources to become available in k8s...")
    time.sleep(5)
    address = subprocess.run(
        [
            "kubectl",
            "get",
            "ksvc",
            ServerlessFunction.name,
            "--output=custom-columns=NAME:.metadata.name,URL:.status.url",
            "-o=jsonpath='{.status.url}'",
        ],
        capture_output=True,
        text=True,
    )
    return address.stdout.replace("'", "")


def generateTempFile(ServerlessFunction: ServerlessFunction):
    os.popen(
        "cp ./app/service.yaml ./app/service-temp.yaml"
    )
    time.sleep(1)
    subprocess.check_call(
        [
            "sed",
            "-i",
            "s/<function_name>/{}/g".format(ServerlessFunction.name),
            "./app/service-temp.yaml",
        ]
    )
    subprocess.check_call(
        [
            "sed",
            "-i",
            "s/<registry>/{}/g".format(os.environ.get("USERNAME")),
            "./app/service-temp.yaml",
        ]
    )
    subprocess.check_call(
        [
            "sed",
            "-i",
            "s/<version>/{}/g".format(ServerlessFunction.version),
            "./app/service-temp.yaml",
        ]
    )


def deployFunction():
    subprocess.check_call(
        [
            "kubectl",
            "apply",
            "-f",
            "./app/service-temp.yaml",
        ]
    )


def cleanUp():
    os.remove("./app/service-temp.yaml")
    os.remove("./app/app.py")


if __name__ == "__main__":
    uvicorn.run(app, debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

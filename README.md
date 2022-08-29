# Builder

This service has been tested on linux (Fedora)

## Prerequisite

- kubectl
- minicube with Knative (follow this guide - https://knative.dev/docs/getting-started/)
- buildah (instll buildah using $sudo dnf -y install buildah )
- sed
- python3

## What should be done before running a service

export USERNAME='registry-username'
export PASSWORD='registry-password'
export KUBECONFIG='path/to/kubernetes/with/knative' (please check context!!!)

## Getting started

1. Clone repo
2. $cd Builder
3. python3 -m venv
4. source ./bin/activate
5. pip install -r requirements
6. run app.js 

Builder should be up & running on http://0.0.0.0:8080/docs#/ .

There is a few REST endpoints defined. For us, most interesting is POST /code.

Get the body from example-code-body.json and put it in body of POST /code in swagger. Execute!

After less then 2-3 mins, your app defined in "code" section of body will be deployed in k8s.

As a result of POST /code you'll get an object with address propery, use that address to access deployed service (address/docs) .
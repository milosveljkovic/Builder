# Builder
This platform should provide deployment of python services to k8s with `ZERO` effort. 

![image](https://user-images.githubusercontent.com/47954575/187308883-273f5b89-fb40-44b5-a011-a5651b8138c1.png)

#### What this service does:
1. Pack your service in Docker and built it using buildah library
2. Push the image to registry
3. Deploy Knative Service in k8s
4. You get address of deployed service so you can access it easily
5. Knative enables routing, autoscaling, revisioning..

## Prerequisite

- kubectl
- minicube with Knative (follow this guide - https://knative.dev/docs/getting-started/) 
- buildah (instll buildah using $sudo dnf -y install buildah )
- sed
- python3

`minikube start -p knative`

`minikube tunnel --profile knative`

## What should be done before running a Builder

```sh
export USERNAME='registry-username'
export PASSWORD='registry-password'
export KUBECONFIG='path/to/kubernetes/with/knative' (please check context!!!)
```

## Getting started

1. clone repo
2. $cd Builder
3. python3 -m venv
4. source ./bin/activate
5. pip install -r requirements
6. run app.js 

Builder should be up & running on http://0.0.0.0:8080/docs#/ .

There is a few REST endpoints defined. For us, most interesting is `POST /code`.

Get the body from _example-code-body.json_ and put it in body of `POST /code` in _swagger_. Execute !!!

After less then ~2-3 mins, your app defined in "code" section of body will be deployed in k8s.

As a result of `POST /code` you'll get an object with `address` propery, use that address to access deployed service (address/docs) .


This service has been tested on linux (Fedora)

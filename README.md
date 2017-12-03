# Docker CMS

This is a submission for the second Cloud Computing module assignment for DT228/3

Student: Robert Vaughan - C15341261

## Q1

```
docker swarm init
```
As we can see from the above command, a docker swarm is itialised. This will allow for nodes to join the manager of a swarm and carry out the same tasks assigned to the manager

```
docker swarm join [OPTIONS] HOST:PORT
```
The above command allows a worker node to join the swarm

## Q2

Question 2 required a student to build a Docker CMS with various endpoints to configure the docker service. We shall go through each one given and describe how a solution to each endpoint is achieved

### GET /containers
Returns JSON data for all the containers in the CMS.

Command: docker ps -a

### GET /containers?state=running
Returns JSON data for all of the running containers in the CMS.

Command: docker ps

### GET /containers/<id>
Returns JSON data for a specific container

Command: docker inspect CONTAINER_ID

### GET /containers/<id>/logs
Returns log data for a specific container. The data is given in a JSON format

Command: docker logs CONTAINER_ID

### GET /services
Returns a JSON list of all services in the CMS

Command: docker service ls

### GET /nodes
Returns a JSON list of all nodes and their details

Command: docker node ls

### GET /images
Returns a list of all images

Command: docker images

### PATCH /images/<id>

Endpoint to change an images tag

Command docker tag IMAGE NEW_TAG

### PATCH /containers/<id>
Command: docker STATUS CONTAINER_ID

### POST /images
Creates an image via a Dockerfile

Command: docker build -t custom .

### POST /containers
Creates an instance (container) of an image

Command: docker run -d image

### DELETE /containers/<id>
Deletes a container

Command: docker rm CONTAINER

### DELETE /containers
Deletes ALL containers

Commands 
docker ps
docker stop CONTAINER
docker rm CONTAINER

### DELETE /images/<id>
Deletes and image within the CMS

Command: docker image rm IMAGE

### DELETE /images
Deletes ALL images within the CMS

Commands
docker images
docker image rm IMAGE

## Q3
```
docker service create --replicas 3 -p 80:80 --name webservice nginx
```
The above command create an NGINX service with the use of the webport (80). This nginx image allows one to deploy the web server service within containers. When the service is lauched, if one goes to the IP of one of the nodes, they will see the default NGINX page

## Q4
For this question, one was required to run a local test script on their machine to test each endpoint. This test script is examined in the You Tube video and is hosted on this repo

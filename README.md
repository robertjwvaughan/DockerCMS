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
### GET /containers?state=running
### GET /containers/<id>
### GET /containers/<id>/logs
### GET /services
### GET /nodes
### GET /images
### PATCH /images/<id>
### PATCH /containers/<id>

## Q3

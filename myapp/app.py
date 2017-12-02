from flask import Flask, Response, render_template, request
import json
from subprocess import Popen, PIPE
import os
from tempfile import mkdtemp
from werkzeug import secure_filename

app = Flask(__name__)

@app.route("/")
def index():
        return """
        Available API endpoints:

        GET /containers                     List all containers
        GET /containers?state=running      List running containers (only)
        GET /containers/<id>                Inspect a specific container
        GET /containers/<id>/logs           Dump specific container logs
        GET /images                         List all images


        POST /images                        Create a new image
        POST /containers                    Create a new container

        PATCH /containers/<id>              Change a container's state
        PATCH /images/<id>                  Change a specific image's attributes

        DELETE /containers/<id>             Delete a specific container
        DELETE /containers                  Delete all containers (including running)
        DELETE /images/<id>                 Delete a specific image
        DELETE /images                      Delete all images

        """

@app.route('/containers', methods=['GET'])
def containers_index():
    if request.args.get('state') == 'running': 
        output = docker('ps')
        resp = json.dumps(docker_ps_to_array(output))

    else:
        output = docker('ps', '-a')
        resp = json.dumps(docker_ps_to_array(output))

    return Response(response=resp, mimetype="application/json")

@app.route('/containers/<id>', methods=['GET'])
def containers_show(id):
    output = docker("inspect", str(id))

    return Response(response=output, mimetype="application/json")

@app.route('/containers/<id>/logs', methods=['GET'])
def containers_logs(id):
    output = docker("logs", str(id))
    resp = json.dumps(docker_logs_to_object(str(id), output))

    return Response(response=resp, mimetype="application/json")

@app.route('/images', methods=['GET'])
def images_index():
    output = docker('images')
    resp = json.dumps(docker_images_to_array(output))

    return Response(response=resp, mimetype="application/json")

@app.route('/nodes', methods=['GET'])
def nodes():
    output = docker('node', 'ls')
    resp = json.dumps(docker_node_to_array(output))
    
    return Response(response=resp, mimetype="application/json")

@app.route('/service', methods=['GET'])
def service():
    output = docker('service', 'ls')
    resp = json.dumps(docker_service_to_array(output))

    return Response(response=resp, mimetype="application/json")

@app.route('/containers', methods=['POST'])
def create_container():
    # https://stackoverflow.com/questions/20001229/how-to-get-posted-json-in-flask
    
    json_request = request.get_json(force=True)
    image = json_request['image']
    
    output = docker('run', '-d', image)
    resp = '{id: "' + output + '"}'

    return Response(response=resp, mimetype="application/json")

@app.route('/images', methods=['POST'])
def images_create():
    """
    Create image (from uploaded Dockerfile)

    curl -H 'Accept: application/json' -F file=@Dockerfile http://localhost:8080/images

    """
    request_file = request.files['file']
    request_file.save('DockerfileUpload')

    docker('build', '-t', 'custom', '.')
    images = docker('images')
    resp  = json.dumps(docker_images_to_array(images))

    return Response(response=resp, mimetype="application/json")

@app.route('/containers/<id>', methods=['PATCH'])
def patch_container(id):
    json_request = request.get_json(force=True)
    state = json_request['state']

    if state == 'stopped':
        docker('stop', str(id))
        resp = '{id: "' + str(id) + '", status: "stopped"}'
    elif state == 'running':
        docker('restart', str(id))
        resp = '{id: "' + str(id) + '", status: "running"}'

    return Response(response=resp, mimetype="application/json")

@app.route('/images/<id>', methods=['PATCH'])
def images_update(id):
    json_request = request.get_json(force=True)
    tag = json_request['tag']

    docker('tag', str(id), tag)
    resp = '{id: "' + str(id) + '", tag:"' + str(tag) + '"}'

    return Response(response=resp, mimetype="application/json")

@app.route('/images', methods=['DELETE'])
def images_remove_all():
    output = docker('images')
    json_data = docker_images_to_array(output)
    
    for obj in json_data:
        if obj['name'] != 'cms':
            docker('rmi', obj['name'])

    resp = '{status: "completed"}'
    return Response(response=resp, mimetype="application/json")

@app.route('/images/<id>', methods=['DELETE'])
def images_remove(id):
    #https://www.digitalocean.com/community/tutorials/how-to-remove-docker-images-containers-and-volumes
    
    docker('rmi', str(id))
    resp = '{id: ' + str(id) + ', status: Deleted}'
    return Response(response=resp, mimetype="application/json")

@app.route('/containers', methods=['DELETE'])
def containers_remove_all():
    output = docker('ps', '-a')
    json_data = docker_images_to_array(output)

    for obj in json_data:
        if obj['image'] != 'cms':
            docker('stop', str(obj['id']))
            docker('rm', str(obj['id']))

    resp = '{status: "completed"}'
    return Response(response=resp, mimetype="application/json")

@app.route('/containers/<id>', methods=['DELETE'])
def containers_remove(id):

    docker ('rm', str(id))
    resp = '{id: ' + str(id) + ', status: Deleted}'
    return Response(response=resp, mimetype="application/json")

def docker(*args):
    cmd = ['docker']
    for sub in args:
        cmd.append(sub)
    process = Popen(cmd, stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate()
    error = stderr.decode('utf-8')
    out = stdout.decode('utf-8')
    if error.startswith('Error'):
        print ('Error: {0} -> {1}'.format(' '.join(cmd), stderr))
    return error + out

def docker_ps_to_array(output):
    all = []
    for c in [line.split() for line in output.splitlines()[1:]]:
        each = {}
        each['id'] = c[0]
        each['image'] = c[1]
        each['name'] = c[-1]
        each['ports'] = c[-2]
        all.append(each)
    return all

def docker_images_to_array(output):
    all = []
    for c in [line.split() for line in output.splitlines()[1:]]:
        each = {}
        each['id'] = c[2]
        each['tag'] = c[1]
        each['name'] = c[0]
        all.append(each)
    return all

def docker_logs_to_object(id, output):
    logs = {}
    logs['id'] = id
    all = []
    for line in output.splitlines():
        all.append(line)
    logs['logs'] = all
    return logs

def docker_node_to_array(output):
    all = []
    for c in [line.split() for line in output.splitlines()[1:]]:
        each = {}
        each['id'] = c[0]
        each['hostname'] = c[1]
        each['status'] = c[2]
        each['availability'] = c[3]
        all.append(each)
    return all

def docker_service_to_array(output):
    all = []
    for c in [line.split() for line in output.splitlines()[1:]]:
        each = {}
        each['id'] = c[0]
        each['name'] = c[1]
        each['mode'] = c[2]
        each['replicas'] = c[3]
        each['image'] = c[4]
        each['ports'] = c[5]
        all.append(each)
    return all

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=8080, debug=True)

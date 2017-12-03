from subprocess import Popen, PIPE
import json

def curl_call(cmd):
	process = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
	stdout, stderr = process.communicate()
	error = stderr.decode('utf-8')
	out = stdout.decode('utf-8')
	return out

def list_container(ip):
	out = curl_call("curl -s -X GET -H 'Accept: application/json' http://"+ip+"/containers | python3 -mjson.tool") 
	if out != "":
		#coverts output into python object
		resp = json.loads(out)
		for line in resp:
			print(line)

def list_running_container(ip):
	out = curl_call("curl -s -X GET -H 'Accept: application/json' http://"+ip+"/containers?state=running | python3 -mjson.tool") 
	if out != "":
		#coverts output into python object
		resp = json.loads(out)
		for line in resp:
			print(line)

def list_specific_container(ip, id):
	out = curl_call("curl -s -X GET -H 'Accept: application/json' http://"+ip+"/containers/"+str(id)+" | python3 -mjson.tool") 
	if out != "":
		#coverts output into python object
		resp = json.loads(out)
		print(out)

def list_specific_container_logs(ip, id):
	out = curl_call("curl -s -X GET -H 'Accept: application/json' http://"+ip+"/containers/"+str(id)+"/logs | python3 -mjson.tool") 
	if out != "":
		#coverts output into python object
		resp = json.loads(out)
		print(json.dumps(resp))

def list_images(ip):
	out = curl_call("curl -s -X GET -H 'Accept: application/json' http://"+ip+"/images | python3 -mjson.tool") 
	if out != "":
		#coverts output into python object
		resp = json.loads(out)
		for line in resp:
			print(line)

def list_nodes(ip):
	out = curl_call("curl -s -X GET -H 'Accept: application/json' http://"+ip+"/nodes | python3 -mjson.tool") 
	if out != "":
		#coverts output into python object
		print(out)

def list_services(ip):
	out = curl_call("curl -s -X GET -H 'Accept: application/json' http://"+ip+"/service | python3 -mjson.tool") 
	if out != "":
		#coverts output into python object
		print(out)

def post_container(ip, name):
	json_data = '{"image": "'+name+'"}'
	cmd = "curl -X POST -H 'Content-Type: application/json' http://"+ip+"/containers -d '" + json_data + "'"
	out = curl_call(cmd) 
	if out != "":
		print(out)

def post_image(ip):
	cmd = "curl -X POST -H 'Accept: application/json' -F file=@Dockerfile http://"+ip+"/images"
	out = curl_call(cmd)
	if out != "":
		print(out)

def patch_container(ip, status, id):
	json_data = '{"state": "'+status+'"}'
	cmd = "curl -X PATCH -H 'Content-Type: application/json' http://"+ip+"/containers/" + str(id) + " -d '" + json_data + "'"
	out = curl_call(cmd) 
	if out != "":
		print(out)

def patch_image(ip, tag, id):
	json_data = '{"tag": "'+tag+'"}'
	cmd = "curl -X PATCH -H 'Content-Type: application/json' http://"+ip+"/images/" + str(id) + " -d '" + json_data + "'"
	out = curl_call(cmd) 
	if out != "":
		print(out)

def delete_container(ip, id):
	cmd = "curl -s -X DELETE -H 'Accept: application/json' http://"+ip+"/containers/" + str(id) + ""
	out = curl_call(cmd) 
	if out != "":
		print(out)

def delete_containers(ip):
	cmd = "curl -s -X DELETE -H 'Accept: application/json' http://"+ip+"/containers"
	out = curl_call(cmd) 
	if out != "":
		print(out)

def delete_image(ip, id):
	cmd = "curl -s -X DELETE -H 'Accept: application/json' http://"+ip+"/images/" + str(id) + ""
	out = curl_call(cmd) 
	if out != "":
		print(out)

def delete_images(ip):
	cmd = "curl -s -X DELETE -H 'Accept: application/json' http://"+ip+"/containers"
	out = curl_call(cmd) 
	if out != "":
		print(out)

if __name__ == "__main__":

	ip = input("What is your IP\n")

	print("List all containers\n")
	list_container(ip)
	print("\n")

	input("\nNEXT\n")

	print("List all RUNNING containers\n")
	list_running_container(ip)
	print("\n")

	input("\nNEXT\n")

	print("List SPECIFIC container\n")
	id = input("Give container ID:\n")
	list_specific_container(ip, id)
	print("\n")

	input("\nNEXT\n")

	print("List SPECIFIC container LOGS\n")
	id = input("Give container ID:\n")
	list_specific_container_logs(ip, id)
	print("\n")

	input("\nNEXT\n")

	print("List all images\n")
	list_images(ip)
	print("\n")

	input("\nNEXT\n")

	print("List swarm nodes\n")
	list_nodes(ip)
	print("\n")

	input("\nNEXT\n")

	print("List all services\n")
	list_services(ip)

	input("\nNEXT\n")

	print("Create image\n")
	post_image(ip)
	print("\n")

	input("\nNEXT\n")

	print("Create container\n")
	list_images(ip)
	name = input("Give image name:\n")
	post_container(ip, name)
	list_container(ip)
	print("\n")
	
	input("\nNEXT\n")

	print("Patch Container\n")
	list_container(ip)
	state = input("Enter: running or stopped\n")
	id = input("Enter ID\n")
	patch_container(ip, state, id)
	print("\n")

	input("\nNEXT\n")

	print("Patch Image\n")
	list_images(ip)
	tag = input("Enter tag\n")
	id = input("Enter ID\n")
	patch_image(ip, tag, id)
	print("\n")

	input("\nNEXT\n")

	print("Delete Container\n")
	list_container(ip)
	id = input("Enter ID\n")
	delete_container(ip, id)
	print("\n")

	input("\nNEXT\n")

	print("Delete ALL Containers\n")
	list_container(ip)
	delete_containers(ip)
	list_container(ip)
	print("\n")

	input("\nNEXT\n")

	print("Delete an Image\n")
	list_images(ip)
	id = input("Enter Name\n")
	delete_image(ip, id)
	print("\n")

	input("\nNEXT\n")

	print("Delete ALL Images\n")

	list_images(ip)
	delete_images(ip)
	print("\n")
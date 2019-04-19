import docker
import socket
from contextlib import closing
import requests
import time

# Test CUI based applications
def runCUI(image, tests, path):
    client = docker.from_env()
    image = client.images.pull(image,'latest')
    for test in range(len(tests)):
        print("Running ",tests[test]["i"],"....")
        container = client.containers.run(image,[tests[test]["i"]], volumes={path: {'bind': '/mnt/tests', 'mode': 'ro'}}, remove=True)
        real = container.decode("utf-8").rstrip()
        expected = open(tests[test]["o"]).read().rstrip()
        if(real == expected):
            tests[test]["r"] = "Success"
        else:
            tests[test]["r"] = "Fail"
    print(tests)
    return tests

#Get Endpoint for WebUI and REST API
def getEP(image, config, path):
    print('running container')
    client = docker.from_env()
    image = client.images.pull(image+':latest')
    if(path == ''):
        container = client.containers.run(image, ports={str(config["port"]): (config['host'],None)}, detach=True)
    else:
        container = client.containers.run(image, ports={str(config["port"]): (config['host'],None)}, volumes={path: {'bind': '/tmp', 'mode': 'ro'}}, detach=True)
    print(container.id)
    client2 = docker.APIClient(base_url='unix://var/run/docker.sock')
    config['host_port'] = client2.inspect_container(container.id)['NetworkSettings']['Ports'][str(config['port'])+'/tcp'][0]['HostPort']
    return container

def get_url(config, test):
    print(test['api'])
    return 'http://'+config['host'] + ':' + str(config['host_port']) + test['api']

def runRest(image, config, tests, path):
    print('running rest')
    container = getEP(image, config, path)
    time.sleep(5)
    for test in range(len(tests)):
        print('Hi',test)
        url = get_url(config, tests[test])
        print(url)
        if(tests[test]["method"]=='GET'):
            print('Trying to GET')
            try:
                real = requests.get(url)
                print(real.status_code)
                print(real.text)
            except Exception as e:
                print(e)
                container.logs()
            expected = open(tests[test]["o"]).read().rstrip()
            if(real.status_code == tests[test]["status"]):
                if(real.text.rstrip() == expected):
                    tests[test]["r"] = "Success"
                else:
                    tests[test]["r"] = 'Error in body'
            else:
                tests[test]["r"] = "Wrong Status Code"
    container.stop()
    container.remove()
    return tests

def runWeb(image, config):
    container = getEP(image, config, path='')
    url =  get_url(config, {'api': ''})
    print(url)
    return [{'url':url, 'containerId':container.id}]


def runTest(image, path):
    client = docker.from_env()
    container = client.containers.run(image, volumes={path: {'bind': '/mnt/tests', 'mode': 'ro'}}, remove=True)
    print("done")

def stopDocker(container_id):
    client = docker.from_env()
    container = client.containers.get(container_id)
    container.stop()
    container.remove()
    return 'Success'

# runCUI("algo", cli_tests)
# runRest("rest",config, tests)
# runWeb("web",config,'')

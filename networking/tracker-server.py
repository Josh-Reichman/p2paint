from socket import *
import json
import http

peer_list = []
port_num = 0

def send_peer_list():
    """Send a json of the peer list to the requestor."""
    data = {
        "response" : "OK",
        "curr_peers" : peer_list
    }
    return json.dumps(data)

def remove_peer(req_ip):
    """Remove the peer from the peer list."""
    peer_list.remove(req_ip)

    data = {
        "response" : "REMOVED"
    }
    return json.dumps(data)


def add_peer(req_ip):
    """Add the peer to the peer list."""
    peer_list.append(req_ip)

    data = {
        "response" : "ADDED"
    }
    return json.dumps(data)


def decode_action(request):
    """Decode the requested action."""

    return json.loads(request)['request']


if __name__ == 'main':
    
    server_port = 12000
    server_socket = socket(AF_INET,SOCK_STREAM)
    server_socket.bind(('',server_port))
    server_socket.listen(1)

    print('server running babyyyyyyy')

    while True:

        connection_socket, addr = server_socket.accept()    # addr is a (ip, port)
        request = connection_socket.recv(1024)    # excessive number of characters

        requested_action = decode_action(request)

        if (requested_action == 'ADD'):
            requested_ip = json.loads(request)['ip']
            connection_socket.send(add_peer(requested_ip))
            print(requested_ip + 'added')

        elif(requested_action == 'REMOVE'):
            requested_ip = json.loads(request)['ip']
            connection_socket.send(remove_peer(requested_ip))
            print(requested_ip + 'deleted')

        elif('PEERS'):
            connection_socket.send(send_peer_list())
            print('Peer list sent to ' + addr[0])

        else:
            print('Unknown action: ' + requested_action)
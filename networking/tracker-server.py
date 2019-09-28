from socket import *
import json
import http
import sys

peer_list = ['bruh moments']

def send_peer_list(req_ip):
    """Send a json of the peer list to the requestor."""
    global peer_list

    data = {
        "response" : "OK",
        "peers" : peer_list,
        "your_ip" : req_ip
    }
    return json.dumps(data).encode()

def remove_peer(req_ip):
    """Remove the peer from the peer list."""
    global peer_list

    peer_list.remove(req_ip)

    data = {
        "response" : "REMOVED"
    }
    return json.dumps(data).encode()


def add_peer(req_ip):
    """Add the peer to the peer list."""
    global peer_list

    peer_list.append(req_ip)

    data = {
        "response" : "ADDED"
    }
    return json.dumps(data).encode()


def decode_action(request):
    """Decode the requested action."""

    return json.loads(request)['request']


def main():
    """Main function of the tracker server."""

    server_port = 12000

    if len(sys.argv) > 1:
        server_port = int(sys.argv[1])

    server_socket = socket(AF_INET,SOCK_STREAM)
    server_socket.bind(('',server_port))
    server_socket.listen(1)

    print('server running babyyyyyyy')

    while True:

        connection_socket, addr = server_socket.accept()    # addr is a (ip, port)
        request = connection_socket.recv(1024)    # excessive number of characters

        requested_action = decode_action(request)

        if (requested_action == 'ADD'):
            connection_socket.send(add_peer(addr[0]))
            print(addr[0] + ' added')

        elif(requested_action == 'REMOVE'):
            connection_socket.send(remove_peer(addr[0]))
            print(addr[0] + ' deleted')

        elif('PEERS'):
            connection_socket.send(send_peer_list(addr[0]))
            print('Peer list sent to ' + addr[0])

        else:
            print('Unknown action: ' + requested_action)
    
        connection_socket.close()

if __name__ == '__main__':
    main()

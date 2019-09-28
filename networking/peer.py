from socket import *
import json

hostname = ''
port = -1
my_ip = -1
peers = []

def main():
    hostname = sys.argv[1]
    port = int(sys.argv[2])

    send_peers_request()
    send_add_request()
    send_remove_request()
    print('debug over')


def __create_request(request):
    data = {
        "request" : request
    }
    return json.dumps(data)


def send_add_request():
    """Requests to be added as a peer."""
    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect((hostname, port))
    client_socket.send(__create_request('ADD'))

    print(client_socket.recv(1024))
    client_socket.close()


def send_peers_request():
    """Request the peers from the tracker."""
    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect((hostname, port))
    client_socket.send(__create_request('PEERS'))

    response = json.loads(client_socket.recv(2048))
    my_ip = response['your_ip']

    peers = filter(__filter_ip, response['peers'])
    print(response)
    client_socket.close()


def __filter_ip(var):
    """Ensures that this peer does not send to itself."""
    return var != my_ip


def send_remove_request():
    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect((hostname, port))
    client_socket.send(__create_request('REMOVE'))

    print(client_socket.recv(1024))
    client_socket.close()


if __name__ == 'main':
    main()
from socket import *
import json
import sys
import time
import select

hostname = ''
port = -1
my_ip = -1
peers = []

peers_map = {
    "North" : None,
    "South" : None,
    "West"  : None,
    "East"  : None
}

def main():
    global hostname, port 

    hostname = sys.argv[1]
    port = int(sys.argv[2])

    send_add_request()

    try:
        while True:
            send_peers_request()

            for direc in peers_map:
                peers_map[direc] = create_socket_pair(peers[0])

            for direc in peers_map:
                read_from_socket(direc[0])
                write_to_socket(direc[1])
            
            time.sleep(0.5)

    except KeyboardInterrupt:
        send_remove_request()
        for direc in peers_map:
            direc[0][0].close()
            direc[1].close()

    print('finished')




#
# Functions for interacting with other peers
#

def create_socket_pair(peer_ip):
    port = 12012

    listen_socket = socket(AF_INET,SOCK_STREAM)
    listen_socket.bind(('',port))

    peer_socket = socket(AF_INET, SOCK_STREAM)
    peer_socket.connect((peer_ip, port))

    return ([listen_socket], peer_socket)


def read_from_socket(socket):
    read, write, error = select.select(socket, [], [])

    for sock in read:
        if sock == socket:
            data = sock.recv(1024)
            print(data)

            # data here will be a JSON changed to rendering instructions on this peer

def write_to_socket(socket):
    socket.send('bruh momento')
        

#
# Functions for interacting with the tracker server 
#


def __create_request(request):
    """Create a request based on the action parameter supplied."""
    data = {
        "request" : request
    }
    return json.dumps(data).encode()


def send_add_request():
    """Requests to be added as a peer."""
    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect((hostname, port))
    client_socket.send(__create_request('ADD'))

    print(client_socket.recv(1024))
    client_socket.close()


def send_peers_request():
    """Request the peers from the tracker."""
    global my_ip, peers

    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect((hostname, port))
    client_socket.send(__create_request('PEERS'))

    response = json.loads(client_socket.recv(2048))
    my_ip = response['your_ip']

    peers = list(filter(__filter_ip, response['peers']))
    print(response)
    client_socket.close()


def __filter_ip(var):
    """Ensures that this peer does not send to itself."""
    return var != my_ip


def send_remove_request():
    """Remove self from the tracker and thus the p2p network."""
    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect((hostname, port))
    client_socket.send(__create_request('REMOVE'))

    print(client_socket.recv(1024))
    client_socket.close()


if __name__ == '__main__':
    main()
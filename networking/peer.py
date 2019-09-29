from socket import *
import json
import sys
import time
import select

hostname = ''
port = 12021
my_ip = -1
peers = []

# this needs to be (listen_socket, writing_socket)
# North will be base_port + 1
# East will be base_port + 4
peers_map = {
    "1" : None,
    "2" : None,
    "3"  : None,
    "4"  : None
}

def main():
    global hostname, port 

    hostname = sys.argv[1]

    send_add_request()

    listen_socket = socket(AF_INET, SOCK_STREAM)
    listen_socket.bind(('', port))

    try:
        while True:

            data = read_from_socket([listen_socket])
            

            if data is not None:
                data = json.loads(data)
                data = data['peers']
                if data == 'ESTABLISH':
                    recv_establish_peer_connections
            else:
                send_peers_request()
            #     establish_connection_peer(peers[0])

            

            time.sleep(0.5)

    except KeyboardInterrupt:
        send_remove_request()
        for direc in peers_map.items():
            direc[0][0].close()
            direc[1].close()


#
# Functions for interacting with other peers
#


def establish_connection_peer(ip):
    global port

    selected_peer = __select_peer_connection()
    # validates that new connections can be made
    if selected_peer != None:
        client_socket = socket(AF_INET, SOCK_STREAM)
        client_socket.connect((ip, port))

        data = {
            "peer" : "ESTABLISH",
        }

        client_socket.send(json.dumps(data).encode())

        ports = json.loads(client_socket.recv(1024).decode())['ports']

        for x in range(0, 3):
            if ports[x]:
                peer_socket = socket(AF_INET, SOCK_STREAM)
                peer_socket.connect((ip, port + x))

                listen_socket = socket(AF_INET, SOCK_STREAM)
                listen_socket.bind(('', port + selected_peer))
                
                data = {
                    "RESPONSE" : "OK",
                    "port_offset" : selected_peer
                }
                client_socket.send(json.dumps(data).encode())

                client_socket.close()
                peers_map[str(selected_peer)] = (listen_socket, peer_socket)
                break
    else:
        # Not able to connect with this peer
        print('cringe, not being able to connect bro pls')


def recv_establish_peer_connections(ip, socket):
    global port

    selected_peer = __select_peer_connection()
    # validates that new connections can be made
    if selected_peer != None:
        listen_socket = socket(AF_INET, SOCK_STREAM)
        listen_socket.bind(('', port + selected_peer))

        socket.connect((ip, port))

        data = {
            "ports" : __get_available_connections()
        }

        socket.send(json.dumps(data).encode())

        peer = json.loads(socket.recv(1024).decode())['port_offset']

        peer_socket = socket(AF_INET, SOCK_STREAM)
        peer_socket.connect((ip, port + int(peer)))

        peers_map[str(selected_peer)] = (listen_socket, peer_socket)


    
def __select_peer_connection():
    for peer in peers_map:
        if peers_map[peer] is not None:
            return int(peer)
    return None


def __get_available_connections():
    avail_peers = []
    for peer in peers_map:
        if peer is not None:
            avail_peers.append(True)
        else:
            avail_peers.append(False)


def read_from_socket(socket):
    read, write, error = select.select(socket, [], [])
    for sock in read:
        if sock == socket:
            data = sock.recv(1024)
            return data.decode()



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
    client_socket.connect((hostname, 12000))
    client_socket.send(__create_request('ADD'))

    print(client_socket.recv(1024))
    client_socket.close()


def send_peers_request():
    """Request the peers from the tracker."""
    global my_ip, peers, hostname

    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect((hostname, 12000))
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
    print('Debug run')
    main()
# coding: utf-8

"""
Encryption without signature
"""

import pickle
import queue
import select
import socket
import sys

from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA

class NodeException(Exception):
    pass

class Node(object):
    """
    This class represent a node of the network. It will play the role of
    both a server and a client.

    Methods:
        __init__(name, port)
        connect_to_remote_server(remote_host, remote_host_port)
        start_node()
        handle_input_sock(inputready)
        handle_output_sock(outputready)
        handle_exceptions(exceptready)
    """

    def __init__(self, name, port):
        self.name = name
        self.port = port
        self.inputs = [sys.stdin]
        self.outputs = []
        self.groups = {}
        self.key = RSA.generate(2048)
        self.public_key = self.key.publickey()
        self.connected_nodes = {
            sys.stdin: {'msg_queue': queue.Queue()},
            sys.stdout: {'msg_queue': queue.Queue()}
        }
        self.all_nodes = {'*': {'key': None}}
        self.backlog = 5
        self.size = 4096
        self.sock = None

    def connect_to_remote_server(self, remote_host_port, remote_host='localhost'):
        """
        Start the connection with the upstream node.
        """
        remote_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            remote_sock.connect((remote_host, remote_host_port))
        except ConnectionRefusedError:
            raise NodeException('The server you mentionned do not exist')
        else:
            # Add the client to the list of input to watch
            self.inputs.append(remote_sock)
            # Add a queue for the client to send messages
            self.connected_nodes[remote_sock] = {'msg_queue':queue.Queue()}
            # Sends a message to check if the name used already exists
            msg = self.name + '->*:test_name'
            remote_sock.send(msg.encode())

    def format_msg(self, origin, destination, msg):
        return origin + '->' + destination + ':' + msg

    def print_msg(self, msg):
        """Send the msg to the sys.stdout flow to print."""
        self.connected_nodes[sys.stdout]['msg_queue'].put_nowait(msg)
        if sys.stdout not in self.outputs:
            self.outputs.append(sys.stdout)

    def share_public_key(self, destination='*'):
        """Will broadcast the public key in a string format."""
        public_key = self.public_key.exportKey().decode()
        msg = self.format_msg(self.name, destination, 'key=' + public_key + '\n')
        self.broadcast(msg.encode())

    def broadcast(self, msg, sock_src=None):
        """Send msg to all connected node except sock_src if specified."""
        # print(msg.decode())
        for sock in self.inputs:
            if sock != sock_src and sock != sys.stdin and sock != sys.stdout:
                try:
                    self.connected_nodes[sock]['msg_queue'].put_nowait(msg)
                except KeyError:
                    self.connected_nodes[sock] = {'msg_queue': queue.Queue()}
                    self.connected_nodes[sock]['msg_queue'].put_nowait(msg)
                
            if (sock not in self.outputs and 
                sock != sys.stdout and 
                sock != sys.stdin
               ):
                self.outputs.append(sock)

    def handle_received_msg(self, msg_recv_enc, sock_src):
        orig_dest, msg = msg_recv_enc.split(b':', maxsplit=1)
        origin, destination = orig_dest.decode().split('->', maxsplit=1)
        # if a node send a test_name msg, it means it is a new one and that
        # the current node is the server for the new node.
        if msg == b'test_name':
            # if node already exists
            if origin in self.all_nodes or origin == self.name:
                to_send = self.format_msg(self.name, origin, 'test_name_fail')
            # if node does not exist yet
            else:
                to_send = self.format_msg(self.name, origin, 'test_name_success')
            to_send = to_send.encode()
            sock_src.send(to_send)

        # Response of the server node if the current node name already exists
        elif msg == b'test_name_fail':
            raise NodeException('Node already exists.')
        elif msg == b'test_name_success':
            # to_send = self.name + '->*:hola\n'
            # self.broadcast(to_send.encode())
            self.share_public_key()

        # Handshake to share the public keys
        elif msg.startswith(b'key='):
            # Message do not concern current node. He just pass it by.
            if destination != self.name and destination != '*':
                self.broadcast(msg_recv_enc, sock_src)
            # Node is one/the destinator, msg should be printed and response
            # sent.
            else:
                c, public_key = msg.split(b'key=', maxsplit=1)
                public_key = public_key.rstrip()
                if origin not in self.all_nodes:
                    self.all_nodes[origin] = {'key': None}
                to_prt = origin + ' PUBLIC KEY ='
                # print(to_prt)
                # print(public_key)
                self.all_nodes[origin]['key'] = RSA.importKey(public_key)
                if destination == '*':
                    # Transmission of message to following nodes
                    self.broadcast(msg_recv_enc, sock_src)
                    # Response to aknowledge new node of current node presence
                    self.share_public_key(origin)

        # If current node is the destination
        elif destination == self.name:
            if msg != b'OK\n':
                msg = self.key.decrypt(msg)
                #
                #   TO USE WITH SIGNATURE UNCOMMENT
                #
                # msg, signature = msg.split(b'|signature', maxsplit=1)
                # signature = int(signature.decode())
                # msg_hash = SHA256.new(msg).digest()
                # if self.all_nodes[origin]['key'].verify(msg_hash, signature):
                #     print('message verificated')
                # else:
                #     print('pb with verif')
                to_prt = origin + ' SAYS ' + msg.decode() 
                self.print_msg(to_prt)

                to_send = self.format_msg(self.name, origin, 'OK\n')
                self.broadcast(to_send.encode())
            else:
                self.print_msg('OK\n')

        elif destination == '*':
            msg = msg.decode()
            to_prt = origin + ' SAYS ' + msg if msg != 'OK\n' else msg
            self.print_msg(to_prt)            
            self.broadcast(msg_recv_enc, sock_src)

        # Current node not the destination needs to transmit message
        else:
            self.broadcast(msg_recv_enc, sock_src)

        # Origin not in network means new node that we need to add
        # to the latter
        if (origin not in self.all_nodes and 
            origin != self.name
           ):
            self.all_nodes[origin] = {'key': None}
        
    def send_msg(self, msg_to_send, sock_src=None):
        if msg_to_send == 'END\n':
            self.close()

        elif msg_to_send.startswith('CHAT'):
            command, dest, msg = msg_to_send.split(maxsplit=2)
            if dest not in self.all_nodes:
                to_prt = 'WRONG ' + dest + ' unknown id.\n'
                self.print_msg(to_prt)
            else:
                #
                #   TO USE WITH SIGNATURE UNCOMMENT
                #
                # msg_hash = SHA256.new(msg.encode()).digest()
                # sign = self.key.sign(msg_hash, '')
                # signature = str(sign[0]).encode()
                # msg = msg.encode() + b'|signature' + signature
                if dest != '*':
                    msg = self.all_nodes[dest]['key'].encrypt(msg, 2048)
                else:
                    msg = (msg.encode(),)
                prepend = self.format_msg(self.name, dest, '')
                msg = prepend.encode() + msg[0]
                print('msg to be sent ', msg)
                self.broadcast(msg)

        elif msg_to_send == 'CONNECTED\n':
            for el in self.connected_nodes:
                print(el, self.connected_nodes[el])
        elif msg_to_send == 'ALL\n':
            for el in self.all_nodes:
                print(el, self.all_nodes[el])

        else:
            self.print_msg('Command invalid.')

    def handle_input_sock(self, inputready):
        for s in inputready: 
            if s == self.sock: 
                # handle the node socket
                client, address = self.sock.accept() 
                self.inputs.append(client)
                self.connected_nodes[client] = {'msg_queue':queue.Queue()}

            elif s == sys.stdin:
                # handle the inputs from the user
                msg = sys.stdin.readline()
                self.send_msg(msg)
                
            else: 
                # handle all other sockets
                msg_recv = s.recv(self.size)
                
                if msg_recv:
                    self.handle_received_msg(msg_recv, s)
                    if s not in self.outputs:
                        self.outputs.append(s)

                # A readable socket without data available is from a client 
                # that has disconnected, and the stream is ready to be closed.
                else:
                    # Stop listening for input on the connection
                    if s in self.outputs:
                        self.outputs.remove(s)
                    self.inputs.remove(s)
                    del self.connected_nodes[s]
                    s.close()


    def handle_output_sock(self, outputready):
        for s in outputready:
            try:
                next_msg = self.connected_nodes[s]['msg_queue'].get_nowait()
            except queue.Empty:
                # No messages waiting so stop checking for writability
                self.outputs.remove(s)
            else:
                # Message is to be printed
                if s == sys.stdout:
                    sys.stdout.write(next_msg)
                # Message is to be send
                else: 
                    s.send(next_msg)

    def handle_exceptions(self, exceptready):
        for s in exceptready:
            # Stop listening for input on the connection
            self.inputs.remove(s)
            del self.connected_nodes[s]
            if s in self.outputs:
                self.outputs.remove(s)
            s.close()
            # Remove from the connected_nodes dictionnary
            del self.connected_nodes[s]

    def start_listening(self):
        """
        Open the listening on the port of the node for other nodes to connect.
        """
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        self.sock.bind(('localhost',self.port)) 
        self.sock.listen(self.backlog) 
        self.inputs.append(self.sock)

        while self.inputs != [sys.stdin, sys.stdout]:
            inputready, outputready, exceptready \
                = select.select(self.inputs, self.outputs, [], 0.5) 

            self.handle_input_sock(inputready)
            self.handle_output_sock(outputready)
            self.handle_exceptions(exceptready)

        self.sock.close()

    def close(self, sock_src=None):
        """
        Close the node.
        """
        self.inputs = [sys.stdin, sys.stdout]

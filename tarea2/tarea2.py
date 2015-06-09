# coding: utf-8

import argparse
import queue

from Node import Node

#
#   Argument Parser
#

parser = argparse.ArgumentParser(description='Process the client name.')
parser.add_argument('node_port', nargs='+')
args = parser.parse_args()
nodes = args.node_port

for n in nodes:
    if ':' not in n:
        raise AssertionError('Options must be of type name:port')

node_name, node_port = nodes[0].split(':')

if len(nodes) == 2:
    remote_name, remote_port = nodes[1].split(':')
    remote_name = remote_name.split('_')[2]

#
#   Create and launch Node
#

node = Node(node_name, int(node_port))

if len(nodes) == 2:
    node.connected_nodes[remote_name] = {'msg_queue':queue.Queue()}
    node.connect_to_remote_server(int(remote_port))

node.start_listening()

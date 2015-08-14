# TAREA 2 : decentralized and secure chat

## Description

The idea is to do a decentralized and secure chat. There are no server or central authority in this case. Every node is both a server and a client.

## How it works

First a node gets up. Then other nodes can connect to either this first node or any other node already in the network.

When connecting itself, the node sends a broadcast with his name and address and a public key. Every other node then add this key to their adress book.

To send a message, the node can choose to broadcast it (in the case it will not be encrypted) or the make it private (in this case it will use the public key of his target.

The message will be sent to every person on the network until the target is found.

## Syntax

To be completed

## Hypothesis

A few hypothesis were made during this homework (basically because given the nature of the network, I could not find a solution to these problem or did not have the time to implement them).

- we forget about the Man in the middle attack when sharing the keys (each node will transmit the public key he receive without altering them)
- that the network is relatively small given that the messages are transmitted to every other node (or almost)

## What has to be improved

- signature : I had a lot of problem with this. As I use pycrypto, I cannot encrypt messages that are bigger than the key. Thus, as the signature are of the size of the key, I cannot sign the messages. This is a security flaw that should be address
- find a way to secure the key sharing part

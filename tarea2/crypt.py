from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA

import struct

key = RSA.generate(1024)
pub_key = key.publickey()

msg = b'testtesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttest'
print('\nmsg', msg)
# msg_hash = SHA256.new(test).digest()
# print('\nmsg_hash', msg_hash)
sign = key.sign(msg, '')
print('\nsign', sign[0])
# signa = str(sign[0]).encode()
# signa = struct.pack('>L', sign[0])
size = len(str(sign[0]))//5
signa1 = str(sign[0])[:size].encode()
msg_sign = msg + b'signature' + signa1
# msg = msg
print('\nmsg', msg_sign)
# msg_hex = binascii.hexlify(msg)
# print('\nmsg_hex', msg_hex)
msg_enc = pub_key.encrypt(msg_sign, 32)
print('\nmsg_enc', msg_enc[0])
msg_dec = key.decrypt(msg_enc[0])
print('\nmsg_dec', msg_dec)
# msg_dec = binascii.unhexlify(msg_dec_hex)

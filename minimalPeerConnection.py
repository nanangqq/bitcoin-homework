import struct
import socket

import utils
import msgUtils


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#sock.connect(("184.155.9.47", 8333))
#sock.connect(("199.247.18.168", 8333))
sock.connect(("13.125.187.220", 8333))

sock.send(msgUtils.getVersionMsg())

while 1:
    header = sock.recv(24)
    if len(header) == 0: break
    magic, cmd, payload_len, checksum = struct.unpack('<L12sL4s', header)
    buf = ''

    while payload_len > 0:
        chunk = sock.recv(payload_len)
        if len(chunk) == 0: break
        buf += chunk
        payload_len -= len(chunk)

    msgUtils.processChunk(header, buf)

    cmd = cmd.replace('\0', '') # Remove null termination
    if cmd == 'version':
        print 'Sending verack'
        sock.send(msgUtils.getVerackMsg())

    if cmd == 'verack':
        print 'Sending addr'
        sock.send(msgUtils.getAddrMsg())

import binascii
import os
import socket
import sys
from . import util

def parseMessage(message):
    lines = message.splitlines()
    
    assert(len(lines) % 2 == 0)
    
    diffs = util.chunk(lines, 2)
      
    for diff in diffs:
        diff[1] = binascii.unhexlify(diff[1].zfill(8))
    return diffs

class MemoryWatcherZMQ:
    def __init__(self, path=None, port=None):
        try:
            import zmq
        except ImportError as err:
            print("ImportError: {0}".format(err))
            sys.exit("Need zmq installed.")
        context = zmq.Context()
        self.socket = context.socket(zmq.REP)
        if path:
            print("Binding socket to correct path")
            self.socket.bind("ipc://" + path)
        elif port:
            self.socket.bind("tcp://127.0.0.1:%d" % port)
        else:
            raise Exception("Must specify path or port.")
    
        self.messages = None
  
    def get_messages(self):
        if self.messages is None:
            message = self.socket.recv()
            message = message.decode('utf-8')
            self.messages = parseMessage(message)
        return self.messages
  
    def advance(self):
        self.socket.send(b'')
        self.messages = None

class MemoryWatcher:
    """Reads and parses game memory changes.

    Pass the location of the socket to the constructor, then either manually
    call next() on this class to get a single change, or else use it like a
    normal iterator.
    """
    def __init__(self, path):
        """Deletes the old socket."""
        self.path = path
        try:
            os.unlink(self.path)
        except OSError:
            pass

    def __enter__(self):
        self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
        self.sock.settimeout(0.001)
        self.sock.bind(self.path)
        return self

    def __exit__(self, *args):
        """Closes the socket."""
        self.sock.close()

    def __iter__(self):
        """Iterate over this class in the usual way to get memory changes."""
        return self

    def __next__(self):
        """Returns the next (address, value) tuple, or None on timeout.

        address is the string provided by dolphin, set in Locations.txt.
        value is a four-byte string suitable for interpretation with struct.
        """
        try:
            data = self.sock.recvfrom(1024)[0].decode('utf-8').splitlines()
        except socket.timeout:
            return None
        assert len(data) == 2
        # Strip the null terminator, pad with zeros, then convert to bytes
        return data[0], binascii.unhexlify(data[1].strip('\x00').zfill(8))

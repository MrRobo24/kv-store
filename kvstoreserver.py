from exception import CustomException
from kvstore import KVStore
import socket

class KVStoreServer:
  _kv_store = None
  
  def __init__(self, host='127.0.0.1', port=6369):
    if (KVStoreServer._kv_store != None):
      raise(CustomException("KVStoreServer is a singleton class"))
    
    KVStoreServer._kv_store = KVStore()
    self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.server_socket.bind((host, port))
    self.server_socket.listen(5)
    print(f"Server started on {host}:{port}")
    
  def handle_client(self, client_socket):
    data = client_socket.recv(1024).decode()
    if not data:
      client_socket.sendall(b'INVALID_COMMAND')
    data = data.strip('\n').split(' ')
    command, key, val = None, None, None
    command = data[0]
    if len(data) > 1:
      key = data[1]
    if len(data) > 2:
      val = data[2]
    
    if command == 'PUT':
      resp = KVStoreServer._kv_store.put(key, val)
      if resp == val:
        print(resp)
        client_socket.sendall(b'OK')
      else: 
        client_socket.sendall(b'KV_ERROR')
    elif command == 'GET':
      val = KVStoreServer._kv_store.get(key)
      if val:
        client_socket.sendall(val.encode())
      else:
        client_socket.sendall(b'NOT_FOUND')
    elif command == 'REMOVE':
      if KVStoreServer._kv_store.remove(key):
        client_socket.sendall(b'OK')
      else:
        client_socket.sendall(b'NOT_FOUND')
    else:
      client_socket.sendall(b'INVALID_COMMAND')
  
    client_socket.close()

  def start(self):
    while True:
      client_socket, addr = self.server_socket.accept()
      print(f"Connection from {addr}")
      self.handle_client(client_socket)
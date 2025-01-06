from exception import CustomException
from kvstore import KVStore
import socket
import threading

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
    try:
      data = client_socket.recv(1024).decode()
      if not data:
        client_socket.sendall(b'INVALID_COMMAND')
      parts = data.strip('\n').split(' ')
      command = parts[0].upper()
      key = parts[1] if len(parts) > 1 else None
      val = parts[2] if len(parts) > 2 else None
      
      if command == 'PUT':
        if key and val:
          resp = KVStoreServer._kv_store.put(key, val)
          client_socket.sendall(b'OK' if resp == val else b'KV_ERROR')
        else: 
          client_socket.sendall(b'INVALID_COMMAND')
      elif command == 'GET':
        if key:
          val = KVStoreServer._kv_store.get(key)
          client_socket.sendall(val.encode() if val else b'NOT_FOUND')
        else:
          client_socket.sendall(b'INVALID_COMMAND')
      elif command == 'REMOVE':
        if key:
          success = KVStoreServer._kv_store.remove(key)
          client_socket.sendall(b'OK' if success else b'NOT_FOUND')
        else:
          client_socket.sendall(b'INVALID_COMMAND')
      else:
        client_socket.sendall(b'INVALID_COMMAND')
    except Exception as e:
      print(f"Error handling client: {e}")
      client_socket.sendall(b'SERVER_ERROR')
    finally:
      client_socket.close()

  def start(self):
    while True:
      client_socket, addr = self.server_socket.accept()
      print(f"Connection from {addr}")
      client_handler = threading.Thread(target=self.handle_client, args=(client_socket,))
      client_handler.daemon = True
      client_handler.start()
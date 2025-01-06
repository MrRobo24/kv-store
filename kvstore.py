from exception import CustomException
import threading
import queue

class KVStore:
  _kv_store = None
  
  def __init__(self, log_file="kv_store.log"):
    if (KVStore._kv_store != None):
      raise(CustomException("KVStore is a singleton class"))
    
    KVStore._kv_store = {}
    self.log_file = log_file
    self.log_queue = queue.Queue()
    self.writer_thread = threading.Thread(target=self._write_to_log, daemon=True)
    self.writer_thread.start()
    self._load_from_log()
    
  def _log_change(self, command, key, value = None):
    self.log_queue.put((command, key, value))
    
  def _write_to_log(self):
    while True:
      command, key, value = self.log_queue.get()
      with open(self.log_file, "a") as f:
        if command == "PUT":
          f.write(f"PUT {key} {value}\n")
        elif command == "REMOVE":
          f.write(f"REMOVE {key}\n")
      self.log_queue.task_done()
        
  def _load_from_log(self):
    try:
      with open(self.log_file, "r") as f:
        for line in f:
          parts = line.strip().split()
          if parts[0] == "PUT" and len(parts) == 3:
            key, value = parts[1], parts[2]
            KVStore._kv_store[key] = value
          elif parts[0] == "REMOVE" and len(parts) == 2:
            key = parts[1]
            if key in KVStore._kv_store:
              del KVStore._kv_store[key]
    except FileNotFoundError:
      print('No previous log file found')
    
  def put(self, key, val):
    if not key.strip() == '':
      self._log_change("PUT", key, val)
      KVStore._kv_store[key] = val
      return val
    return None
    
  def get(self, key):
    return KVStore._kv_store.get(key, None)
  
  def remove(self, key):
    if KVStore._kv_store.get(key, None):
      self._log_change("REMOVE", key)
      del KVStore._kv_store[key]
      return True
    else:
      return False
  
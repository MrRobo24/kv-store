class KVStore:
  def __init__(self, log_file="kv_store.log"):
    self.kv_store = {}
    self.log_file = log_file
    self._load_from_log()
    
  def _log_change(self, command, key, value=None):
    with open(self.log_file, "a") as f:
      if command == "PUT":
        f.write(f"PUT {key} {value}\n")
      elif command == "REMOVE":
        f.write(f"REMOVE {key}\n")
        
  def _load_from_log(self):
    try:
      with open(self.log_file, "r") as f:
        for line in f:
          parts = line.strip().split()
          if parts[0] == "PUT" and len(parts) == 3:
            key, value = parts[1], parts[2]
            self.kv_store[key] = value
          elif parts[0] == "REMOVE" and len(parts) == 2:
            key = parts[1]
            if key in self.kv_store:
              del self.kv_store[key]
    except FileNotFoundError:
      print('No previous log file found')
    
  def put(self, key, val):
    if not key.strip() == '':
      self._log_change("PUT", key, val)
      self.kv_store[key] = val
      return val
    return None
    
  def get(self, key):
    return self.kv_store.get(key, None)
  
  def remove(self, key):
    if self.kv_store.get(key, None):
      self._log_change("REMOVE", key)
      del self.kv_store[key]
      return True
    else:
      return False
  
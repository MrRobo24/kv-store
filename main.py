class KVStore:
  def __init__(self):
    self.kv_store = {}
    
  def put(self, key, val):
    if not key.strip() == '':
      self.kv_store[key] = val
    
  def get(self, key):
    return self.kv_store.get(key, None)
  
  def remove(self, key):
    if self.kv_store.get(key, None):
      del self.kv_store[key]
      return True
    else:
      return False
  
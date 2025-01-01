from main import KVStore

class Test:
  def __init__(self):
    self.kv = KVStore()
      
  def run_tests(self):
    self.test_put()
    self.test_get()
    self.test_remove()
    print('All tests passed')
  
  def test_put(self):
    self.kv.put('name', 'John Doe')
    assert self.kv.get('name') == 'John Doe'

  def test_get(self):
    self.kv.put('name', 'John Doe')
    assert self.kv.get('name') == 'John Doe'

  def test_remove(self):
    self.kv.put('name', 'John Doe')
    assert self.kv.remove('name') == True
    assert self.kv.remove('name') == False
    
if __name__ == '__main__':
  t = Test()
  t.run_tests()
  
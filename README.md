# kv-store
A simple key value store with simple persistence logic, all behind a socket server.

### Sample Commands
```
PUT key value
GET key
REMOVE key
```
You can use a custom script or tools like netcat ```nc``` to send commands to the kv-store server.

### Sample Log File
_kv_store.log_
```
PUT key val
PUT key val
PUT key2 val2
REMOVE key
PUT key3 val3
```
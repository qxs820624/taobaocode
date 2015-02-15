import bmemcached
import threading

class ConnMan:
    _MAX = 10
    _MAX_COUNT = 1000

    def __init__(self, host, username, password):
        self.host = host
        self.username = username
        self.password = password
        self._conns = []
        self._work_conns = set()
        self._lock = threading.Lock()
        
    def checkout(self):
        with self._lock:
            item = None
            if len(self._conns) <= 0:
                c = bmemcached.Client((self.host,),
                                      self.username, 
                                      self.password)
                item = [c, 1]
            else:
                item = self._conns[0]
                item[1] += 1 # add checkout count
                self._conns.pop(0)
                
            self._work_conns.add(item[0])
            return item
            
    def checkin(self, item):
        with self._lock:
            if item[0] in self._work_conns:
                self._work_conns.remove(item[0])

            if item[1] > self._MAX_COUNT: # too many checkout count
                print 'too many',item[1]
                return

            if len(self._conns) > self._MAX:
                assert 0
                return

            self._conns.insert(0, item)
  
class ClientWrap:
    def __init__(self, connMan):
        self._cli = connMan.checkout()
        self._connMan = connMan

    def __del__(self):
        if self._cli is None:
            return

        self._connMan.checkin(self._cli)
        self._connMan = None
        self._cli = None

    def set(self, key, value, expire=20):
        self._cli[0].set(key, value, expire)

    def get(self, key):
        return self._cli[0].get(key)

def get_client(man):
    return ClientWrap(man)

def test():
    connMan = ConnMan('127.0.0.1', 'test', 'hello')

    def test_case():
        c = get_client(connMan)
        c.get('hello')
        c.set('abcd','abcd')

    for i in range(10):
        try:
            test_case()
        finally:
            pass
        assert len(connMan._conns) == 1

if __name__ == '__main__':
    test()

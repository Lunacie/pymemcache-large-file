import unittest
from caching import Cache
import hashlib


class ChunkerTestCase(unittest.TestCase):
    def setUp(self) :
        self.client = Cache.client

    def test_readFile(self):
        name = "./test_file.txt"
        cache = Cache(chunk_size = 1)
        result = cache.readFile(name)
        expected = [b'a', b'b', b'c', b'd', b'\r', b'\n']

        cm = cache.client.get("{}:hash".format(name))
        file = open(name, 'rb')
        content = file.read()
        file.close()
        cm2 = hashlib.md5(content).digest()

        assert result == expected
        assert cm == cm2
        assert cache.client.get("{}:0".format(name)) == b'a'
        assert cache.client.get("{}:1".format(name)) == b'b'
        assert cache.client.get("{}:2".format(name)) == b'c'
        assert cache.client.get("{}:3".format(name)) == b'd'
        assert cache.client.get("{}:4".format(name)) == b'\r'
        assert cache.client.get("{}:5".format(name)) == b'\n'



if __name__ == '__main__':
    unittest.main()

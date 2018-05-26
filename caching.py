from pymemcache.client.base import Client
import hashlib

class Cache:
    client = None
    __path = ""
    __md5 = ""
    __chunks = []

    def __init__(self, chunk_size = 1000000) :
        self.client = Client(('localhost', 11211))
        self.__chunk_size = chunk_size

    def readFile(self, path, data=None) :
        self.__path = path
        if data is not None:
            data = data.encode()
        self.__md5 = self.__getMd5(data)
        self.__getChunks(data)
        self.__cache()
        return self.__chunks

    def getFile(self, name) :
        """ TODO: use join() instead """
        i = 0
        content = bytearray()
        while True :
            data = self.client.get("{}:{}" . format(name, i))
            if not data :
                break
            content += data;
            i += 1

        checksum = self.client.get("{}:hash". format(name))
        new_md5 = hashlib.md5(content).digest()
        assert checksum == new_md5, 'data corrupted'
        return content


    def __cache(self) :
        self.client.set("{}:hash" . format(self.__path), self.__md5)
        for i, chunk in enumerate(self.__chunks):
            item_key = "{}:{}" . format (self.__path, i)
            self.client.set(item_key, chunk)

    def __getMd5(self, data=None) :
        if data is not None :
            return hashlib.md5(data).digest()
        file = open(self.__path, 'rb')
        content = file.read()
        file.close()
        return hashlib.md5(content).digest()

    def __getChunks(self, data=None) :
        self.__chunks = []
        if data is not None :
            return hashlib.md5(data).digest()
        file = open(self.__path, 'rb')
        count = 0
        while True :
            data = file.read(self.__chunk_size)
            if not data :
                break
            self.__chunks.append(data)

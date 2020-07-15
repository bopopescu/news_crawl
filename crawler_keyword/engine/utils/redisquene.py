import redis
import hashlib
import uuid


class RedisQueue(object):



    def __init__(self, **redis_kwargs):
       self.__db= redis.Redis(**redis_kwargs)
       self.queue = "CRAWLER_QUEUE"
       self.message_prefix = "CRAWLER:"

    def qsize(self):
        """Return the approximate size of the queue."""
        return self.__db.llen(self.key)

    def empty(self):
        """Return True if the queue is empty, False otherwise."""
        return self.qsize() == 0

    def put(self, item):
        """Put item into the queue."""
        #key = hashlib.md5(item['url'].encode('utf8')).hexdigest()
        key = str(uuid.uuid4())
        self.__db.hmset(self.message_prefix + key, item)
        self.__db.lpush(self.queue, key)

    def get(self, timeout=None):
        key = self.__db.rpop(self.queue)
        if key is not None:
        
            key = key.decode('utf8')
            item = self.__db.hgetall(self.message_prefix + key)
    

            print(self.message_prefix + key)
            self.__db.hdel(self.message_prefix + key, *item.keys())

            return item
        return  None

    def get_nowait(self):
        """Equivalent to get(False)."""
        return self.get(False)
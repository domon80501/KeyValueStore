import unittest
import multiprocessing
from core.cache import Cache
from core.utilities import Utility


size = Utility.getCacheMaxSize()
mode = Utility.getCacheMode()


def setCache(key, value):
    cache = Cache()
    cache.set(key, value)


class cacheTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_addSingleCacheAndVerify(self):
        cache = Cache()

        key = "testUsername"
        value = "Kasshu"

        cache.set(key, value)
        result = cache.get(key)
        self.assertEqual(result, value)

    def test_addMutipleCacheAndVerify(self):
        cache = Cache()

        list = dict()
        for i in range(size):
            temp = "test"+str(i)

            list[temp] = temp + "_value"

        for k, v in list.items():
            cache.set(k, v)

        cache.query()

        # 反轉查看 LRU 運作情況
        if mode == "LRU":
            for k, v in reversed(list.items()):
                result = cache.get(k)
                self.assertEqual(result, v)
        else:
            # 正向
            for k, v in list.items():
                result = cache.get(k)
                self.assertEqual(result, v)

        cache.query()

    def test_addMutipleCacheAndVerify_Multiprocessing(self):
        cache = Cache()

        list = dict()
        for i in range(size):
            temp = "test"+str(i)

            list[temp] = temp + "_value"

        for k, v in list.items():
            p = multiprocessing.Process(target=setCache, args=(k, v))
            p.start()

        cache.query()

    # 清除緩存,透過 store 獲取
    def test_addCacheAndGetByKVS(self):
        cache = Cache()

        key = "testUsername"
        value = "Kasshu"

        cache.set(key, value)
        cache.remove(key)
        result = cache.get(key)
        
        self.assertEqual(result, value)


if __name__ == '__main__':
    unittest.main()

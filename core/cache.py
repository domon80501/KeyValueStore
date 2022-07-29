from collections import deque
from .keyValueStore import KeyValueStore
from .utilities import Utility

hash_map = dict()
queue = deque()
maxSize = Utility.getCacheMaxSize()

# FIFO: 先進先出模式 [get] 不理會 key
# LRU: 最常使用的擺在隊頭(key將會應用)
mode = Utility.getCacheMode()


class Cache:
    def get(self, key=None):
        kvs = KeyValueStore()
        ascii_key = ""  # mode FIFO 不理會 key.

        if key != None:
            ascii_key = Utility.ConvertToASCII(key)

        if ascii_key in queue and mode == "LRU":
            # 將當前命中的值移轉至隊頭，並回傳命中的值.
            queue.remove(ascii_key)
            queue.appendleft(ascii_key)
            return Utility.ConvertToString(hash_map[ascii_key])
        elif len(queue) > 0 and mode == "FIFO":
            # 取出最先進入隊伍的值.
            ascii_key = queue.pop()
            kvs.remove(ascii_key)
            return Utility.ConvertToString(hash_map.pop(ascii_key))
        else:
            result = kvs.get(ascii_key)

            if mode == "LRU" and len(result) > 0:
                # 當 mode 是 LRU 進行回存.
                self.setByfeedback(
                    ascii_key, Utility.ConvertToArrayASCII(result))

            return result

    def set(self, key, value):
        ascii_key = Utility.ConvertToASCII(key)
        ascii_value = Utility.ConvertToArrayASCII(value)

        if ascii_key not in queue:
            if len(queue) >= maxSize:
                match mode:
                    case "LRU":
                        disuseKey = queue.pop()  # 取出隊尾(最不常用)將其汰換.
                        queue.appendleft(ascii_key)
                        hash_map[ascii_key] = ascii_value
                        del hash_map[disuseKey]
                    case _:
                        return False
            else:
                queue.appendleft(ascii_key)
                hash_map[ascii_key] = ascii_value

                kvs = KeyValueStore()
                return kvs.set(ascii_key, ascii_value)
        else:
            match mode:
                case "LRU":
                    # Key 存在，將其加到隊頭，並賦予新值.
                    queue.remove(ascii_key)
                    queue.appendleft(ascii_key)
                    hash_map[ascii_key] = ascii_value
                case _:
                    return False

    def setByfeedback(self, key, value):  # 當前僅有 LRU mode 會使用.
        # key & value 已轉為 ascii 直接使用即可.
        # 因為來自 feedback 直接添加即可 無須其他判斷.
        queue.appendleft(key)
        hash_map[key] = value

    # 供 unittest 使用
    def remove(self, key):
        ascii_key = Utility.ConvertToASCII(key)
        del queue[queue.index(ascii_key)]
        del hash_map[ascii_key]

    def query(self):
        print(queue)
        print(hash_map)


# cac = Cache()
# cac.set("hello", "world")
# cac.set("asd", "asd123")
# # cac.query()

# print(cac.get("asd"))

# cac.query()

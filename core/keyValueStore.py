from collections import deque
from .utilities import Utility

hash_map = dict()  # data info
queue = deque()  # provide GIL-Lock
maxSize = Utility.getCacheMaxSize()

# FIFO 先進先出模式 get不理會key
# LRU 最常使用的擺在隊頭(key將會應用)
mode = Utility.getCacheMode()  # switch cache mode


class KeyValueStore:
    def get(self, key):
        if key in queue and mode == "LRU":
            # 將當前命中的值移轉至隊頭，並回傳命中的值.
            queue.remove(key)
            queue.appendleft(key)
            
            return Utility.ConvertToString(hash_map[key])
        elif len(queue) > 0 and mode == "FIFO":
            # 取出最先進入隊伍的值.
            key = queue.pop()
            return Utility.ConvertToString(hash_map.pop(key))

    def set(self, key, value):  # parameters 已經轉換為 ascii
        if key not in queue:
            if len(queue) >= maxSize:
                match mode:
                    case "LRU":
                        disuseKey = queue.pop()  # 取出隊尾(最不常用)將其汰換.
                        queue.appendleft(key)
                        hash_map[key] = value
                        del hash_map[disuseKey]
                    case _:
                        return False
            else:
                queue.appendleft(key)
                hash_map[key] = value

                return True
        else:
            match mode:
                case "LRU":
                    # Key 存在，將其加到隊頭，並賦予新值.
                    queue.remove(key)
                    queue.appendleft(key)
                    hash_map[key] = value
                case _:
                    return False

    def remove(self, key):  # FIFO mode 才會使用. pop後即移除，kvs也將移除該值.
        del queue[queue.index(key)]
        del hash_map[key]
        pass

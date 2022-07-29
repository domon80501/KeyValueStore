# KeyValueStore
簡單實現 cache to key-value store. (FIFO &amp; LRU)

---

進行測試

`python testCases.py`

可透過 `config.json` 修改 `cacheMaxSize` & `cacheMode`

**cacheMaxSize** : 緩存接受的數量

**cacheMode** :目前提供 FIFO (先進先出) 及 LRU (最近最少使用算法)

---

**testCases**

測試提供4個基礎項目
1. 單一 cache
2. 大量 cache
3. 多執行緒寫入 cache
4. 模擬遺失 cache 時, 透過 store 獲取並回存緩存(LRU才會應用)

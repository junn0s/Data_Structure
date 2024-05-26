from minheap import MinHeap
    
def lfu_sim(cache_slots):
    cache_hit = 0
    tot_cnt = 0
    cache = MinHeap()
    
    data_file = open("linkbench.trc")               # test.trc
    lpn_freq_dict = {}
    
    for line in data_file.readlines():
        lpn:int = line.split()[0]
        tot_cnt += 1
        
        if lpn in lpn_freq_dict:
            lpn_freq_dict[lpn][1] += 1
            cache.insert_count(lpn_freq_dict[lpn])  # 논리적으로 맞음
            #cache.insert(lpn_freq_dict[lpn])      # 중복됨
            cache_hit += 1
            #print(lpn_freq_dict)                   # for test.trc
            #print(cache.heapPrint())               # for test.trc
        else:
            lpn_freq_dict[lpn] = [lpn, 1]           # 논리적으로 먼저 오는게 맞음
            cache.insert(lpn_freq_dict[lpn])
                        
            if cache.size() > cache_slots:
                evicted = cache.deleteMin()
                if evicted[0] in lpn_freq_dict:
                    del lpn_freq_dict[evicted[0]]
            #print(lpn_freq_dict)                   # for test.trc
            #print(cache.heapPrint())               # for test.trc
  
    print("cache_slot =", cache_slots, "cache_hit =", cache_hit, "hit ratio =", cache_hit / tot_cnt)

if __name__ == "__main__":
    for cache_slots in range(100, 1000, 100):
        lfu_sim(cache_slots)
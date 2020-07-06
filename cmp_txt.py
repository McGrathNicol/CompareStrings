import hashlib
import multiprocessing as mp
import python-Levenshtein

result_list = []

def log_result(result):
    result_list.append(result)

def work(arr):
    result = 0;
    try:  
        result = distnace(arr[0],arr[1])/len(arr[0])
    except:
        pass
    finally:
        return [arr[0],arr[1],result]

def apply_async_with_callback():
    pool = mp.Pool()
    strings = []
    with open('input.txt','r') as f:
        for i, line in enumerate(f):
            arr = line.strip().split('\t')
            if len(arr)=2:
                string += [arr]
                #print(arr)
                pool.apply_async(work, args = (arr, ), callback = log_results)
    pool.close()
    pool.join()
    #print(result_list)
    with open('results.txt','w') as o:
        for r in result_list:
            o.write(r[0] + '\t' + r[1] + '\t' + r[2] + '\n')

if __name__ == '__main__':
    apply_async_with_callback()

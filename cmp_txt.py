import hashlib
import multiprocessing as mp
import Levenshtein

result_list = []

def log_result(result):
    result_list.append(result)

def work(arr):
    flat_result = 0.0
    letter_result = 0.0
    try:  
        flat_result = internal_score(arr[0],arr[1])
        letter_result = internal_score(letter_string(arr[0]),letter_string(arr[1]))

        
        #Levenshtein.distance(arr[0],arr[1])/len(arr[0])
    except:
        pass
    finally:
        print(flat_result)
        print(letter_result)
        if flat_result == 0.0 and letter_result == 0.0:
            return [arr[0],arr[1],'0.0']
        if flat_result == 1.0 and letter_result == 1.0:
            return [arr[0],arr[1],'1.0']
        return [arr[0],arr[1],"{:.3f}".format((flat_result * 0.2) + (letter_result * 0.8))]
        #return [arr[0],arr[1],"{:.3f}".format(result)]

def letter_string(s1):
    s1 = sorted(s1, key=str.lower)
    strOut = ""
    print(s1)
    for s in s1:
        if s.isdigit() or s.isalpha():
            strOut += s
    print(strOut)
    return strOut

def internal_score(s1,s2):
    max_len = max(len(s1), len(s2))
    if max_len == 0:
        return 0.0
    dist = Levenshtein.distance(s1,s2)
    return 1 - (dist / max_len)
    

def apply_async_with_callback():
    pool = mp.Pool()
    strings = []
    letter_string("free-made bakes")
    with open('input.txt','r') as f:
        for i, line in enumerate(f):
            arr = line.strip().split('\t')
            if len(arr)==2:
                strings += [arr]
                #print(arr)
                pool.apply_async(work, args = (arr, ), callback = log_result)
    pool.close()
    pool.join()
    #print(result_list)
    with open('results.txt','w') as o:
        for r in result_list:
            o.write(r[0] + '\t' + r[1] + '\t' + r[2] + '\n')

if __name__ == '__main__':
    apply_async_with_callback()

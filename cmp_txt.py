import hashlib
import multiprocessing as mp
import Levenshtein
import numpy

result_list = []

def log_result(result):
    result_list.append(result)

def work(arr):
    flat_result = 0.0
    letter_result = 0.0
    try:  
        flat_result = internal_score(arr[0],arr[1])
        letter_result = internal_score(letter_string(arr[0]),letter_string(arr[1]))
    except:
        pass
    finally:
        #print(flat_result)
        #print(letter_result)
        if flat_result == 0.0 and letter_result == 0.0:
            return [arr[0],arr[1],arr[2],arr[3],'0.0']
        if flat_result == 1.0 and letter_result == 1.0:
            return [arr[0],arr[1],arr[2],arr[3],'1.0']
        return [arr[0],arr[1],arr[2],arr[3],"{:.3f}".format((flat_result * 0.2) + (letter_result * 0.8))]
        #"{:.3f}".format()
        #return [arr[0],arr[1],"{:.3f}".format(result)]

def letter_string(s1):
    s1 = sorted(s1, key=str.lower)
    strOut = ""
    #print(s1)
    for s in s1:
        if s.isdigit() or s.isalpha():
            strOut += s
    #print(strOut)
    return strOut

def internal_score(s1,s2):
    max_len = max(len(s1), len(s2))
    if max_len == 0:
        return 0.0
    dist = compute_distance(s1,s2)
    #dist = Levenshtein.distance(s1,s2)
    return 1.0 - (dist / max_len)

def compute_distance(s1,s2):
    if s1 is None or s2 is None:
        return 0.0

    n = len(s1)
    m = len(s2)
    #print(n,m)
    d = numpy.empty((n,m))
    #[[]]
    #[[0 for x in range(n)] for y in range(m)] 
    #print(d)
    # Step 1
    if n == 0: return m-1
    if m == 0: return n-1
    
    # Step 2
    for i in range(0,n):
        d[i][0] = i
    
    for j in range(0,m):
        d[0][j] = j

    # Step 3
    for i in range(1,n):
        for j in range (1,m):
            cost = 0 if s2[j-1] == s1[i-1] else 1
            d[i][j] = min(min(d[i-1][j] + 1, d[i][j-1] + 1), d[i-1][j-1] + cost)         
    
    return d[n-1,m-1]

def apply_async_with_callback():
    pool = mp.Pool()
    strings = []
    #print('space',letter_string('space'))
    #print(Levenshtein.distance('eefr','aceps'))
    #print(Levenshtein.distance('acek','acegr'))
    #print(1.0-((compute_distance('free','space')* 0.2) + (compute_distance('eefr','aceps') * 0.8))/5.0)
    #print((Levenshtein.distance('free','space')* 0.2) + (Levenshtein.distance('eefr','aceps') * 0.8))
    with open('input.txt','r') as f:
        for i, line in enumerate(f):
            arr = line.strip().split('\t')
            if len(arr)==4:
                strings += [arr]
                #print(arr)
                pool.apply_async(work, args = (arr, ), callback = log_result)
    pool.close()
    pool.join()
    #print(result_list)
    with open('results.txt','w') as o:
        for r in result_list:
            o.write(r[0] + '\t' + r[1] + '\t' + r[2] + '\t' + r[3] + '\t' + r[4] + '\n')

if __name__ == '__main__':
    apply_async_with_callback()

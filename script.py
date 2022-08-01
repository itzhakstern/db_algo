from itertools import combinations



def closure(X, F):
    V = X
    len_v = len(V)
    while True:
        for atr in F:
            a = set(atr[0]).issubset(set(V))
            if a and not set(atr[1]).issubset(set(V)):
                V = ''.join(set(V+''.join(sorted(atr[1]))))
        if len_v == len(V):
            return V
        len_v = len(V)

def is_super_key(X, F, R):
    V = closure(X, F)
    return sorted(V) == sorted(R) 

def minimize(X, F):
    for x in X:
        if x in closure(X.replace(x, ''), F):
            X = X.replace(x, '')
    return X

def find_key(R, F):
    return minimize(R, F)

def all_keys(R, F):
    x = 0
    K = find_key(R, F)
    key_queue = [K]
    keys = [K]
    while len(key_queue):
        x += 1
        K = key_queue.pop()
        for atr in F:
            y = ''.join(sorted(atr[1]))
            k = ''.join(sorted(K))
            instruction = set(y).intersection(k)
            if len(instruction) > 0:
                s = ''.join(sorted(set(k.replace(''.join(instruction), '') + ''.join(sorted(atr[0])))))
                s_min = minimize(s, F)
                if s_min not in keys:
                    # s_min = minimize(s, F)
                    keys.append(s_min)
                    key_queue.append(s_min)
    return list(set(keys))

def is_in_bcnf(R, F):
    if len(R) <= 2:
        return True
    for atr in F:
        if set(atr[1]).issubset(set(atr[0])) or is_super_key(atr[0], F, R):
            continue
        return False
    return True

def a_is_in_keys(a, keys):
    for key in keys:
        if a in key:
            return True
    return False

def a_is_subset(a, atr_0):
    return a in atr_0

def is_in_3nf(R, F):
    if(is_in_bcnf(R, F)):
        return True
    keys = all_keys(R, F)
    # flag = False
    for atr in F:
        if not is_super_key(atr[0], F, R):
            return False
        for a in atr[1]:
            if (not a_is_in_keys(a, keys)) and (not a_is_subset(a,atr[0])):
                return False
    return True

# אלגוריתם לחישוב שימור תלויות
def is_dependency_preserving(sub_R, F):
    dependency = {}
    for atr in F:
        z = atr[0]
        while True:
            z_1 = z
            for r in sub_R:
                close_intersuction_z_ri = closure(''.join(set(z).intersection(set(r))), F)
                intersuction_zri_ri = set(close_intersuction_z_ri).intersection(set(r))
                z = intersuction_zri_ri.union(set(z))
            if set(z_1) == z:
                if(not set(atr[1]).issubset(z)):
                    dependency[atr] = [''.join(z), False]
                else:
                    dependency[atr] = [''.join(z), True]
                break
    flug = True
    for x in dependency:
        if not dependency[x][1]:
            flug = False
    print("*****    ", flug, "     ******")
        
    return dependency

# אלגוריתם לחישוב קבוצת התלויות F_R_i
def compute_dependencies_in_projection(R_i, F):
    res = [''.join(l) for i in range(len(R_i)) for l in combinations(R_i, i+1)]
    G = []
    for r in res:
        closure_r = closure(r, F)
        intrsection_ri_r = set(closure_r).intersection(set(R_i))
        G.append((r,''.join(intrsection_ri_r)))
    return G

# אלגוריתם למציאת כיסוי מינימלי
def compute_minimal_cover(F):
    G = []
    for atr in F:
        for A in atr[1]:
            G.append((atr[0], A))
    for i in range(len(G)):
        for B in G[i][0]:
            if G[i][1] in closure(G[i][0].replace(B, ''), F):
                lst_atr = list(G[i])
                lst_atr[0] = G[i][0].replace(B, '')
                atr_temp = tuple(lst_atr)
                G[i] = atr_temp
    counter = 0
    len_G = len(G)
    while len_G:
        atr = G[counter]
        G_ = G[:counter] + G[counter+1:]
        flug = True
        if atr[1] in closure(atr[0], G_):
            G = G_
            flug = False
        if flug:
            counter += 1
        len_G -= 1
    return G

# אלגוריתם לפירוק 3NF
def find_3NF_decomposition(R, F):
    G = compute_minimal_cover(F)
    res = []
    for atr in G:
        res.append(atr[0] + atr[1])
    keys = all_keys(R, F)
    flag = False
    for r in res:
        if ''.join(sorted(r)) in keys:
            flag = True
            break
    if not flag:
        res.append(keys[0])
    res2 = []
    for i in range(len(res)):
        res_1 = res[:i] + res[i+1:]
        is_subset = False
        for r in res_1:
            if not set(res[i]).issubset(set(r)):
                continue
            is_subset = True
        if is_subset:
            continue
        res2.append(res[i])
    return res2

# אלגוריתם לפירוק BCNF
def find_BCNF_decomposition(R, F):
    if is_in_bcnf(R,F):
        return R
    violation = ''
    for atr in F:
        if (not set(atr[1]).issubset(set(atr[0]))) and (not is_super_key(atr[0], F, R)):
            violation = atr
            break
    R_1 = closure(violation[0],F)
    R_2 = ''.join(set(violation[0]).union(set(R).difference(R_1)))
    return find_BCNF_decomposition(R_1,compute_dependencies_in_projection(R_1,F)), (find_BCNF_decomposition(R_2,compute_dependencies_in_projection(R_2,F)))


     

# F = [('a','b'),('abcd','e'),('ej','gh'),('acdj','eg')]

f1 = [('a', 'b'), ('acd', 'e'),('ej', 'g'),('ej', 'h'), ('acd', 'e'), ('acdj', 'g')]
r1 = 'acdj'
f2 = [('eg', 'ab'), ('gc', 'ae'),('ec', 'db'),('ab', 'cdg'), ('e', 'ag')]
f3 = [('bc', 'ade'), ('db', 'ace'),('c', 'ad'),('d', 'ce')]
r2 = "abcde"
str = ""
sub_r1 = ['ab', 'bc', 'cd']
f4 = [('a', 'b'), ('b', 'c'),('c', 'd'),('d', 'a')]
sub_r2 = ['abde', 'bec']
f5 = [('a', 'abcde'), ('bc', 'a'),('de', 'c')]
sub_r3 = ['abc', 'ad']
f6 = [('a', 'bc'), ('b', 'ad'),('c', 'd')]
sub_r4 = ['aeg', 'bce', 'cdeg']
f7 = [('bc', 'g'), ('ce', 'ad'),('eg', 'abd'),('ae', 'b'), ('cg', 'ae')]

r3 = 'abc'
r4 = 'ad'
f8 = [('ab', 'c'),('d', 'a')]

r5 = 'abce'
r6 = 'abcde'
f9 = [('eg', 'ab'), ('gc', 'ae'), ('ec', 'bd'), ('ab', 'cdg'), ('e','ag')]

# print(all_keys(r2,f3))
# print(compute_minimal_cover(f3))
# print(is_dependency_preserving(sub_r4, f7))
# ff = compute_dependencies_in_projection(r6, f9)
# print(ff)
# print(all_keys(r6, f9))
# print(is_in_bcnf(r6, ff))
# print(is_in_3nf(r6, ff))
# print(find_BCNF_decomposition(r6,f9))
print(is_dependency_preserving(['bcd', 'ace'], f3))


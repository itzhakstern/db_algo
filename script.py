f = [('ab', 'c'), ('c', 'da'), ('bd', 'c'), ('ad','b')]
r = 'abcd'


# F need be an array of tuples 
def closure(X, F):
    V = X
    len_v = len(V)
    while True:
        for atr in F:
            if set(atr[0]).issubset(set(V)) and not set(atr[1]).issubset(set(V)):
                V = ''.join(set(V+''.join(sorted(atr[1]))))
        if len_v == len(V):
            return V
        len_v = len(V)

# print(closure('c', f))


def super_key(X, F, R):
    V = closure(X, F)
    return sorted(V) == sorted(R) 

# print(super_key('al', f,r))

def minimize(X, F):
    for x in X:
        if x in closure(X.replace(x, ''), F):
            X = X.replace(x, '')
    return X

# print(minimize('bc', f))

def find_key(R, F):
    return minimize(R, F)


# print(find_key(r, f))

def all_keys(R, F):
    x = 0
    K = find_key(R, F)
    key_queue = [K]
    keys = [K]
    while len(key_queue):
        x += 1
        print(key_queue)
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
    return set(keys)

print(all_keys(r, f))

def is_in_bcnf(R, F):
    if len(R) == 2:
        return True
    pass


def is_in_3nf(R, F):
    if(is_in_bcnf(R, F)):
        return True
    pass


# אלגוריתם לחישוב שימור תלויות
def id_dependency_preserving(R, sub_R, F):
    pass

# אלגוריתם לחישוב קבוצת התלויות F_R_i
def compute_dependencies_in_projection(R, R_i, F):
    pass

# אלגוריתם למציאת כיסוי מינימלי
def compute_minimal_cover(F):
    pass

# אלגוריתם לפירוק 3NF
def find_3NF_decomposition(R, F):
    pass

# אלגוריתם לפירוק BCNF
def find_BCNF_decomposition(R, F):
    pass

import networkx as nx
import numpy as np

def dsatur(g,h):

    def saturasi(n,r,c):
        ls = {i: [] for i in range(n)} 
        for i in range(n):
            for j in range(n):
                if(r[i][j] <= 2 and c[j] != -1):
                    ls[i].append(c[j]) 
        uniq = []
        sat_node = []
        for i in range(n):
            uniq = set(ls[i])
            sat_node.append(len(uniq))
        return sat_node

    def maks_saturasi(n,c):
        sat_node = saturasi(n,r,c)
        ex = [i for i, nilai in enumerate(c) if nilai != -1]
        for i in range(n):
            if i in ex:
                sat_node[i]=0
        max_value = max(sat_node)
        index_max = [index for index, value in enumerate(sat_node) if value == max_value]
        index_max_sat = np.argmax(degrees[index_max])
        max_sat = index_max[index_max_sat]
        return max_sat

    def cek_duplikat_set(cc):
        seen_sets = set()
        for set_i in cc:
            set_tuple = tuple(set_i) 
            if set_tuple in seen_sets:
                return 1
            seen_sets.add(set_tuple)
        return 0

    q = nx.tensor_product(g, h)
    Q = nx.convert_node_labels_to_integers(q, first_label=0)
    a = nx.adjacency_matrix(Q)
    A = a.toarray()
    n = Q.order()
    T = nx.convert_node_labels_to_integers(q, first_label=1)
    t = T.nodes

    r = np.zeros((n,n))
    for i in range(n):
        for j in range(n):
            r[i][j] = nx.shortest_path_length(Q, i, j)
            
    degrees = np.sum(A, axis=1)
    
    c = [-1] * n
    
    p=1
    l=[]
    for i in range(n) :
        max_sat = maks_saturasi(n,c)
        if(c[max_sat]==-1):
            for j in range(n):
                if(r[max_sat][j] <= 2 and c[j] != -1):
                    l.append(c[j])
            for k in range(1, p+1):
                if(k not in l):
                    c[max_sat]=k
                    break
            if(c[max_sat]==-1):
                p=p+1
                c[max_sat]=p
        l=[] 

    t = np.array(t)
    t = t.reshape(-1, 1)
    c = np.array(c)
    c = c.reshape(-1, 1)
    s = np.concatenate((c, t), axis=1)
    ss = np.array(sorted(s, key=lambda x: x[0]))
    PI = np.split(ss[:,1], np.unique(ss[:,0], return_index=True)[1][1:])

    pi = []
    for i in range(n):
        rows = []
        for j in range(p):
            cols = []
            for k in PI[j]:
                cols.append(r[i][k-1])
            rows.append(cols)
        pi.append(rows)

    cc = []
    for i in range(n):
        col = []
        for j in range(p):
            col.append(min(pi[i][j]))
        cc.append(col) 

    cek = cek_duplikat_set(cc)

    kai_L = []
    for i in range(n):
        for j in range(n):
            if (i != j):
                if (cek == 1):
                    kai_L = 0
                    break
                if (cek == 0):
                    kai_L = p
    kai = []
    for i in range(n):
        for j in range(n):
            if (i != j):
                if (cek == 1):
                    kai = p
                    break
                if (cek == 0):
                    kai = 0
    return kai, kai_L
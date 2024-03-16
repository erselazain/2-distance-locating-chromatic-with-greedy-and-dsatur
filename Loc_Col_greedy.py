import networkx as nx
import numpy as np

def greedy(g,h):

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

    color=[-1]*n
    
    p=1
    l=[]
    for i in range(n):
        for j in range(n):
            if(r[i][j] <= 2 and color[j] != -1):
                l.append(color[j])
        for k in range(1, p+1):
            if(k not in l):
                color[i]=k
                break
        if(color[i]==-1):
            p=p+1
            color[i]=p
        l=[]

    t = np.array(t)
    t = t.reshape(-1, 1)
    c = np.array(color)
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
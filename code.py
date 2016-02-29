import pandas as pd
import numpy as np
import math

dire = 'C:/Users/richard.brooker/Documents/Aus_Journey_viz/'
dt = pd.read_csv(dire + 'Consumer Journey Raw Data.csv' )
order = dt.columns[2:87]
index = dt.columns[89:89+89]



vols = {f:{'c':0, 'i': 0 } for f in order}
edges = {}
for r in dt.iterrows():
    r1 = [ r[1][k] for k in order] 
    r2 = [ r[1][k] for k in index] 
    for i in range(85):
        s = order[i]
        if not math.isnan( r1[i] ):
            vols[s]['c'] += 1 
            vols[s]['i'] += float(r2[i].replace('%',''))
            if r1[i]+1 in r1:
                t = order[ r1.index(r1[i] + 1) ]
                if (s,t) in edges: 
                    edges[(s,t)] += 1
                    print((s,t))
                else: edges[(s,t)] = 1
                
edges = [[k[0],k[1],edges[k]] for k in edges]
edges = pd.DataFrame(edges, columns=['Source','Target','Weight'])
edges['s_rank'] = edges.groupby('Source')['Weight'].rank(ascending=False)
edges['t_rank'] = edges.groupby('Target')['Weight'].rank(ascending=False)
edges['rank'] = edges.apply( lambda x: min(x['s_rank'],x['t_rank']) , axis=1)
edges['Type'] = "Directed"
edges.to_csv(dire+'edge_table.csv') 

vols = [ [f,f,vols[f]['c'], vols[f]['i'], vols[f]['i']/vols[f]['c'] ] for f in vols]

vols =  pd.DataFrame(vols,columns=['Id','Label','Count','Influence','AvgInfluence'])
vols.to_csv(dire+'node_table.csv') 
    
    
    
    
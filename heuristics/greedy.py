import numpy as np

def greedy_path(dist_matrix,start):

    ind = list()
    ind.append(start)
    
    for v in range(len(dist_matrix[0])-1):
        while(True):
            n = np.argmin(dist_matrix[ind[-1]])
            if n in ind:
                dist_matrix[ind[-1]][int(n)] = np.inf
            else:  
                ind.append(int(n))
                break
            
    return ind
    
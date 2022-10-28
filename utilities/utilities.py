import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from heuristics.AGSimple import AGSimple
import itertools as it
from tqdm import tqdm

def txt2matrix(path: str) -> list:
    with open(path,'r') as f:
        matrix = [list(map(int,line.strip().split(sep=" "))) for line in f.readlines()]
    return matrix

def load_tsp(path: str) -> tuple:
    dist_matrix = np.array(txt2matrix(path))
    return dist_matrix

def plot_results(path_results, path_fig):
    data = pd.read_csv(path_results)   
    data_mean = data.groupby(by=["n_gen|n_ind|mutate_rate"])['best'].mean().reset_index()
    
    best_parameter = data_mean.min()['n_gen|n_ind|mutate_rate']
    data_parameter = data[data["n_gen|n_ind|mutate_rate"] == best_parameter]
    it_ls = data_parameter.groupby(by="it").agg({"best": lambda x: list(x)})

    for lst in it_ls['best']:
        plt.plot(range(len(it_ls['best'][0])),lst)

    plt.title(f"Best parameter: {best_parameter}")
    plt.xlabel("Generation")
    plt.ylabel("Fitness")
    plt.savefig(path_fig)

def AGSimple_simulate(path_results, dist_matrix, n_gen, n_ind, mutate_rate):
    
    with open(path_results,"w") as f:
        f.write("n_gen|n_ind|mutate_rate,it,gen,best\n")

    for n_gen,n_ind,mutate_rate in tqdm(it.product(n_gen,n_ind,mutate_rate),desc="Runing genetics "):
        for i in range(10):
            AGSimple(dist_matrix,n_gen,n_ind,mutate_rate,i).simulate(path_results)
    pass
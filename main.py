from utilities.utilities import AGSimple_simulate, load_tsp
from utilities.utilities import plot_results

def main():
    path_matrix = "matrix_examples/sgb128_dist.txt"
    path_results = "results_normal.csv"
    path_fig = "results_normal.png"

    dist_matrix = load_tsp(path_matrix)

    mutate = [i/100 for i in range(1,21)]
    ind = [20, 50, 100]
    gen = [20, 50, 100]

    AGSimple_simulate(path_results, dist_matrix, gen, ind, mutate)

    plot_results(path_results,path_fig)

if __name__ == "__main__":
    main()
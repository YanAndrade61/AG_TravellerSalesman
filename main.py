from utilities.utilities import AGSimple_simulate, load_tsp
from utilities.utilities import plot_results

def main():
    path_matrix = "matrix_examples/lau15_dist.txt"
    path_results = "results.csv"
    path_fig = "results.png"

    dist_matrix = load_tsp(path_matrix)

    mutate = [i/100 for i in range(1,21)]
    ind = [20]
    gen = [20]

    AGSimple_simulate(path_results, dist_matrix, gen, ind, mutate)

    plot_results(path_results,path_fig)

if __name__ == "__main__":
    main()
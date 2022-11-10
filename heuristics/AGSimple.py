import numpy as np
import random
from heuristics.greedy import greedy_path

class AGSimple:

    def __init__(self,dist: list(), n_ind: int = 20, n_gen: int = 500, mutate_rate: float = 0.1,greedy_rate: float = 0, i: int=0):
        self.dist = dist
        self.n_cities = len(dist[0])
        self.n_ind = n_ind
        self.n_gen = n_gen
        self.mutate_rate = mutate_rate
        self.greedy_rate = greedy_rate
        self.i = i

    def simulate(self,path_results) -> None:
        
        individuals = [np.random.choice(self.n_cities, self.n_cities, replace=False) 
                        for i in range(self.n_ind)]
                
        # % dos individuos sao inicializados por um caminho guloso
        greedy_starts = np.random.choice(self.n_cities, int(self.n_ind*self.greedy_rate), replace=False) 
        for i,start in enumerate(greedy_starts):
            individuals[i] = np.array(greedy_path(self.dist.copy(),start))

        estagna = 0
        best = 0
        for i in range(self.n_gen):
            
            fitness_lst = self.fitness(individuals)        
            
            parents = self.tournament_selection(fitness_lst)
            
            new_ind = self.ox_cross(individuals,parents)
            
            if estagna >= 100:
                new_ind = self.mutate_pos(new_ind)
                estagna=0
            else:
                new_ind = self.mutate_ind(new_ind)

            menor = np.argmin(fitness_lst)
            
            new_ind[0] = individuals[menor]
            if (best == fitness_lst[menor]):
               estagna += 1
            else:
                best = fitness_lst[menor]
                estagna = 0 
            
            with open(path_results,"a") as f:
                print(f"{self.n_gen}|{self.n_ind}|{self.mutate_rate},{self.i},{i},{fitness_lst[menor]}",file=f)

            individuals = np.array(new_ind)
            # print(f"GEN: {i}, Best: {fitness_lst[menor]}")
            
        return individuals[menor]
        

    def fitness(self, ind : list) -> list:
        fitness_lst = []
        for i in range(self.n_ind):

            dist_ind = [self.dist[ind[i][j-1]][ind[i][j]] for j in range(self.n_cities)]
            fitness_lst.append(sum(dist_ind))

        return fitness_lst
    
    def tournament_selection(self,fitness : list) -> list:
        parents = []
        for i in range(self.n_ind):
            while True:
                choosen = np.random.choice(self.n_ind,2,replace=False)
                best = choosen[np.argmin([fitness[j] for j in choosen])]
                if (i % 2 != 0) or (i == 0) or best != parents[-1]:
                    parents.append(best)
                    break
        return parents
    
    def ox_cross(self,individuals: list,parents: list):
        new_individuals = []
        for i in range(0,self.n_ind,2):
            a = individuals[parents[i]]
            b = individuals[parents[i+1]]

            point1 = random.randint(1,self.n_cities-2)
            point2 = random.randint(point1,self.n_cities-1)
            
            a_reorder = np.concatenate([a[point2:],a[:point2]])
            b_reorder = np.concatenate([b[point2:],b[:point2]])

            new_ind1 = [-1]*self.n_cities
            new_ind2 = [-1]*self.n_cities
            
            new_ind1[point1:point2] = b[point1:point2]
            new_ind2[point1:point2] = a[point1:point2]
            
            cross_list = [(a_reorder,new_ind1),(b_reorder,new_ind2)]
            for parent,new_ind in cross_list:
                cont = point2
                for n in parent:
                    if cont == len(a):
                        cont=0
                    if n not in new_ind:
                        new_ind[cont] = n
                        cont += 1

            new_individuals.append(new_ind1)
            new_individuals.append(new_ind2)

        return new_individuals

    def mutate_ind(self,individuals: list):
        
        for i in range(self.n_ind):
            rate = random.random()
            if rate <= self.mutate_rate:
                pos1,pos2 = np.random.choice(self.n_cities, 2, replace=False)
                individuals[i][pos1],individuals[i][pos2] = individuals[i][pos2],individuals[i][pos1]
    
        return individuals
    
    def mutate_pos(self,individuals: list):
        
        for i in range(self.n_ind):
            for j in range(self.n_cities):
                rate = random.random()
                if rate <= self.mutate_rate:
                    pos1 = np.random.choice(self.n_cities, 1, replace=False)
                    individuals[i][j],individuals[i][pos1[0]] = individuals[i][pos1[0]],individuals[i][j]
    
        return individuals
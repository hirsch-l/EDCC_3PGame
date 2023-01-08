#Evolutionary Dynamics of Coordinated Cooperation



import random
from math import *
import matplotlib.pyplot as plt


class Network :
    def __init__(self):
        self.network_nodes = []

        self.current_state = [0,0,0,0]


class Node :

    def __init__(self):
        self.number = None #every Node is initialized with None, later they get assigned their real number
        self.strategy = None #going to be C0, C1, C2, or C3
        self.neighbors = []




def network_initialization(Size):

    random.seed()




    network = Network()

    for i in range(Size):
        node = Node()
        node.number = i
        network.network_nodes.append(node)


    for i in range(Size):

        strat = random.randint(0,3)
        strat_associated = False
        while not strat_associated:
            if network.current_state[strat] < Size/4:
                network.network_nodes[i].strategy = strat
                network.current_state[strat] += 1
                strat_associated = True
            else:
                strat = random.randint(0, 3)

    return network






def update_mechanism(k,l,network,beta, r, p, c):
    # k and l are the nodes


    i = network.network_nodes[k].strategy
    j = network.network_nodes[l].strategy

    A = [[-c+r*c,-c+r*c,-c+r*c,-c+(2/3)*r*c,-c+r*c,-c+r*c,-c+(2/3)*r*c,-c+((p**2+p+1)/3)*r*c,-c+(1/3)*r*c,-c+(1/3)*r*c],
         [-c+r*c,-c+r*c,-c+r*c,-c+(2/3)*r*c,p*(2-p)*(-c+r*c),(p*(3-p)/2)*(-c+r*c),-(p*(3-p)/2)*c+(p*(3-p)/2)*r*c,(p*(1+p)/2)*(-c+r*c),0,0],
         [-c+r*c,-c+r*c,-(p*(1+p)/2)*c+(p**2+p+1)*r*c/3,(1/3)*r*c,(p*(3-p)/2)*(-c+r*c),(p*(1+p)/2)*(-c+r*c),0,(p**2)*(-c+r*c),0,0],
         [(2/3)*r*c,(2/3)*r*c,(1/3)*r*c,(1/3)*r*c,(p*(3-p)/3)*r*c,0,0,0,0,0]]



    fitness_i = (((network.current_state[0])**2)*A[i][0] + network.current_state[0]*network.current_state[1]*A[i][1] +
                 network.current_state[0]*network.current_state[2]*A[i][2] + network.current_state[0]*network.current_state[3]*A[i][3]
                 + network.current_state[1]*network.current_state[1]*A[i][4] + network.current_state[1]*network.current_state[2]*A[i][5]
                 + network.current_state[1]*network.current_state[3]*A[i][6] + network.current_state[2]*network.current_state[2]*A[i][7]
                 + network.current_state[2]*network.current_state[3]*A[i][8] + network.current_state[3]*network.current_state[3]*A[i][9])/(len(network.network_nodes))**2

    fitness_j = (((network.current_state[0])**2)*A[j][0] + network.current_state[0]*network.current_state[1]*A[j][1] +
                 network.current_state[0]*network.current_state[2]*A[j][2] + network.current_state[0]*network.current_state[3]*A[j][3]
                 + network.current_state[1]*network.current_state[1]*A[j][4] + network.current_state[1]*network.current_state[2]*A[j][5]
                 + network.current_state[1]*network.current_state[3]*A[j][6] + network.current_state[2]*network.current_state[2]*A[j][7]
                 + network.current_state[2]*network.current_state[3]*A[j][8] + network.current_state[3]*network.current_state[3]*A[j][9])/(len(network.network_nodes))**2

    probability_ij = (1 + exp(beta * (fitness_i - fitness_j)))**(-1)




    r = random.uniform(0,1)

    if r <= probability_ij:
        network.network_nodes[k].strategy = j
        network.current_state[i] -= 1
        network.current_state[j] += 1



def game_simulation(size,r,p,c,beta):



    random.seed()

    strategy_frequencies = [None for i in range(36)]

    network1 = network_initialization(size)
    for i in range(36):
        #network1 = network_initialization(size)
        for j in range(len(network1.network_nodes)):
                q = random.randint(0, len(network1.network_nodes)-1)
                update_mechanism(j,q, network1, beta,r,p,c)
        strategy_frequencies[i] = [network1.current_state[0]/len(network1.network_nodes),
                                   network1.current_state[1]/len(network1.network_nodes),
                                   network1.current_state[2]/len(network1.network_nodes),
                                   network1.current_state[3]/len(network1.network_nodes)]

    return strategy_frequencies






if __name__ == "__main__":

    size = 36
    r = 2.5
    p = 0.5
    c = 1
    beta = [10**(-3),10**(-2),10**(-1),10**(0),10**(1),10**(2),10**(3)]
    res = []

    for l in range(len(beta)):
        average_generations = [0,0,0,0]
        for k in range(10**3):
            game_sim = game_simulation(size,r,p,c, beta[l])
            average_stat_dist = [0,0,0,0]
            for i in range(len(game_sim)):
                for j in range(4):
                    average_stat_dist[j] += game_sim[i][j]/len(game_sim)
            for t in range(4):
                average_generations[t] += average_stat_dist[t]/10**3
        res.append(average_generations)

    print(res)

    x_axis = [10**(-3),10**(-2),10**(-1),10**(0),10**(1),10**(2),10**(3)]
    y_axisC0 = []
    y_axisC1= []
    y_axisC2= []
    y_axisC3= []
    for i in range(len(res)):
        y_axisC0.append(res[i][0])
        y_axisC1.append(res[i][1])
        y_axisC2.append(res[i][2])
        y_axisC3.append(res[i][3])



    fig, ax = plt.subplots(figsize=(10, 5))


    ax.plot(x_axis,y_axisC0,'b')
    ax.plot(x_axis, y_axisC1, 'g')
    ax.plot(x_axis, y_axisC2, 'y')
    ax.plot(x_axis, y_axisC3, 'r')

    ax.legend(["C0","C1","C2","C3"], frameon=False)

    ax.set_ylabel('Time-averaged frequency')
    ax.set_xlabel('intensity of selection')
    ax.set_xscale('log')

    plt.show()



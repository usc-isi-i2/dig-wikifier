import random, json
class Graph():
    def __init__(self, G):
        """
        :param G: A dictionary representing the graph edges
        """
        self.G = G

    def printProgressBar(self, iteration, total, prefix='', suffix='', decimals=1, length=100, fill='█'):
        """
        Call in a loop to create terminal progress bar
        @params:
            iteration   - Required  : current iteration (Int)
            total       - Required  : total iterations (Int)
            prefix      - Optional  : prefix string (Str)
            suffix      - Optional  : suffix string (Str)
            decimals    - Optional  : positive number of decimals in percent complete (Int)
            length      - Optional  : character length of bar (Int)
            fill        - Optional  : bar fill character (Str)
        """
        percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
        filledLength = int(length * iteration // total)
        bar = fill * filledLength + '-' * (length - filledLength)
        print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end='\r')
        # Print New Line on Complete
        if iteration == total:
            print()

    def random_walk(self, n_walks=100, steps=5,out_file="random_walk.txt"):
        """
        :param n_walks : number of random walks to perform per node
        :param steps : length of each single random walk
        
        This function generates random walks for the given graph, depending on the parameters entered. It will store the walks in a file called randomwalk.txt
        """
         
        walks = []
        ct = 0
        walks_file = open(out_file,"w")
        for _ in range(n_walks):
            nodes = list(self.G.keys())
            random.shuffle(nodes)

            for node in nodes:
                self.printProgressBar(iteration=ct, total=n_walks * len(nodes), prefix='Progress:', suffix='Complete', length=50)
                #print(" {}/{} walks completed ".format(len(walks), n_walks * len(nodes)))
                walk = [node]
                s = 0
                backtrack = dict()
                backtrack[node] = None
                while s < steps:
                    curr = walk[-1]
                    edges = self.G[curr] if curr in self.G.keys() else {}
                    if not edges:
                        walks.append(walk)
                        break 
                    choice = random.choices(population=['up','backtrack','forward'], weights=[0.2,0.3,0.5])[0]
                    if choice == 'up':
                        if 'P31' not in edges.keys():
                            # print("P31 was not in keys {}:{}".format(curr, edges.keys()))
                            choice = 'forward'
                        else:
                            options = edges['P31']
                            if not options:
                                s+=1
                                continue
                            nxt = random.choice(options)
                            walk.append('P31')
                            walk.append(nxt)
                            backtrack[nxt] = curr
                    if choice == 'backtrack':
                        if len(walk) < 3 or backtrack[curr] == None:
                            choice = 'forward'
                        else:
                            # Go back a step
                            p = backtrack[curr]
                            # print("Backtracked from {} to {}".format(curr,p))
                            # get neighbors for this node
                            p_edges = self.G[p]
                            options = [x for x in p_edges.keys() if x != 'P31']
                            if not options:
                                s+=1
                                continue
                            # choosing an option to go forward
                            _choice = random.choice(options)
                            # Go forward in one of the qnodes for that property
                            qnode = random.choice(p_edges[_choice])
                            walk.append(_choice)
                            walk.append(qnode)
                            backtrack[qnode] = p

                    if choice == 'forward':
                        # get options
                        options = [x for x in edges.keys() if x != 'P31']
                        # print("options were {}".format(options))
                        if not options:
                            s+=1
                            continue
                        # choosing an option to go forward
                        _choice = random.choice(options)
                        # print("Chose property {}".format(_choice))
                        # Go forward in one of the qnodes for that property
                        qnode = random.choice(edges[_choice])
                        walk.append(_choice)
                        walk.append(qnode)
                        backtrack[qnode] = curr
                    s+=1
                #walks.append(walk)
                ct+=1
                walks_file.write(' '.join(walk) + '\n')
        return walks



if __name__ == "__main__":
    # Set the json format graph file here
    with open('film-data-exp2/film_graph_2.json','r') as fin:
        data = json.load(fin)
    walker = Graph(data)
    all_walks = walker.random_walk()
    #out_file = open('film-data-exp2/random_walk.txt','w')
    #for walk in all_walks:
    #    out_file.write(' '.join(walk) + '\n')
    print("Done")
    exit(0) 
    

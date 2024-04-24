import numpy as np
import random
import matplotlib.pyplot as plt

class Grid:
    def __init__(self, p, q, size = 50, empty = 0.1):
        self.grid = np.zeros((size, size))

        self.size = size
        self.p = p
        self.q = q

        total_agents = int(size*size*(1-empty))
        agent_dist = (int(q*size*size), total_agents-int(q*size*size))

        # populate grid with type 1
        for _ in range(agent_dist[0]):

            x = np.random.randint(size)
            y = np.random.randint(size)

            # make sure we're adding at an empty spot
            while self.grid[x, y] != 0:
                x = np.random.randint(size)
                y = np.random.randint(size)

            self.grid[x, y] = 1

        # populate grid with type 2
        for _ in range(agent_dist[1]):

            x = np.random.randint(size)
            y = np.random.randint(size)

            # make sure we're adding at an empty spot
            while self.grid[x, y] != 0:
                x = np.random.randint(size)
                y = np.random.randint(size)

            self.grid[x, y] = 2

    def get_sim_pct(self, x, y, t = 0):
        total = 0
        similar = 0

        if not t:
            t = self.grid[x, y]

        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:

                # make sure not out of bounds
                if 0 <= x+dx < self.size:
                    if 0 <= y+dy < self.size:

                        # account for dx = dy = 0
                        if not(dx == 0 and dy == 0):
                            total += 1

                            if self.grid[x+dx, y+dy] == t:
                                similar += 1

        return similar/total
    
    def get_avg_sim(self):

        total = 0
        count = 0

        for x in range(self.size):
            for y in range(self.size):

                count += 1
                total += self.get_sim_pct(x, y)

        return total/count
    
    def is_unsatisfied(self, x, y):
        return self.get_sim_pct(x, y) < self.p and self.grid[x, y]
    
    def get_unsatisfied(self):

        result = []

        for x in range(self.size):
            for y in range(self.size):

                if self.is_unsatisfied(x, y):
                    result.append((x, y))

        return result
    
    def get_dist_cells(self, x, y, distance):

        if distance == 0:
            return [(x, y)]
        
        result = []

        for dx in [-distance, distance]:
            for dy in range(-distance, distance):

                # make sure not out of bounds
                if 0 <= x+dx < self.size:
                    if 0 <= y+dy < self.size:
                        result.append((x+dx, y+dy))

        for dy in [-distance, distance]:
            for dx in range(-distance, distance):

                # make sure not out of bounds
                if 0 <= x+dx < self.size:
                    if 0 <= y+dy < self.size:
                        result.append((x+dx, y+dy))

        return result
    
    def find_nearest_empty(self, x, y):

        found = False
        d = 0

        while not found and d < self.size:
            cells = self.get_dist_cells(x, y, d)

            for cell in cells:
                if self.grid[cell] == 0 and self.get_sim_pct(cell[0], cell[1], self.grid[x, y]) > self.p:
                    found = True
                    return cell
                
            d += 1

    def step(self):

        unsatisfied = self.get_unsatisfied()

        if not unsatisfied:
            print('reached equilibrium')
            return False
        
        agent = random.choice(unsatisfied)
        # print(f'agent:{agent}')
        x, y = agent

        empty = self.find_nearest_empty(x, y)

        if not empty:
            print('no equilibrium')
            return False
        
        # print(f'empty{empty}')
        self.grid[empty] = self.grid[agent]
        self.grid[x, y] = 0

        return True
    
    def simulate(self, max_steps = None):

        if not max_steps:
            max_steps = float('inf')

        steps = 0
        flag = True
        while flag and steps < max_steps:
            flag = self.step()
            # print(f'step: {steps}')
            steps += 1

        if steps == max_steps:
            print('reached max_steps')

        return self.grid



        
if __name__ == '__main__':
    results = []

    n = 100
    for i in range (0, n+1):
        p = i/n
        grid = Grid(p, 0.5)
        grid.simulate(1000)
        results.append(grid.get_avg_sim())

    plt.title('Average Similarity Percentage Across \n Neighborhoods vs. Intolerance (p) with q = 0.5')
    plt.ylabel('Average Similarity Across Neighborhoods')
    plt.xlabel('p')
    plt.plot(np.arange(0, n+1)/n, results, label = 'q = 0.5')
    plt.show()
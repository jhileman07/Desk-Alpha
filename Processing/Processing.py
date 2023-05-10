import math
import numpy as np
import time
import matplotlib.pyplot as plt

class Var_sampler:
    # alpha is how much you want variability to matter, measured 0-1.
    # beta is where you want the cutoff for variable sampling to be, measured as a percent tolerance in price standard deviation.
    # base rate is how many times per second you want the sample to be taken.
    def __init__(self, base_rate, alpha, beta, sample, lookback):
        self.base_rate = base_rate
        self.alpha = alpha
        self.beta = beta
        self.sample = sample
        self.previous_sample_time = 0
        self.lookback = lookback
        self.sampled = np.array([])

    def run(self, runtime):
        start_time = time.time()
        while time.time() - start_time < runtime:
            history = self.sampled[-self.lookback:]
            if time.time() - self.previous_sample_time >= 1/self.base_rate:
                self.add_sample()
            elif (len(self.sampled) > self.lookback) and (np.std(history)/np.mean(history) > self.beta):
                self.add_sample()
            else:
                pass
                
    def add_sample(self):
        self.sampled = np.append(self.sampled, self.sample())
        self.previous_sample_time = time.time()

def main():
    vs = Var_sampler(10, 0.5, 0.1, lambda: np.random.normal(100, 10), 10)
    vs.run(10)
    plt.plot(vs.sampled)
    plt.show()
    print("done")

if __name__ == '__main__':
    main()
    

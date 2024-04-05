import numpy as np
from configs.params import get_assigner
from configs.draw import draw
from commons.functions import config_logger
import logging


def main():

    N = 25                  # Time-horizon
    n = 2                   # System dynamics

    TA, LG, LL = get_assigner(N, n)     # TA: the task assigner
    tlg, slg = LG                       # LG: the list of global specifications (slg) and its time list (tlg) 
    tll, sll = LL                       # LG: the list of local specifications (sll) and its time list (tlg)

    # The list of global specifications

    config_logger(logging, 'INFO.log')
    for t in range(N):

        if t in tlg:
            TA.assign_global(t, slg[tlg.index(t)])
        
        if t in tll:
            TA.assign_local(t, sll[tll.index(t)])
        
        TA.update_control(t)

    meas = {}
    for name, agent in TA.agents.items():
        meas[name] = agent.xx

    return TA.agents, meas


if __name__ == "__main__":

    # Set random seed       
    np.random.seed(3)
    agents, meas = main()
    draw(agents, meas)
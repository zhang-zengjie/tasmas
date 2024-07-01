from probstlpy.benchmarks.common import inside_rectangle_formula, outside_rectangle_formula
import numpy as np
from components.agent import Agent
from components.assigner import Assigner
from probstlpy.systems.linear import LinearSystem


# Areas of interest

SAFETY = (0, 40, 0, 40)

HOME_A = (0, 10, 0, 5)
HOME_B = (10, 20, 0, 5)
HOME_C = (20, 30, 0, 5)
HOME_D = (30, 40, 0, 5)

CASE_1 = (0, 10, 35, 40)
CASE_2 = (10, 20, 35, 40)
CASE_3 = (20, 30, 35, 40)
CASE_4 = (30, 40, 35, 40)

OBSTACLE_1 = (10, 18, 16, 24)
OBSTACLE_2 = (22, 30, 16, 24)

HOMES = {'T-A': HOME_A, 'T-B': HOME_B, 'T-C': HOME_C, 'T-D': HOME_D}
CASES = {'GP-I': CASE_1, 'GP-II': CASE_2, 'GP-III': CASE_3, 'GP-IV': CASE_4}
OBSTACLES = {'B-1': OBSTACLE_1, 'B-2': OBSTACLE_2}

LOAD = (34, 40, 17, 23)


def safe_spec(n, N):

    mu_safety = inside_rectangle_formula(SAFETY, 0, 1, n)
    for obstacle in OBSTACLES.values():
        mu_safety &= outside_rectangle_formula(obstacle, 0, 1, n)
    phi_safety = mu_safety.always(0, N)
    phi_safety.name = "SAFETY"

    return phi_safety


def fetch_spec(t, T, n, via, goal, name):

    # t: the starting time of the task
    # T: the time interval needed for a task unit

    mu_case = inside_rectangle_formula(via, 0, 1, n)
    not_mu_case = outside_rectangle_formula(via, 0, 1, n)
    mu_load = inside_rectangle_formula(goal, 0, 1, n)

    from_case_to_load = not_mu_case | mu_load.eventually(0, T)
    fetch = mu_case.eventually(t, t + T) & from_case_to_load.always(t, t + T)
    fetch.name = name

    return fetch


def go_home(t, T, n, home, name):

    mu_home = inside_rectangle_formula(home, 0, 1, n)
    go_home = mu_home.always(0, 2).eventually(t, t+T-2)
    go_home.name = name
    return go_home


class agent_specs:

    def __init__(self, n, N):

        self.safety = safe_spec(n, N)
        # The time list of global specifications 
        self.tlg = [2, 8]
        # The list of global specifications
        self.slg = [[fetch_spec(self.tlg[0], 7, 2, CASES['GP-I'], LOAD, 'FETCH GP-I'), fetch_spec(self.tlg[0]+1, 7, 2, CASES['GP-II'], LOAD, 'FETCH GP-II'), fetch_spec(self.tlg[0]+2, 7, 2, CASES['GP-IV'], LOAD, 'FETCH GP-IV')],
            [fetch_spec(self.tlg[1], 7, 2, CASES['GP-III'], LOAD, 'FETCH GP-III'), fetch_spec(self.tlg[1]+1, 7, 2, CASES['GP-II'], LOAD, 'FETCH GP-II')]]

        # The time list of local specifications 
        self.tll = [15]
        # The list of local specifications
        self.sll = [{0: go_home(self.tll[0], 10, 2, HOME_A, 'BACK TO T-A'),
                1: go_home(self.tll[0], 10, 2, HOME_B, 'BACK TO T-B'),
                2: go_home(self.tll[0], 10, 2, HOME_C, 'BACK TO T-C'),
                3: go_home(self.tll[0], 10, 2, HOME_D, 'BACK TO T-D')}
            ]

        # LG: the list of global specifications (slg) and its time list (tlg) 
        # LG: the list of local specifications (sll) and its time list (tlg)

class agent_model:

    def __init__(self, n):

        self.A = np.eye(n)
        self.B = np.eye(n)
        self.C = np.eye(n)
        self.D = np.zeros([n, n])

        # Disturbance variables
        self.mu = np.zeros(n)
        self.Sigma = 0.01 * np.eye(n)

        # Initialize System
        self.sys = LinearSystem(self.A, self.B, self.C, self.D, self.mu, self.Sigma)

        # Quadratic Cost function (nonzero & SPD)
        self.Q = np.eye(self.sys.n) * 0.001
        self.R = np.eye(self.sys.m) * 0.001

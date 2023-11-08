import math
import random
import numpy as np
import pyttsx3
from constant import num_of_system


def init_workers(start, stop, length):
    random_list = random.sample(range(start, stop + 1), length)
    return random_list


def postprocess(group_efficiency, times_of_epsilon):
    group_efficiency = group_efficiency / times_of_epsilon
    return group_efficiency


def mcs_init(num_of_group):
    relation_total = np.zeros(num_of_system)
    relation_n = np.zeros(num_of_system)
    relation_pre = np.zeros(num_of_system)
    p_co_ability = np.zeros(num_of_system)
    p_si_ability = np.zeros(num_of_system)
    person_efficiency = np.zeros(num_of_system)  # 工人个体效能估计值，用于贪心算法，找到高效能工人的编号
    person_efficiency_n = np.zeros(num_of_system)  # 工人个体效能估计值，用于贪心算法，找到高效能工人的编号
    group_efficiency = 0.0
    selected_workers = init_workers(0, num_of_system - 1, num_of_group)
    min_index = np.zeros(num_of_group)  # 群组里效能的倒序，用于找到低效能工人的位置并替换
    return relation_total, relation_n, relation_pre, p_co_ability, p_si_ability, selected_workers, person_efficiency, person_efficiency_n, group_efficiency, min_index


def normalization(x):  # 归一化函数
    dif = max(x) - min(x)
    min_x = min(x)
    if dif == 0:
        return x
    else:
        for i in range(num_of_system):
            x[i] = (x[i] - min_x) / dif
    return x


def epsilon_make(times):
    if times == 0:
        epsilon = 1
    else:
        epsilon = 1 / math.sqrt(times)
    return epsilon

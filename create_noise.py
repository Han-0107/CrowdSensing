import numpy as np
import random


# 人数越多噪声越大 任务次数越少噪声越大

def increase_raise_co(co_ability, task):
    co_len = len(co_ability)
    sequence = [round(random.uniform(-2, 2), 3) for _ in range(co_len)]
    sequence = np.array(sequence)
    # 可调节的重要参数
    if task < 101:
        sequence = sequence * 0.02 * np.log(task)
    elif task < 151:
        sequence = sequence * 0.04 * np.sqrt(task)
    elif task < 201:
        sequence = sequence * 0.04 * np.sqrt(2 * task)
    elif task < 251:
        sequence = sequence * 0.05 * np.sqrt(2 * task)
    else:
        sequence = sequence * 0.06 * np.sqrt(2 * task)
    co_ability = co_ability + sequence
    co_ability[co_ability < 0] = -co_ability[co_ability < 0] - np.floor(-co_ability[co_ability < 0])
    return co_ability


def increase_raise_si(si_ability):
    si_len = len(si_ability)
    sequence = np.random.normal(0, 0.2, si_len)
    return si_ability + sequence

import numpy as np
import random
import math
import functions
import create_noise
from constant import si_ability
from constant import co_ability
from constant import num_of_system

# 换人比例
change_rate = 0.2


class worker:
    def __init__(self, num):
        self.mu = si_ability[num]
        self.sigma = 0.01

    def person_work(self):
        worker_result = np.random.normal(self.mu, self.sigma, 1)
        return worker_result


def group_work(workers, num_of_group):
    group_result = 0
    person_result = np.zeros(num_of_group)
    for i in range(num_of_group):
        for j in range(num_of_group):
            if i != j:
                # print("workers:",workers)
                # print("worker:",workers[i])
                # print("worker: i=",i,":","worker(worker[i])=",si_ability[workers[i]]," then=",worker(workers[i]).person_work())
                # person_result[i] += worker(workers[i]).person_work() * (co_ability[j])
                person_result[i] += worker(workers[i]).person_work() * (co_ability[j])
        person_result[i] = person_result[i] / (num_of_group - 1)
        group_result += person_result[i]
    group_result = group_result / num_of_group
    return group_result, person_result


def group_work_with_noise(workers, num_of_group, task):
    group_result = 0
    person_result = np.zeros(num_of_group)
    now_co_ability = create_noise.increase_raise_co(co_ability, task)
    for i in range(num_of_group):
        for j in range(num_of_group):
            if i != j:
                # print("workers:",workers)
                # print("worker:",workers[i])
                # print("worker: i=",i,":","worker(worker[i])=",si_ability[workers[i]]," then=",worker(workers[i]).person_work())
                person_result[i] += worker(workers[i]).person_work() * (now_co_ability[j])
        person_result[i] = person_result[i] / (num_of_group - 1)
        group_result += person_result[i]
    group_result = group_result / num_of_group
    return group_result, person_result


def do_task(num_choice, pos_choice, selected_workers, num_of_group):
    # print("selected workers",selected_workers)
    # print("pos_choice",pos_choice)
    # print("num_choice",num_choice)
    for k in range(int(num_of_group * change_rate)):
        selected_workers[int(pos_choice[k])] = int(num_choice[k])
    result = group_work(selected_workers, num_of_group)
    return result


def do_task_with_noise(num_choice, pos_choice, selected_workers, num_of_group, task):
    # print("selected workers",selected_workers)
    # print("pos_choice",pos_choice)
    # print("num_choice",num_choice)
    for k in range(int(num_of_group * change_rate)):
        selected_workers[int(pos_choice[k])] = int(num_choice[k])
    result = group_work_with_noise(selected_workers, num_of_group, task)
    return result


# selected_workers为当前群组内的工人，由个人能力从小到大排序
# p_si_ability_rank为当前平台估计的工人个人能力排名，数组内为工人编号
def system_work_e(epsilon, min_index, selected_workers, person_efficiency, person_efficiency_n, num_of_group):
    pos_choice = np.zeros(num_of_group)
    num_choice = np.zeros(num_of_group)
    # print("person_efficiency:", person_efficiency)
    person_efficiency = person_efficiency / person_efficiency_n
    person_efficiency[np.isnan(person_efficiency)] = 0
    # print("person_efficiency:", person_efficiency)
    person_efficiency_sort = np.argsort(person_efficiency)
    # print(person_efficiency_sort)
    for i in range(int(num_of_group * change_rate)):
        pos_choice[i] = min_index[i]
        if random.random() < epsilon:
            # 随机选
            new_worker = random.randint(0, (num_of_system - 1))
            while (new_worker in selected_workers):
                new_worker = random.randint(0, (num_of_system - 1))
                # print("new:",new_worker)
            num_choice[i] = new_worker
        else:
            # 选能力好的
            j = -(i + 1)
            while person_efficiency_sort[j] in selected_workers:
                j -= 1
            # num_choice[i] = 1
            num_choice[i] = person_efficiency_sort[j]
    result = do_task(num_choice, pos_choice, selected_workers, num_of_group)
    return result


def system_work_m(epsilon, min_index, person_efficiency, person_efficiency_n, selected_workers, person_co, times,
                  num_of_group, new_z, new_beta):
    pos_choice = np.zeros(num_of_group)
    num_choice = np.zeros(num_of_group)
    # print("person_efficiency:", person_efficiency)
    person_efficiency = person_efficiency / person_efficiency_n
    person_efficiency[np.isnan(person_efficiency)] = 0
    # print("person_efficiency:", person_efficiency)
    # print("person_co:", person_co)
    person_efficiency_sort = np.argsort(person_efficiency)
    # beta [-3: 1: 0]
    Regulatory_factor = float(1 / (1 + math.exp(- times + new_beta)))  # 调节因子，当times的原点位置不加以修正的时候，达到了更好的效果
    # 对person_efficiency和person_co进行归一化，并组合出一个“综合能力”用于贪心算法的选择
    person_co_n = functions.normalization(person_co)
    person_co_n = np.array(person_co_n)
    person_efficiency_n = functions.normalization(person_efficiency)
    person_efficiency_n = np.array(person_efficiency_n)
    # z [0.4: 0.2: 1]
    person_comprehensive = (person_co_n * Regulatory_factor) + (person_efficiency_n * (1 - new_z * Regulatory_factor))
    # print("person_comprehensive", person_comprehensive)
    person_comprehensive = np.argsort(person_comprehensive)
    # 由小到大排序
    # print("person_comprehensive", person_comprehensive)
    for i in range(int(num_of_group * change_rate)):
        pos_choice[i] = min_index[i]
        if random.random() < epsilon:
            new_worker = random.randint(0, (num_of_system - 1))
            while (new_worker in selected_workers):
                new_worker = random.randint(0, (num_of_system - 1))
                # print("new:",new_worker)
            num_choice[i] = new_worker
        else:
            j = -(i + 1)
            while person_comprehensive[j] in selected_workers:
                j -= 1
            # num_choice[i] = person_efficiency_sort[j]
            num_choice[i] = person_comprehensive[j]
    result = do_task(num_choice, pos_choice, selected_workers, num_of_group)
    return result


def system_work_mab_with_noise(epsilon, min_index, person_efficiency, person_efficiency_n, selected_workers, person_co,
                               times, num_of_group, new_z, new_beta, task):
    pos_choice = np.zeros(num_of_group)
    num_choice = np.zeros(num_of_group)
    # print("person_efficiency:", person_efficiency)
    person_efficiency = person_efficiency / person_efficiency_n
    person_efficiency[np.isnan(person_efficiency)] = 0
    # print("person_efficiency:", person_efficiency)
    # print("person_co:", person_co)
    # person_efficiency_sort = np.argsort(person_efficiency)
    # beta [-3: 1: 0]
    Regulatory_factor = float(1 / (1 + math.exp(- times + new_beta)))  # 调节因子，当times的原点位置不加以修正的时候，达到了更好的效果
    # 对person_efficiency和person_co进行归一化，并组合出一个“综合能力”用于贪心算法的选择
    person_co_n = functions.normalization(person_co)
    person_co_n = np.array(person_co_n)
    person_efficiency_n = functions.normalization(person_efficiency)
    person_efficiency_n = np.array(person_efficiency_n)
    # z [0.4: 0.2: 1]
    person_comprehensive = (person_co_n * Regulatory_factor) + (person_efficiency_n * (1 - new_z * Regulatory_factor))
    # print("person_comprehensive", person_comprehensive)
    person_comprehensive = np.argsort(person_comprehensive)
    # 由小到大排序
    # print("person_comprehensive", person_comprehensive)
    for i in range(int(num_of_group * change_rate)):
        pos_choice[i] = min_index[i]
        if random.random() < epsilon:
            new_worker = random.randint(0, (num_of_system - 1))
            while (new_worker in selected_workers):
                new_worker = random.randint(0, (num_of_system - 1))
                # print("new:",new_worker)
            num_choice[i] = new_worker
        else:
            j = -(i + 1)
            while person_comprehensive[j] in selected_workers:
                j -= 1
            # num_choice[i] = person_efficiency_sort[j]
            num_choice[i] = person_comprehensive[j]
    result = do_task_with_noise(num_choice, pos_choice, selected_workers, num_of_group, task)
    return result


def sort_co_ability(per_co_ability, task):
    # 重要调参，噪声浮动大小
    # print("before:",per_co_ability)
    per_co_ability = create_noise.increase_raise_co(per_co_ability, task)
    # print("now:",per_co_ability)
    num_of_group = len(per_co_ability)
    person_result = np.zeros(num_of_group)
    for i in range(num_of_group):
        for j in range(num_of_group):
            if i != j:
                person_result[i] += si_ability[i] * (per_co_ability[j])
        person_result[i] = person_result[i] / (num_of_group - 1)
    # print("person_result:",person_result)
    sorted_si_ability = sorted(enumerate(per_co_ability), key=lambda x: x[1])
    # print(sorted_si_ability)  # [(编号，数值)]
    p_co_ability_rank = []
    p_co_ability = []
    for idx, val in enumerate(sorted_si_ability):
        # print(f'编号：{val[0]}, 数值：{val[1]}')
        p_co_ability_rank.append(val[0])
        p_co_ability.append(val[1])
    return p_co_ability, p_co_ability_rank


def cal_co_ability(result_of_system, relation_pre, relation_total, relation_n, workers, num_of_group):
    # relation_n是参与次数
    # workers是选取的工人
    # relation_total是根据执行任务得出来的总结果加一起
    for k in range(num_of_group):
        relation_n[workers[k]] += 1
        relation_total[workers[k]] += result_of_system
    for k in range(num_of_system):
        if relation_n[k] > 0:
            relation_pre[k] = round(relation_total[k] / relation_n[k], 5)
    # print("relation_tt",relation_total)
    # print("relation_n",relation_n)
    # print("relation_pre",relation_pre)
    return relation_pre, relation_total, relation_n

# def find_best_si_ability(num_of_group):
#     now_co_ability = np.array(co_ability)
#     now_si_ability = np.array(si_ability)
#     all_selected_workers =now_si_ability * now_co_ability
#     # print(selected_workers)
#     # print(len(selected_workers))
#     all_selected_workers = np.argsort(all_selected_workers)
#     max_n_values = group_work(all_selected_workers,num_of_group)
#     print(max_n_values)
#     return max_n_values[0]

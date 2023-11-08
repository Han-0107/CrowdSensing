import numpy as np
import pandas as pd
import work
import time
import output as out
import functions as func
from constant import co_ability_var
from constant import co_ability
from constant import si_ability
from constant import si_ability_var
from constant import num_of_system

# 参数设置
num_of_group = 30
iterations = 200
times_of_mab = 0
times_total = 0
p_si_chose_ability = 0
new_beta = 0.6  # [0.2: 0.2: 1]   0   0.6
new_z = 0.6  # [0.2: 0.2: 1]       1   0.6
new_delta = 0.4  # [0: 0.2: 0.8]   0   0.4   epsilon
new_b = 0.4  # [0: 0.2: 0.8]       1   0.4

# test_times = [50]
# test_times = [100,150,250,400,550]
test_times = [50, 100, 150, 200, 250, 300, 350, 400, 450, 500, 550]
mode = 'e'
excel_datas = {}
excel_values = []
excel_times = []
excel_another_values = []
person_co_real = np.zeros(num_of_system)
relation_total, relation_n, relation_pre, p_co_ability, p_si_ability, selected_workers, person_efficiency, person_efficiency_n, group_efficiency, min_index \
    = func.mcs_init(num_of_group)
out.print_basic(num_of_group)

# best
each_time = 1000
times_of_epsilon = each_time
result_of_system = 0
start_time = time.time()
new_iterations = 20
for i in range(new_iterations):
    relation_total, relation_n, relation_pre, p_co_ability, p_si_ability, selected_workers, person_efficiency, person_efficiency_n, group_efficiency, min_index \
        = func.mcs_init(num_of_group)
    person_co = np.zeros(num_of_system)
    person_co_real = np.zeros(num_of_system)
    for k in range(times_of_epsilon):
        epsilon = func.epsilon_make(k) + np.sqrt(new_delta)
        person_co = relation_pre  # 更新person_co
        if k == 0:
            person_co_real = person_co
        else:
            person_co_n = func.normalization(person_co)
            person_co_n = np.array(person_co_n)
            person_co_real = person_co_real * new_b + (1 - new_b) * person_co_n
        result_temp = work.system_work_mab_with_noise(epsilon, min_index, person_efficiency, person_efficiency_n,
                                                      selected_workers, person_co_real, k, num_of_group, new_z,
                                                      new_beta, each_time)
        min_index = np.argsort(result_temp[1])  # 个人表现从小到大的编号
        group_efficiency += result_temp[0]
        relation_pre, relation_total, relation_n = work.cal_co_ability(result_temp[0], relation_pre, relation_total,
                                                                       relation_n, selected_workers, num_of_group)
        for m in range(num_of_group):  # 更新person_efficiency
            person_efficiency[selected_workers[m]] += result_temp[1][m]
            person_efficiency_n[selected_workers[m]] += 1
    group_efficiency = func.postprocess(group_efficiency, times_of_epsilon)
    # print("task:",each_time,"iterations:",i,"efficiency:",group_efficiency)
    result_of_system += group_efficiency
best_ability = result_of_system / new_iterations
print("the best ability:", best_ability)
print("the mode:", mode)

for each_time in test_times:
    times_of_epsilon = each_time
    times_of_mab = each_time
    times_total = each_time
    result_of_system = 0
    start_time = time.time()
    for i in range(iterations):
        relation_total, relation_n, relation_pre, p_co_ability, p_si_ability, selected_workers, person_efficiency, person_efficiency_n, group_efficiency, min_index \
            = func.mcs_init(num_of_group)
        # Epsilon-Greedy
        if mode == 'e':
            for k in range(times_of_epsilon):
                epsilon = func.epsilon_make(k)
                result_temp = work.system_work_e(epsilon, min_index, selected_workers, person_efficiency,
                                                 person_efficiency_n, num_of_group)
                group_efficiency += result_temp[0]
                min_index = np.argsort(result_temp[1])  # 个人表现从小到大的编号
                for m in range(num_of_group):  # 更新person_efficiency
                    person_efficiency[selected_workers[m]] += result_temp[1][m]
                    person_efficiency_n[selected_workers[m]] += 1
            relation_pre = person_efficiency
        # NEW_MAB
        if mode == 'm':
            # efficient是每个人自己结果，而relationpre是几个人一起的均值，是协作结果
            person_co = np.zeros(num_of_system)
            person_co_real = np.zeros(num_of_system)
            for k in range(times_of_epsilon):
                epsilon = func.epsilon_make(k) + np.sqrt(new_delta)

                # b [0: 0.1: 0.4]
                person_co = relation_pre  # 更新person_co
                if k == 0:
                    person_co_real = person_co
                else:
                    # 归一化可能存在问题，会把最大的全变成1
                    pass
                    person_co_n = func.normalization(person_co)
                    person_co_n = np.array(person_co_n)
                    person_co_real = person_co_real * new_b + (1 - new_b) * person_co_n
                result_temp = work.system_work_mab_with_noise(epsilon, min_index, person_efficiency,
                                                              person_efficiency_n, selected_workers, person_co_real, k,
                                                              num_of_group, new_z, new_beta, each_time)
                min_index = np.argsort(result_temp[1])  # 个人表现从小到大的编号
                group_efficiency += result_temp[0]
                relation_pre, relation_total, relation_n = work.cal_co_ability(result_temp[0], relation_pre,
                                                                               relation_total, relation_n,
                                                                               selected_workers, num_of_group)
                for m in range(num_of_group):  # 更新person_efficiency
                    person_efficiency[selected_workers[m]] += result_temp[1][m]
                    person_efficiency_n[selected_workers[m]] += 1

        # Postprocessing
        group_efficiency = func.postprocess(group_efficiency, times_of_epsilon)
        result_of_system += group_efficiency

    # 遗憾
    p_si_difference = best_ability - result_of_system / iterations
    print("The difference of time", each_time, ":", p_si_difference)
    excel_another_values.append(p_si_difference)

    end_time = time.time()
    out.print_result_of_all(result_of_system, iterations, times_total)
    out.print_time(start_time, end_time)
    result_values = round(result_of_system / iterations, 3)
    excel_values.append(result_values)
    excel_times.append(round(end_time - start_time, 3))
excel_labels = ["The number of workers in a group",
                "The number of workers in the system",
                "The variance of the co_ability",
                "The variance of the si_abilitys",
                "The average of the co_ability",
                "The average of the si_ability",
                "mode",
                "b",
                "z",
                "delta",
                "beta"
                ]
co_ability_average = sum(co_ability) / num_of_system
si_ability_average = sum(si_ability) / num_of_system
excel_parameters = [num_of_group, num_of_system, co_ability_var, si_ability_var, co_ability_average, si_ability_average,
                    mode, new_b, new_z, new_delta, new_beta]
excel_datas["task"] = test_times
excel_datas["result"] = excel_values
excel_another_values = list(excel_another_values)
excel_datas["regret"] = excel_another_values
if mode == 'm':
    excel_datas["forecast"] = list(person_co_real)
    excel_datas["real"] = list(person_efficiency / person_efficiency_n)
excel_datas["time"] = excel_times
excel_datas["label"] = excel_labels
excel_datas["parameter"] = excel_parameters
excel_max = max(len(v) for v in excel_datas.values())
excel_filled = {k: v + [None] * (excel_max - len(v)) for k, v in excel_datas.items()}
excel_all = pd.DataFrame(excel_filled)
print(excel_all)
excel_name = '.xlsx'
excel_label_name = 'si_var_' + str(round(si_ability_var, 2)) + '_co_ave_' + str(
    round(co_ability_average, 2)) + '_var' + str(round(co_ability_var, 2)) + '_group_' + str(num_of_group) + '_' + str(
    mode) + excel_name
excel_all.to_excel(excel_label_name, index=False)

from constant import co_ability_var
from constant import co_ability
from constant import si_ability
from constant import si_ability_var
from constant import num_of_system


def print_basic(num_of_group_new):
    relation_average = sum(co_ability) / num_of_system
    abilities_average = sum(si_ability) / num_of_system
    print("\033[1;30;47mBasic constants:\033[0m")
    print("   The number of workers in a group is ", num_of_group_new)
    print("   The number of workers in the system is ", num_of_system)
    print("   The variance of the relation is ", co_ability_var)
    print("   The variance of the abilities is ", si_ability_var)
    print("   The average of the relation is ", relation_average)
    print("   The average of the abilities is ", abilities_average)
    print("\033[1;30;47mThe results of system:\033[0m")


def print_result(group_efficiency):
    print("   The average result of the group is ", group_efficiency)


def print_result_of_all(sum_of_result, iterations, times_total):
    print("The final result is ", sum_of_result / iterations, " with ", times_total,
          " times training")


def print_time(start, end):
    run_time = end - start
    print("The time cost of iterations is ", run_time)
    print("-------------------------------------------------")

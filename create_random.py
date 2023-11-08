import numpy as np


# 均值生成较准确，方差生产不准确，但是可以生成全部正数的

def generate_positive_lognormal_sequence(mean, variance, size):
    # 计算对数正态分布的参数
    mu = np.log((mean ** 2) / np.sqrt(variance + mean ** 2))
    sigma = np.sqrt(np.log((variance / (mean ** 2)) + 1))

    # 生成符合指定均值和方差要求的对数正态分布随机数序列
    sequence = np.random.lognormal(mean=mu, sigma=sigma, size=size)

    return sequence


mean = 1.0  # 设置均值
variance = 2  # 设置方差
size = 100  # 设置数列的大小

sequence = generate_positive_lognormal_sequence(mean, variance, size)
print(f"Generated sequence with mean={np.mean(sequence):.2f} and variance={np.var(sequence):.2f}")
sequence = list(sequence)
print(sequence)
f = open("create_test.txt", 'w')
f.write(str(sequence))

import random
import math
import time

# 数据v离散化+扰动
def vpp(v, epsilon):
    # 将v离散化到-1,1
    p = random.random()
    boundary = (1 + v) / 2
    vp = 0
    if p < boundary:
        vp = 1
    else:
        vp = -1
    #     对离散化后的vp扰动
    p = random.random()
    boundary = math.e ** epsilon / (1 + math.e ** epsilon)
    if p > boundary:
        vp = -vp
    return vp

# 对键值对扰动
def lpp(k_v, epsilon1, epsilon2):
    #TODO 这里k_v为组数，可以改进为字典列表
    k = k_v[0]
    v = k_v[1]
    kp = 0
    vp = 0
    if k == 1:
        # 扰动value
        vp = vpp(v, epsilon2)
        # 扰动key
        #TODO 这里仅适用于key为1的情况。当k取值多个时，可以单独定义一个扰动函数kRR
        p = random.random()
        boundary = math.e ** epsilon1 / (1 + math.e ** epsilon1)
        # key 1->1
        if p < boundary:
            kp = 1
        # key 1->0
        else:
            kp = 0
            vp = 0
    else:
        v = random.random() * 2 - 1
        vp = vpp(v, epsilon2)
        p = random.random()
        boundary = math.e ** epsilon1 / (1 + math.e ** epsilon1)
        # key 0->0
        if p < boundary:
            kp = 0
            vp = 0
        # key 0->1
        else:
            kp = 1
    return kp, vp

def priv_kv(all_kv, epsilon1, epsilon2): #返回估计评率 均值
    all_kvp = [lpp(kv, epsilon1, epsilon2) for kv in all_kv]
    total = 0 #总数
    have = 0 #计数
    pos = 0
    neg = 0
    for kv in all_kvp:
        # TODO 这里仅计算了key为1时的频率，均值。
        if kv[0] == 1:
            have += 1
        total += 1
        if kv[1] == 1:
            pos += 1
        if kv[1] == -1:
            neg += 1
    f = have / total
    p = math.e ** epsilon1 / (1 + math.e ** epsilon1)
    f = (p - 1 + f) / (2 * p - 1)
    n = pos + neg
    p = math.e ** epsilon2 / (1 + math.e ** epsilon2)
    n1 = (p - 1) / (2 * p - 1) * n + pos / (2 * p - 1)
    n2 = (p - 1) / (2 * p - 1) * n + neg / (2 * p - 1)
    if n1 < 0:
        n1 = 0
    elif n1 > n:
        n1 = n
    if n2 < 0:
        n2 = 0
    elif n2 > n:
        n2 = n
    # 均值估计
    m = (n1 - n2) / n
    return f, m

if __name__ == "__main__":
    filename = "data.txt"
    seed = 10
    random.seed(seed)
    f = open(filename, "r")
    data = f.readlines()
    data = [(int(d.split()[0]), float(d.split()[1])) for d in data]
    f, m = priv_kv(data, 1, 1)
    print(f, m)
    total = 0
    have = 0
    value = 0
    for d in data:
        if d[0] == 1:
            have += 1
            value += d[1]
        total += 1
    print(have / total, value / have)
        
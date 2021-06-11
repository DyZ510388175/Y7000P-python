# -*- coding: utf-8 -*-
# @Time    : 2020/5/9
# @Author  : ForestNeo
# @Site    : forestneo.com
# @Email   : dr.forestneo@gmail.com
# @File    : k_randomized_response.py
# @Software: PyCharm


import numpy as np
import heavy_hitters.compare_methods as example
import matplotlib.pyplot as plt


class GeneralizedRandomizedResponse:
    # bucket_size k的取值，回答结果的可选值
    # epsilon 隐私预算
    def __init__(self, bucket_size, epsilon):
        self.bucket_size = bucket_size
        self.epsilon = epsilon
        self.k = bucket_size

        # self.p_h扰动成自身的概率；self.p_l扰动成其他值的概率；
        # self.__tf_matrix扰动矩阵，主对角线为self.p_h，其余为self.p_l。
        self.p_h = np.e ** epsilon / (np.e ** epsilon + self.k - 1)
        self.p_l = 1 / (np.e ** epsilon + self.k - 1)
        self.__tf_matrix = np.full(shape=(self.k, self.k), fill_value=self.p_l) #填充矩阵，大小为k*k，填充元素为self.p_l
        for i in range(self.k):
            self.__tf_matrix[i][i] = self.p_h

    def user_encode(self, bucket):
        probability_list = self.__tf_matrix[bucket] #矩阵第bucket行
        return np.random.choice(a=range(self.k), p=probability_list) #在数组a中以概率p随机取样

    def aggregate_histogram(self, private_bucket_list):
        private_hist = np.zeros(shape=self.k) #返回来一个给定形状和类型的用0填充的数组
        for private_bucket in private_bucket_list:
            private_hist[private_bucket] += 1
        estimate_hist = (private_hist - len(private_bucket_list) * self.p_l) / (self.p_h - self.p_l)
        return estimate_hist

    def aggregate_histogram_by_matrix(self, private_bucket_list):
        """
        this method is to estimate the histogram by the inverse of tf_matrix
        """
        private_hist = np.zeros(shape=self.k)
        for private_bucket in private_bucket_list:
            private_hist[private_bucket] += 1
        tf_reverse = np.linalg.inv(self.__tf_matrix) #矩阵求逆
        # np.dot向量内积、多维矩阵乘法和矩阵与向量的乘法。
        # np.reshape在不改变数据内容的情况下，改变一个数组的格式
        estimated_hist = np.dot(tf_reverse, np.reshape(private_hist, newshape=(self.bucket_size, 1)))
        return np.reshape(estimated_hist, newshape=self.bucket_size)


def run_example():
    # threshold：int触发汇总的数组元素总数而不是完整的repr(默认1000)
    # edgeitems：int在开头和结尾的摘要中的数组项数 每个维度(默认为3)
    # linewidth：int每行用于插入的字符数# 换行符(默认为75)
    np.set_printoptions(threshold=40, linewidth=200, edgeitems=5)

    n = 10 ** 5
    bucket_size = 10
    epsilon = 1

    print("==========>>>>> in KRR")
    krr = GeneralizedRandomizedResponse(bucket_size=bucket_size, epsilon=epsilon)
    bucket_list, true_hist = example.generate_bucket(n=n, bucket_size=bucket_size, distribution_name='exp')
    print("this is buckets: ", bucket_list)
    print("this is true hist: ", true_hist)

    private_bucket_list = [krr.user_encode(item) for item in bucket_list]
    estimated_hist = krr.aggregate_histogram(private_bucket_list)
    print("this is estimate_hist", estimated_hist)

    index = range(bucket_size)
    plt.plot(index, true_hist)
    plt.plot(index, estimated_hist)
    plt.legend(['true', 'krr'])
    plt.show()


if __name__ == '__main__':
    run_example()
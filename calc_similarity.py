#!/usr/bin/python3
import MeCab
from decimal import Decimal
import math

mecab = MeCab.Tagger('')
N = 255

def main():

    df_name= "./df.list"
    train_name = "./train/2012-04-04_1.txt"
    test_name = "./test/2012-04-18_3.txt"

    sgml = open(df_name)
    df_list = sgml.readlines()
    df_hash = {}
    for df in df_list:
        df_info = df.split(' ')
        df_hash[df_info[0]] = int(df_info[1])

    train_hash = {}
    test_hash = {}

    file_name = train_name
    train_hash = get_TFIDF(file_name, df_hash)

    file_name = test_name
    test_hash = get_TFIDF(file_name, df_hash)

    sum_train=0
    sum_test=0
    train_test=0

    for key in train_hash.keys():
        sum_train += train_hash[key]**2
        if key in test_hash:
            train_test += train_hash[key] * test_hash[key]

    for key in test_hash.keys():
        sum_test += test_hash[key]**2


    cos = train_test /((sum_test**0.5)*(sum_train**0.5))

    print(cos)





def get_TF(file_name):
    hash = {}
    sgml = open(file_name)
    lines = sgml.readlines()
    for line in lines:
        if  "。" not in line or "<id>" in line or "<date>" in line or "<company>" in line or "<title>" in line or "<class>" in line:
            continue
        mecab_results = mecab.parse(line)
        results = mecab_results.split('\n')
        for one in results:
            if "名詞" not in one or one=="EOF":
                continue
            one = one.split('\t')
            word = one[0]
            if len(word) < 2:
                continue

            if word in hash:
                hash[word] += 1
            else:
                hash[word] = 1

    return hash


def get_TFIDF(file_name, df_hash):
    hash2 = {}
    hash2 = get_TF(file_name)
    for key in hash2.keys():
        if key in df_hash:
            hash2[key] = hash2[key] * math.log2(N/df_hash[key])

    return hash2



if __name__ == "__main__":
        main()

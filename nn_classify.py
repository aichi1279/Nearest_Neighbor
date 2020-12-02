#!/usr/bin/python3
import MeCab
from decimal import Decimal
import math
import glob

mecab = MeCab.Tagger('')
N = 255

def main():

    df_name= "./df.list"
    train_name = "./train/*.txt"
    test_name  = "./test/*.txt"
    train_file_list = glob.glob(train_name)
    test_file_list  = glob.glob(test_name)

    sgml = open(df_name)
    df_list = sgml.readlines()
    df_hash = {}
    for df in df_list:
        df_info = df.split(' ')
        df_hash[df_info[0]] = int(df_info[1])

    test_file_list.sort()
    for test_file in test_file_list:
        test_hash = {}
        test_hash,test_class = get_TFIDF(test_file, df_hash)

        test_sum = 0
        for key in test_hash.keys():
            test_sum += test_hash[key]**2

        index = 0
        index_class = ""

        for train_file in train_file_list:
            train_hash = {}
            train_hash,train_class = get_TFIDF(train_file, df_hash)

            train_sum = 0
            train_test_dot = 0
            for key in train_hash.keys():
                train_sum += train_hash[key]**2
                if key in test_hash:
                    train_test_dot += train_hash[key] * test_hash[key]

            cos = train_test_dot/( (train_sum**0.5)*(test_sum**0.5) )
            if cos == max(cos, index):
                index = cos
                index_class = train_class

        test_file = test_file.split('/')
        test_file = test_file[-1]
        print(test_file+" "+index_class+" "+str(index))





def get_TF(file_name):
    hash = {}
    CL = ""
    sgml = open(file_name)
    lines = sgml.readlines()
    for line in lines:
        if "<class>" in line:
            line = line.split(' ')
            CL = line[2]
            continue
        elif  "。" not in line or "<id>" in line or "<date>" in line or "<company>" in line or "<title>" in line:
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

    return hash, CL


def get_TFIDF(file_name, df_hash):
    hash2 = {}
    hash2,CL = get_TF(file_name)
    for key in hash2.keys():
        if key in df_hash:
            hash2[key] = hash2[key] * math.log2(N/df_hash[key])

    return hash2, CL


if __name__ == "__main__":
        main()

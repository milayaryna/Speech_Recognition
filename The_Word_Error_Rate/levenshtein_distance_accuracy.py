# 計算辨識正確率

# !/usr/bin/env python
# coding: utf-8

import numpy as np
import os,sys

def levenshtein_distance_accuracy(hyp, ref):
    """編輯距離
    計算兩個序列的levenshtein distance，可用於計算 WER/CER
    參考資料：
        https://www.cuelogic.com/blog/the-levenshtein-algorithm
        https://martin-thoma.com/word-error-rate-calculation/

    C: correct
    W: wrong
    I: insert
    D: delete
    S: substitution

    :param hypothesis: 預測序列
    :param reference: 真實序列
    """
    with open(hyp, "r", encoding='utf-8') as f:
        hypothesis_original = f.read()
    
    with open(ref, "r", encoding='utf-8') as f:
        reference_original = f.read()
    
    hypothesis = hypothesis_original.replace(" ", "")
    reference = reference_original.replace(" ", "")
    
    len_hyp = len(hypothesis)
    len_ref = len(reference)
    cost_matrix = np.zeros((len_hyp + 1, len_ref + 1), dtype=np.int16)

    # 紀錄所有的操作，0-equal；1-insertion；2-deletion；3-substitution
    ops_matrix = np.zeros((len_hyp + 1, len_ref + 1), dtype=np.int8)

    for i in range(len_hyp + 1):
        cost_matrix[i][0] = i
    for j in range(len_ref + 1):
        cost_matrix[0][j] = j

    # 生成 cost 矩陣和 operation矩陣，i:外層hyp，j:内層ref
    for i in range(1, len_hyp + 1):
        for j in range(1, len_ref + 1):
            if hypothesis[i-1] == reference[j-1]:
                cost_matrix[i][j] = cost_matrix[i-1][j-1]
            else:
                substitution = cost_matrix[i-1][j-1] + 1
                insertion = cost_matrix[i-1][j] + 1
                deletion = cost_matrix[i][j-1] + 1

                compare_val = [substitution, insertion, deletion]   # 優先順序

                min_val = min(compare_val)
                operation_idx = compare_val.index(min_val) + 1
                cost_matrix[i][j] = min_val
                ops_matrix[i][j] = operation_idx

    match_idx = []  # 保存 hyp與ref 中所有對齊的元素下標
    i = len_hyp
    j = len_ref
    nb_map = {"N": len_ref, "C": 0, "W": 0, "I": 0, "D": 0, "S": 0}
    while i >= 0 or j >= 0:
        i_idx = max(0, i)
        j_idx = max(0, j)

        if ops_matrix[i_idx][j_idx] == 0:     # correct
            if i-1 >= 0 and j-1 >= 0:
                match_idx.append((j-1, i-1))
                nb_map['C'] += 1

            # 出邊界後，仍然使用，第一行與第一列必然全都是零
            i -= 1
            j -= 1
        # elif ops_matrix[i_idx][j_idx] == 1:   # insert
        elif ops_matrix[i_idx][j_idx] == 2:   # insert
            i -= 1
            nb_map['I'] += 1
        # elif ops_matrix[i_idx][j_idx] == 2:   # delete
        elif ops_matrix[i_idx][j_idx] == 3:   # delete
            j -= 1
            nb_map['D'] += 1
        # elif ops_matrix[i_idx][j_idx] == 3:   # substitute
        elif ops_matrix[i_idx][j_idx] == 1:   # substitute
            i -= 1
            j -= 1
            nb_map['S'] += 1

        # 出邊界處理
        if i < 0 and j >= 0:
            nb_map['D'] += 1
        elif j < 0 and i >= 0:
            nb_map['I'] += 1

    match_idx.reverse()
    wrong_cnt = cost_matrix[len_hyp][len_ref]
    nb_map["W"] = wrong_cnt


    #print("ref: %s" % reference)   #印出每個字中間沒有空格的序列
    #print("hyp: %s" % hypothesis)
    
    #print("ref: %s" % " ".join(reference)) #印出每個字中間有一個空格的序列
    #print("hyp: %s" % " ".join(hypothesis))
    
    #print(nb_map) #印出N、C、W、I、D、S數量各有多少
    
    if nb_map['N'] != 0:
      print('accuracy:', (nb_map['C']-nb_map['S']-nb_map['D']-nb_map['I'])/nb_map['C'])
    
hyp = input("Please enter your hyp_file: ")
ref = input("Please enter your ref_file: ")
    
levenshtein_distance_accuracy(hyp, ref)

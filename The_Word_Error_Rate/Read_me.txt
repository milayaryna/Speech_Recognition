計算辨識率程式 levenshtein_distance_accuracy.py 使用說明


1. 開啟 Anaconda Prompt

2. 移動至同時存放文本和程式的資料夾 (cd 資料夾路徑 )

3. 執行程式 (輸入 python levenshtein_distance_accuracy.py)。

4. 程式會問說要分析哪筆文本，依序貼上 hypothesis(辨識結果文本 )、reference(聽打後的正確文本 )的檔案名稱即可，要記得加上 .txt。

5. 按 Enter等它跑一下，就可以得到辨識率的計算結果。



辨識率計算方式是： (標準文本字數-錯字-少字-多字) / 標準文本字數

偵測錯字、少字、多字的演算法是 levenshtein distance
(兩個字串之間，由一個轉成另一個所需的最少編輯操作次數)

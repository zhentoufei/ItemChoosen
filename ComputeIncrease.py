import pandas as pd
import os
from Config import BASICINFO_PATH, INCREASE_PATH
pd.set_option('display.max_columns', None)

def computeIncreaseRaw(start, end):
    new_file_path = []
    for root, dirs, files in os.walk(BASICINFO_PATH):
        for file_name in files:
            src_path = os.path.join(root, file_name)
            new_file_path.append(src_path)


    for file_path in new_file_path:
        print(file_path)
        src_df = pd.read_csv(file_path)

        df = src_df[['itemid', 'itemlink']]

        start_col = [col for col in src_df.columns if col.find(start) >= 0][0]
        end_col = [col for col in src_df.columns if col.find(end) >= 0][0]

        df[end_col.replace('order_num', 'up')] = src_df[end_col]-src_df[start_col]



if __name__ == '__main__':
    computeIncreaseRaw('2019_04_05', '2019_04_06')

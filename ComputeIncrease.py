import pandas as pd
import os
import argparse

from Config import BASICINFO_PATH, INCREASE_PATH
pd.set_option('display.max_columns', None)

def computeIncrease(start, end):
    new_file_path = []
    for root, dirs, files in os.walk(BASICINFO_PATH):
        for file_name in files:
            src_path = os.path.join(root, file_name)
            new_file_path.append(src_path)

    for file_path in new_file_path:
        print(file_path)
        cur_save_path = os.path.join(INCREASE_PATH, file_path.split('/')[-1].replace('msearchitem', 'msearchitem_increase'))
        src_df = pd.read_csv(file_path)

        if os.path.exists(cur_save_path):
            df = pd.read_csv(cur_save_path).unique()
            del df['itemlink']
            df = pd.merge(src_df[['itemid', 'itemlink']], df, how="left", on="itemid")
        else:
            df = src_df[['itemid', 'itemlink']].unique()

        start_col_list = [col for col in src_df.columns if col.find(start) >= 0]
        end_col_list = [col for col in src_df.columns if col.find(end) >= 0]
        if len(start_col_list) <= 0 or len(end_col_list) <= 0:
            continue

        start_col = start_col_list[0]
        end_col = end_col_list[0]


        if end_col.replace('order_num', 'up') in df.columns:
            del df[end_col.replace('order_num', 'up')]


        df[end_col.replace('order_num', 'up')] = src_df[end_col]-src_df[start_col]

        df.sort_values(end_col.replace('order_num', 'up'), inplace=True, ascending=False)

        df.fillna(0, inplace=True)
        df.to_csv(cur_save_path, index=False)
        print(df.columns)


def genArgParser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-start", "--start", type=str, help="start")
    parser.add_argument("-end", "--end", type=str, help="end")
    args = parser.parse_args()
    return args

if __name__ == '__main__':
    # python ComputeIncrease.py -start 2019_04_05 -end 2019_04_06
    input_args = genArgParser()
    start = input_args.start
    end = input_args.end
    computeIncrease(start, end)

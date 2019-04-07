import os
import pandas as pd

from Config import PATH, ALL_ITEM_INFO
pd.set_option('display.max_columns', None)

def getFileNames(path):
    new_file_path = []
    for root, dirs, files in os.walk(path):
        for file_name in files:
            if file_name.startswith('.') or file_name.find("msearchitem") > 0:
                continue
            src_path = os.path.join(root, file_name)
            new_file_path.append(src_path)

    return new_file_path

def getMsearchItem(path):
    df = pd.read_excel(path)
    df['id'] = df['标题链接'].map(lambda x: str(x).split('-')[-1])
    return df['id']


def getAllItemBasicInfo(file_list, cid):
    id_link_path = dict()
    file_list.sort()
    for file_path in file_list:
        if file_path.find(cid) > 0:
            if file_path.find('msearchitem') > 0:
                continue
            df = pd.read_excel(file_path)
            df['id'] = df['标题链接'].map(lambda x: str(x).split('-')[-1])
            df = df[['id', '标题链接']]
            for ele in df.values:
                id_link_path[ele[0]] = ele[1]
    itemid = []
    itemlink = []
    for ele in id_link_path.keys():
        itemid.append(ele)
        itemlink.append(id_link_path[ele])

    itemBasicInfo = pd.DataFrame({"itemid": itemid,
                                  "itemlink": itemlink})
    itemBasicInfo.to_csv(os.path.join(ALL_ITEM_INFO, cid+'_msearchitem.csv'))
    return itemBasicInfo

if __name__ == '__main__':

    file_list = getFileNames(PATH)
    cid_list = set()
    for file_name in file_list:
        tmp_cid = file_name.split('_')[-1].split('.')[0]
        cid_list.add(tmp_cid)

    print(cid_list)
    for cid in cid_list:
        itemBasicInfo = getAllItemBasicInfo(file_list, cid)  # 更新商品基本信息
        for file_name in file_list:
            if file_name.find(cid) > 0:
                dateInfo = file_name.split('/')[-1].split('_')[0].replace('.', '_')
                tmp_df = pd.read_excel(file_name)
                tmp_df['itemid'] = tmp_df['标题链接'].map(lambda x: str(x).split('-')[-1])
                tmp_df[dateInfo+'_order_num'] = tmp_df['销量']
                tmp_df = tmp_df[['itemid', dateInfo+'_order_num']]
                itemBasicInfo = pd.merge(itemBasicInfo, tmp_df, how='left', on='itemid')
        itemBasicInfo.to_csv(os.path.join(ALL_ITEM_INFO, cid+'_msearchitem.csv'))


        #
        # print(itemBasicInfo.columns)
        # for i in range(length-1):
        #     print(i)
        #     # itemIncreaseInfo[itemInfoColumns[i+1].replace('order_num','up')] = itemBasicInfo.apply(lambda x: int(x[itemInfoColumns[i+1]]) - int(x[itemInfoColumns[i]]))
        #     itemIncreaseInfo[itemInfoColumns[i + 1].replace('order_num', 'up')] = itemBasicInfo[itemInfoColumns[i + 1]] - itemBasicInfo[itemInfoColumns[i]]
        # itemIncreaseInfo.fillna(0)
        # print(itemIncreaseInfo.head())
        #








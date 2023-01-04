# url : 0
# title : 1
# type : 2
# database : 3
# 曾用刊名 : 4
# 主办单位 : 5
# 出版周期 : 6
# ISSN : 7
# CN : 8
# 出版地 : 9
# 语种 : 10
# 开本 : 11
# 邮发代号 : 12
# 创刊时间 : 13
# 专辑名称 : 14
# 专题名称 : 15
# 出版文献量 : 16
# 总下载次数 : 17
# 总被引次数 : 18
# (2022) 复合影响因子 : 19
# (2022) 综合影响因子 : 20

import streamlit as st
import pandas as pd


@st.cache
def get_data(file):
    data = pd.read_json(file, orient="index")
    return data


cssci_info = get_data("cssci/cssci_info.json")
expanded_info = get_data("cssci-expanded/cssci-expanded_info.json")

df = pd.concat([cssci_info, expanded_info], axis=0)

df_renamed = df.rename(
    columns={"url": "期刊信息页", "title": "期刊名", "type": "发行类型", "database": "数据库收录"}
)

st.write(df_renamed)

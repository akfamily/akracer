# -*- coding:utf-8 -*-
# !/usr/bin/env python
"""
测试文件，主要用来调试 py_mini_racer 模块
"""
import pathlib
from importlib import resources

import pandas as pd
import requests

from py_mini_racer import py_mini_racer


def get_ths_js(file: str = "ths.js") -> pathlib.Path:
    """Get path to data "ths.js" text file."""
    with resources.path(package="py_mini_racer.data", resource=file) as f:
        data_file_path = f
        return data_file_path


def _get_file_content_ths(file: str = "cninfo.js") -> str:
    """
    获取 JS 文件的内容
    :param file:  JS 文件名
    :type file: str
    :return: 文件内容
    :rtype: str
    """
    setting_file_path = get_ths_js(file)
    with open(setting_file_path) as f:
        file_data = f.read()
    return file_data


def stock_industry_category_cninfo(symbol: str = "巨潮行业分类标准") -> pd.DataFrame:
    """
    巨潮资讯-行业分类数据
    http://webapi.cninfo.com.cn/#/apiDoc
    查询 p_public0002 接口
    :param symbol: 行业类型; choice of {"证监会行业分类标准", "巨潮行业分类标准", "申银万国行业分类标准", "新财富行业分类标准", "国资委行业分类标准", "巨潮产业细分标准", "天相行业分类标准", "全球行业分类标准"}
    :type symbol: str
    :return: 行业分类数据
    :rtype: pandas.DataFrame
    """
    symbol_map = {
        "证监会行业分类标准": "008001",
        "巨潮行业分类标准": "008002",
        "申银万国行业分类标准": "008003",
        "新财富行业分类标准": "008004",
        "国资委行业分类标准": "008005",
        "巨潮产业细分标准": "008006",
        "天相行业分类标准": "008007",
        "全球行业分类标准": "008008",
    }
    url = "http://webapi.cninfo.com.cn/api/stock/p_public0002"
    params = {"indcode": "", "indtype": symbol_map[symbol], "format": "json"}
    js_code = py_mini_racer.MiniRacer()
    js_content = _get_file_content_ths("cninfo.js")
    js_code.eval(js_content)
    mcode = js_code.call("getResCode1")
    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Cache-Control": "no-cache",
        "Content-Length": "0",
        "Host": "webapi.cninfo.com.cn",
        "Accept-Enckey": mcode,
        "Origin": "http://webapi.cninfo.com.cn",
        "Pragma": "no-cache",
        "Proxy-Connection": "keep-alive",
        "Referer": "http://webapi.cninfo.com.cn/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
    }
    r = requests.get(url, params=params, headers=headers)
    data_json = r.json()
    temp_df = pd.DataFrame(data_json["records"])
    cols_map = {
        "PARENTCODE": "父类编码",
        "SORTCODE": "类目编码",
        "SORTNAME": "类目名称",
        "F001V": "类目名称英文",
        "F002D": "终止日期",
        "F003V": "行业类型编码",
        "F004V": "行业类型",
    }
    temp_df.rename(columns=cols_map, inplace=True)
    # 行业按分级排序
    tmp = temp_df[["类目编码"]].copy()
    tmp["len"] = temp_df["类目编码"].str.len()
    tmp["Level"] = 0
    g = tmp.groupby("len")
    level = 0
    for k in g.groups.keys():
        temp_df.loc[temp_df["类目编码"].isin(g.get_group(k)["类目编码"]), "Level"] = level
        level += 1
    temp_df["Level"] = temp_df["Level"].astype(int)
    temp_df.rename(columns={"Level": "分级"}, inplace=True)
    temp_df["终止日期"] = pd.to_datetime(temp_df["终止日期"]).dt.date
    return temp_df


if __name__ == "__main__":
    stock_industry_category_cninfo_df = stock_industry_category_cninfo(
        symbol="巨潮行业分类标准"
    )
    print(stock_industry_category_cninfo_df)

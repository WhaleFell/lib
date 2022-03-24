# -*- coding:utf-8 -*-
# 抖音去水印 Flask API 支持 视频/图文
from email import header
from turtle import title
import httpx
from pydantic import BaseModel
from typing import Optional, List
from urllib3 import disable_warnings
disable_warnings()

header = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 8.1.0; ALP-AL00 Build/HUAWEIALP-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/63.0.3239.83 Mobile Safari/537.36 T7/10.13 baiduboxapp/10.13.0.11 (Baidu; P1 8.1.0)"
}


class Data(BaseModel):
    """返回的数据"""
    title: Optional[str]  # 标题
    author: Optional[str]  # 作者
    v_url: Optional[str]  # 无水印视频链接
    img_lst: List = []  # 无水印图片列表


class Response(BaseModel):
    """返回的响应"""
    status: int = 0  # 状态码 0-->成功 1-->失败
    type_: Optional[str]  # 链接类型  v:视频 / p:图片 / None:错误
    msg: str = "前端显示的简短信息"
    data: Data = []  # 数据对象


def get_dy_main(share_url: str) -> Response:
    """传入dy分享链接,返回 Response 对象
    :param share_url: dy 复制的分享链接
    """
    raw_url = httpx.get(share_url, headers=header, timeout=5).url
    


if __name__ == "__main__":
    print(Data().dict())

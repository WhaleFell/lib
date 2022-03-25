# -*- coding:utf-8 -*-
# 抖音去水印 Flask API 支持 视频/图文
import json
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
    m_url: Optional[str]  # 音乐
    p_url: Optional[str]  # 视频预览图
    v_url: Optional[str]  # 无水印视频链接
    img_lst: List = []  # 无水印图片列表(如果有)


class Response(BaseModel):
    """返回的响应"""
    status: int = 0  # 状态码 0-->成功 1-->失败
    type_: Optional[str]  # 链接类型  v:视频 / p:图片 / None:错误
    msg: str = "前端显示的简短信息"
    data: Data = []  # 数据对象


def pp_json(json_thing, sort=True, indents=4):
    """pretty print json data"""
    if type(json_thing) is str:
        print(json.dumps(json.loads(json_thing), sort_keys=sort,
              indent=indents, ensure_ascii=False))
    else:
        print(json.dumps(json_thing, sort_keys=sort,
              indent=indents, ensure_ascii=False))
    return None


def get_dy_main(share_url: str) -> Response:
    """传入dy分享链接,返回 Response Object
    :param share_url: dy 复制的分享链接
    :return: Response Object
    """
    raw_url = httpx.get(share_url, headers=header, timeout=5).url

    try:
        v_id = str(raw_url).split('/')[-2]
    except IndexError:
        return Response(status=1, msg="获取视频ID失败,请检查链接或重试.")

    api = f"https://www.iesdouyin.com/web/api/v2/aweme/iteminfo/?item_ids={v_id}"
    api_response = httpx.get(api, headers=header).json()
    # pp_json(api_response)
    api_useful_data = api_response["item_list"][0]
    if api_useful_data:
        title = api_useful_data["desc"]
        m_url = api_useful_data["music"]["play_url"]["uri"]
        p_url = api_useful_data["video"]["origin_cover"]["url_list"][0]
        v_url = api_useful_data["video"]["play_addr"]["url_list"][0].replace(
            'playwm', 'play')
        if api_useful_data['images']:
            type_ = "p"
            # 图文类型处理
            img_lst = [
                img['url_list'][0]
                for img in api_useful_data['images']
            ]
        data = Data(**{"title": title, "m_url": m_url,
                    "p_url": p_url, "v_url": v_url, "img_lst": img_lst})
        return Response(type_=type_, msg="视频解析成功！", data=data)
    
    return Response(status=1, msg=f"视频解析失败ID:{v_id}")
    


if __name__ == "__main__":
    get_dy_main("https://v.douyin.com/N5gu9XT/")

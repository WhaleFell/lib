# -*- coding:utf-8 -*-
# 抖音去水印 Flask API 支持 视频/图文
import json
import httpx
from pydantic import BaseModel
from typing import Optional, List
import re
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
    img_list: List = []  # 无水印图片列表(如果有)


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


def handle_pics(imgs: list) -> list:
    """ 选出可以访问的图片.
    :param imgs: 图片列表.
    [{"urls":[..,..,..,]},{},{}]
    :return: 有效的图片列表
    """
    imgs_ok = []
    for img in enumerate(imgs):
        for img_url in img[1]["url_list"]:
            img_resp = httpx.get(img_url, headers=header, timeout=5)
            if img_resp.status_code == 200:
                imgs_ok.append(img_url)
                print("================")
                print(img_url)
                with open(f"p_{img[0]}.jpg",mode="wb") as p:
                    p.write(img_resp.content)
                break
    return imgs_ok


def get_dy_main(share_url: str) -> Response:
    """传入dy分享链接,返回 Response Object
    :param share_url: dy 复制的分享链接
    :return: Response Object
    """
    data = Data()
    raw_url = httpx.get(share_url, headers=header, timeout=5).url

    # 正则匹配视频id
    pat = re.compile(r"/video/(\d+)[^d]")
    result = pat.search(str(raw_url))
    if result == None:
        return Response(status=1, msg="获取视频ID失败,请检查链接或重试.")
    else:
        v_id = result.group(1)

    api = f"https://www.iesdouyin.com/web/api/v2/aweme/iteminfo/?item_ids={v_id}"
    api_response = httpx.get(api, headers=header).json()
    api_data = api_response["item_list"]
    # pp_json(api_data)
    if api_data:
        type_ = "v"
        data.title = api_data[0]["desc"]
        data.m_url = api_data[0]["music"]["play_url"]["uri"]
        data.p_url = api_data[0]["video"]["origin_cover"]["url_list"][0]
        data.author = api_data[0]['author']['nickname']
        data.v_url = api_data[0]["video"]["play_addr"]["url_list"][0].replace(
            'playwm', 'play')
        imgs = api_data[0]['images']
        if imgs:
            type_ = "p"
            # pp_json(imgs)
            # 图文类型处理
            # fix: 涉及到部分图片可能无法访问,所以要单独一个函数排除。
            data.img_list = [
                img['url_list'][0]
                for img in api_data[0]['images']
            ]
            # data.img_list = handle_pics(imgs)

        return Response(type_=type_, msg="视频解析成功！", data=data)

    return Response(status=1, msg=f"视频解析失败ID:{v_id}")


if __name__ == "__main__":
    # print(get_dy_main("https://v.douyin.com/N5gu9XT/"))
    get_dy_main("https://v.douyin.com/N5gu9XT/")

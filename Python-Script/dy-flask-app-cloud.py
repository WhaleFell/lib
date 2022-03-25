# -*- coding:utf-8 -*-
# 抖音去水印 Flask API 云函数版本.
import json
import re
from typing import List, Optional

import requests
from flask import Flask, Response, request, make_response
from flask_cors import CORS
from pydantic import BaseModel
from urllib3 import disable_warnings

disable_warnings()
app = Flask(__name__)
CORS(app, supports_credentials=True, resources="/*")  # 跨域

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


class BaseResponse(BaseModel):
    """返回的响应"""
    status: int = 0  # 状态码 0-->成功 1-->失败
    type_: Optional[str]  # 链接类型  v:视频 / p:图片 / None:错误
    msg: str = "前端显示的简短信息"
    data: Data = []  # 数据对象

    @property
    def resp(self):
        '''BaseModel类型返回json'''
        response = make_response(
            json.dumps(
                self.dict(),
                ensure_ascii=False,
                sort_keys=False
            ),
        )
        if self.status == 1:
            response.status_code = 403
        response.mimetype = 'application/json'
        # 跨域设置
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'OPTIONS,HEAD,GET,POST'
        response.headers['Access-Control-Allow-Headers'] = 'x-requested-with'
        return response


def request_parse(req_data: request) -> dict:
    '''解析请求数据并以字典的形式返回'''
    if req_data.method == 'POST':
        data = req_data.form

    elif req_data.method == 'GET':
        data = req_data.args

    return dict(data)


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
            img_resp = requests.get(img_url, headers=header, timeout=5)
            if img_resp.status_code == 200:
                imgs_ok.append(img_url)
                print("================")
                print(img_url)
                with open(f"p_{img[0]}.jpg", mode="wb") as p:
                    p.write(img_resp.content)
                break
    return imgs_ok


def get_dy_main(share_url: str) -> BaseResponse:
    """传入dy分享链接,返回 BaseResponse Object
    :param share_url: dy 复制的分享链接
    :return: BaseResponse Object
    """
    
    data = Data()
    if share_url.startswith("https://" or "http://") is False:
        return BaseResponse(status=1, msg="链接需带http(s)://")
    raw_url = requests.get(share_url, headers=header, timeout=5).url

    # 正则匹配视频id
    pat = re.compile(r"/video/(\d+)[^d]")
    result = pat.search(str(raw_url))
    if result == None:
        return BaseResponse(status=1, msg="获取视频ID失败,请检查链接或重试.")
    else:
        v_id = result.group(1)

    api = f"https://www.iesdouyin.com/web/api/v2/aweme/iteminfo/?item_ids={v_id}"
    api_BaseResponse = requests.get(api, headers=header).json()
    api_data = api_BaseResponse["item_list"]
    # pp_json(api_data)
    if api_data:
        type_ = "v"
        data.title = api_data[0]["desc"]
        data.m_url = api_data[0]["music"]["play_url"]["uri"]
        data.p_url = api_data[0]["video"]["origin_cover"]["url_list"][0]
        data.author = api_data[0]['author']['nickname']
        v_url = api_data[0]["video"]["play_addr"]["url_list"][0].replace(
            'playwm', 'play')
        
        # 处理视频URL
        try:
            data.v_url = requests.get(v_url, headers=header, timeout=5).url
        except:
            data.v_url = v_url

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

        return BaseResponse(type_=type_, msg="视频解析成功！", data=data)

    return BaseResponse(status=1, msg=f"视频解析失败ID:{v_id}")


@app.route('/dy/', methods=['GET', 'POST'])
def dy_api():
    req = request_parse(request)
    # app.logger.warning(req)
    url = req.get('url')[0]
    if url:
        try:
            return get_dy_main(url).resp
        except Exception as why:
            return BaseResponse(status=1, msg=f"发生未知错误!{why}").resp
    return BaseResponse(status=1, msg=f"url参数为空!").resp


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9000, debug=True)

# Script-library
> 存放一些自用小脚本

## Shadowsocks 一键安装管理脚本(中国版)  
> source:[ToyoDAdoubi/doubi#ss_gosh](https://github.com/ToyoDAdoubi/doubi#ss_gosh)  

下载安装  
```shell
wget -N --no-check-certificate https://github.do/https://raw.githubusercontent.com/AdminWhaleFall/Script-library/master/shadowsock/ss-install.sh && chmod +x ss-go.sh && bash ss-go.sh
```  

## 抖音解析接口(支持视频/图文)  
> 基于 Python Flask 构建  

1. Python 3.8版本: [Python-Script/dy-flask-app.py](https://github.com/AdminWhaleFall/lib/blob/master/Python-Script/dy-flask-app.py)
2. Tencent 云函数版本:[Python-Script/dy-flask-app-cloud.py](https://github.com/AdminWhaleFall/lib/blob/master/Python-Script/dy-flask-app-cloud.py)
3. 接口文档:  
   接口demo: [https://service-dyjwokh6-1300913563.gz.apigw.tencentcs.com/dy/](https://service-dyjwokh6-1300913563.gz.apigw.tencentcs.com/dy/)  
   WEB 前端: [https://lskyl.xyz/lib/dy/](https://lskyl.xyz/lib/dy/)
   > 为作者自建,仅供测试使用.随时可能失效,请知悉.请勿频繁使用,重度使用者请自行部署API.  
   > **接口已允许跨域请求!**

   **URL:** `/dy/`  
   **methods:** GET or POST  
   **params:**  
   | Params | Description                       |
   | ------ | --------------------------------- |
   | URL    | 抖音app复制分享的URL,支持长短链接 |

   **response:**  
   | Params | Description                       |
   | ------ | --------------------------------- |
   | status | 1->异常 0->成功                   |
   | type_  | 视频类型: v->视频 p->图文         |
   | msg    | 简短的信息结果,若错误输出错误信息 |
   | data   | 解析数据                          |

   data:
   | Params   | Description        |
   | -------- | ------------------ |
   | title    | 视频文案           |
   | author   | 视频作者用户名     |
   | m_url    | 视频背景音乐地址   |
   | p_url    | 视频缩略图地址     |
   | v_url    | 无水印视频地址     |
   | img_list | 图文无水印图片列表 |

    **response example:**
    > [https://service-dyjwokh6-1300913563.gz.apigw.tencentcs.com/dy/?url=https://v.douyin.com/N5pCqQN/](https://service-dyjwokh6-1300913563.gz.apigw.tencentcs.com/dy/?url=https://v.douyin.com/N5pCqQN/)
    ```json
    {
	"status": 0,
	"type_": "v",
	"msg": "视频解析成功！",
	"data": {
		"title": "",
		"author": "",
		"m_url": "",
		"p_url": "",
		"v_url": "",
		"img_list": []
	}
    }
    ``` 

   

## PAC规则.
> proxy内网流量,direct其他.适合家中服务器搭建 Shadowsocks 远程连回家.  

[https://github.do/https://raw.githubusercontent.com/AdminWhaleFall/Script-library/master/LAN-proxy-PAC.js](https://github.do/https://raw.githubusercontent.com/AdminWhaleFall/Script-library/master/LAN-proxy-PAC.js)
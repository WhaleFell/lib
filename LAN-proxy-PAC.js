// 局域网代理脚本.局域网网段链接代理 其他直连.
// 适合通过链接回家
// PAC has no v6 support, it sucks
var ip4Re = /^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$/
var proxy = __PROXY__;
var direct = 'DIRECT;';

// 需要代理访问的内网地址
var privateNet = [
    ["10.0.0.0", "255.0.0.0"],
    ["127.0.0.0", "255.0.0.0"],
    ["172.16.0.0", "255.240.0.0"],
    ["192.168.0.0", "255.255.0.0"],
]

// 不需要代理访问的内网地址(当前所处内网)
var currentNet = [
    ["192.168.5.0", "225.225.225.0"]
]

function FindProxyForURL(url, host) {
    if (host.match(ip4Re)) {
        // 需要登录光猫时使用.
        // if (host == "192.168.1.1") return proxy;
        for (var a = 0; a < currentNet.length; a++) {
            // isInNet 判断主机IP是否在指定子网内
            // 先判断所处内网
            if (isInNet(host, currentNet[a][0], currentNet[a][1])) return direct;
        }
        for (var i = 0; i < privateNet.length; i++) {
            // isInNet 判断主机IP是否在指定子网内
            // 再判断需要代理的内网ip
            if (isInNet(host, privateNet[i][0], privateNet[i][1])) return proxy;
        }
    }
    return direct;
}


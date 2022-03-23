// 局域网代理脚本.局域网网段链接代理 其他直连.
// 适合通过链接回家
// PAC has no v6 support, it sucks
var ip4Re = /^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$/

var privateNet = [
    ["10.0.0.0", "255.0.0.0"],
    ["127.0.0.0", "255.0.0.0"],
    ["172.16.0.0", "255.240.0.0"],
    ["192.168.0.0", "255.255.0.0"],
]

function FindProxyForURL(url, host) {
    if (host.match(ip4Re)) {
        for (var i = 0; i < privateNet.length; i++) {
            // isInNet 判断主机IP是否在指定子网内
            if (isInNet(host, privateNet[i][0], privateNet[i][1])) return proxy;
        }
    }
    return direct;
}


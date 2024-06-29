#!/bin/bash

# 获取脚本所在目录
DIR=$(cd $(dirname $0); pwd)
# 获取网卡名称
enxname=$(ifconfig | grep -B 1 -E '192.168.55.100|192.168.44.100' | grep 'flags' | cut -d ':' -f1)

case "$(uname -s)" in
  Darwin)   # MacOS
    sudo route add -net 224.0.0.0 -netmask 240.0.0.0 -interface $enxname  # 添加路由
    ;;
  Linux)
    sudo ifconfig $enxname multicast  # 启用组播
    sudo route add -net 224.0.0.0 netmask 240.0.0.0 dev $enxname  # 添加路由
    ;;
  *)
    echo '其他操作系统'
    ;;
esac

# 动态防火墙 - FastAPI安全加固工具

基于CentOS 7系统的实时流量分析防火墙，通过分析Gunicorn访问日志动态屏蔽恶意IP。

## 功能特性

✅ 定时分析access.log日志（请使用系统service中的timer进行控制）  
✅ 基于自定义规则（RULES.json）的IP匹配  
✅ 自动更新防火墙规则  
✅ 永久化防火墙配置  
✅ 可视化日志记录（Execute.log）

## 依赖环境

- CentOS 7+
- Python 3.8+（当前运行环境为3.11，未测试3.6能否运行）
- firewalld服务
- Gunicorn（需启用access日志）

## 快速开始

1. 安装依赖：

```bash
sudo yum install firewalld python38
systemctl start firewalld
systemctl enable firewalld
```

2. 配置匹配规则：

```json
[
  "CONNECT malicious-domain.com",
  "POST /sensitive-api"
]
```

3.启动Gunicorn并启用access日志：

```bash
gunicorn --access-logfile logs/access.log main:app
```

4.运行防火墙：

```bash
python3 sideM.py
```

注意事项：

- 请确保防火墙服务已启动。
- 请确保防火墙服务已安装。
- 不需要额外安装依赖。# dynamicFireWall


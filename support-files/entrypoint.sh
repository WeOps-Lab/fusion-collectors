#!/bin/sh

## 定义配置模板文件和最终配置文件的路径
TEMPLATE_FILE="/fusion-collector/sidecar_template.yml"
CONFIG_FILE="/fusion-collector/sidecar.yml"

## 读取环境变量
SERVER_URL=${SERVER_URL:-http://127.0.0.1:9000/api/}
SERVER_API_TOKEN=${SERVER_API_TOKEN:-}

## 生成新的配置文件
sed "s|__SERVER_URL__|${SERVER_URL}|g" ${TEMPLATE_FILE} | \
sed "s|__SERVER_API_TOKEN__|${SERVER_API_TOKEN}|g" > ${CONFIG_FILE}

## 启动主进程
exec "$@"
## 启动前配置
相关配置项在setting.py，需配置MYSQL信息
## 启动命令
```shell
gunicorn -c server-config.py app:app
```
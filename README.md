## 启动前配置
相关配置项在setting.py，需配置MYSQL信息
## 启动命令
```shell
#前台启动
waitress-serve --host 0.0.0.0 --port 2024 app:app
#后台启动
nohup waitress-serve --host 0.0.0.0 --port 2024 app:app >log/output.log 2>&1 &

```
##停止命令
```shell
#查看进程
lsof -i tcp:2024
#杀死进程
kill -9 PID
```
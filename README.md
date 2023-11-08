# Python Flask

[Flask](https://flask.palletsprojects.com/en/3.0.x/) 是一个轻量级的 Python Web 框架



## 环境准备

- conda（推荐）
- python>=3.8



## 快速上手

安装：

```sh
pip install flask
```

编写 `app.py`：

```python
from flask import Flask

app = Flask(__name__)

@app.get("/")
def hello_world():
 	return "Hello, world!"

if __name__ == "__main__":
 	app.run()
```

启动：

```sh
flask run
flask run --host=0.0.0.0 # 局域网可见
flask run --debug # 调试模式，修改代码后自动重启
```

浏览器访问 `http://127.0.0.1:5000` 或者使用 `curl` 工具进行测试



## 实例

### Get 请求

```python
from flask import Flask, request, make_response, jsonify

app = Flask(__name__)

@app.get("/user")
def get_user():
    username = request.args.get("username")  # 获取url参数
    if username is None:
        # 状态码
        response = make_response("Argument {username} is required", 400)
    else:
        # 返回json
        response = jsonify({
            "username": username
        })
    return response

if __name__ == "__main__":
    app.run()
```

```sh
curl http://127.0.0.1:5000/user?username=Tom
```



### Post 请求

```python
from flask import Flask, request, make_response, jsonify

app = Flask(__file__)

@app.post("/user")
def create_user():
    # 获取post请求体（json）
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    if username is None or password is None:
        # 状态码
        response = make_response("Invalid username or password", 400)
    else:
        # 返回json
        response = jsonify({
            "msg": "Success"
        })
    return response

if __name__ == "main":
    app.run()
```

```sh
curl -X POST -H "Content-Type: application/json" -d '{ "username": "Tom", "password": "123456" }' http://127.0.0.1:5000/user
```



### 上传文件并保存

```python
from flask import Flask, request, make_response, jsonify
import os
import time

app = Flask(__name__)

@app.post("/upload")
def upload():
    file = request.files.get("file")

    if file is None or file.filename == "":
        return make_response("No upload file", 400)

    # 判断路径是否存在，否则创建
    file_path = "uploads/"
    if not os.path.exists(file_path):
        os.makedirs(file_path)

    # 使用时间戳作为文件名
    timestamp = str(round(time.time()))
    filename, extension = os.path.splitext(file.filename)

    # 将文件保存到本地
    file.save(file_path + timestamp + extension)

    return jsonify({
        "msg": "Success"
    })


if __name__ == "__main__":
    app.run()
```

```sh
curl -X POST -F "file=@1.jpeg" http://127.0.0.1:5000/upload
```



### 下载文件

```python
from flask import Flask, request, make_response, send_file
import os

app = Flask(__name__)


@app.get('/download')
def download():
    filename = request.args.get("filename")
    if filename is None:
        return make_response("Argument {username} is required", 400)

    file_path = "uploads/" + filename
    if not os.path.exists(file_path):
        return make_response("File not found", 404)

    return send_file(file_path)


if __name__ == "__main__":
    app.run()
```

```sh
curl -o 2.jpeg  http://127.0.0.1:5000/download?filename=1699428822.jpeg
```



### 执行 Linux 脚本

```python
from flask import Flask
import subprocess

app = Flask(__file__)


@app.get("/shell")
def shell():
    cmd = "ls"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdout


if __name__ == "__main__":
    app.run()
```

```sh
curl http://127.0.0.1:5000/shell
```


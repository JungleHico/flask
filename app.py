from flask import Flask, request, make_response, jsonify, send_file
import os
import time
import subprocess

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


@app.get('/download')
def download():
    filename = request.args.get("filename")
    if filename is None:
        return make_response("Argument {username} is required", 400)

    file_path = "uploads/" + filename
    if not os.path.exists(file_path):
        return make_response("File not found", 404)

    return send_file(file_path)


@app.get("/shell")
def shell():
    cmd = "ls"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdout


if __name__ == "__main__":
    app.run()

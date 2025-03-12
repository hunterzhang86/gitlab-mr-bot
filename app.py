# -*- coding: utf-8 -*-
# app.py
import socket

import requests
from flask import Flask, jsonify, request

# 企业微信机器人 webhook URL
WECHAT_WEBHOOK_URL = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=YOUR_WEBHOOK_KEY"
# 服务端口
SERVER_PORT = 16080

app = Flask(__name__)


def send_wechat_message(content: str):
    data = {"msgtype": "markdown", "markdown": {"content": content}}
    response = requests.post(WECHAT_WEBHOOK_URL, json=data)
    return response.status_code


# 转换 Markdown 工具
class Markdown:
    def __init__(self):
        self.content = ""

    def mark(self, text: str) -> "Markdown":
        self.content += f"**{text}**"
        return self

    def link(self, text: str, url: str) -> "Markdown":
        self.content += f"[{text}]({url})"
        return self

    def quote(self, text: str) -> "Markdown":
        self.content += f"> {text}\n"
        return self

    def info(self, text: str) -> "Markdown":
        self.content += f"{text}\n"
        return self

    def new_line(self) -> "Markdown":
        self.content += "\n"
        return self

    def build(self) -> str:
        return self.content.strip()


@app.route("/gitlab_hook", methods=["POST"])
def gitlab_hook():
    try:
        return do_gitlab_hook()
    except Exception as e:
        return jsonify({"error": str(e)}), 500


def do_gitlab_hook():
    data = request.json

    if not data:
        return jsonify({"error": "No data provided"}), 400

    if data.get("object_kind") == "merge_request":
        object_attributes = data.get("object_attributes", {})
        user = data.get("user", {})
        project = data.get("project", {})

        title = object_attributes.get("title", "无标题")
        url = object_attributes.get("url", "")
        action = object_attributes.get("action", "")
        state = object_attributes.get("state", "")
        author_name = user.get("name", "未知")
        assignee_name = data.get("assignees", [{}])[0].get("name", "未分配")
        project_name = project.get("name", "未知项目")

        markdown = Markdown()

        # Action 类型处理
        if action in ["open", "reopen"]:
            if assignee_name == "未分配":
                message = (
                    markdown.info(
                        f"您有一个新的 MR 待处理：<font color='green'>{title}</font>"
                    )
                    .new_line()
                    .new_line()
                    .info(f"**仓库名**：{project_name}")
                    .new_line()
                    .info(f"**发起人**：{author_name}")
                    .new_line()
                    .info(f"**审核人**：<@{assignee_name}>")
                    .new_line()
                    .new_line()
                    .link("点击查看 MR", url)
                    .build()
                )
                send_wechat_message(message)
            else:
                message = (
                    markdown.info(
                        f"您有一个新的 MR 待处理：<font color='green'>{title}</font>"
                    )
                    .new_line()
                    .new_line()
                    .info(f"**仓库名**：{project_name}")
                    .new_line()
                    .info(f"**发起人**：{author_name}")
                    .new_line()
                    .info(f"**审核人**：<@{assignee_name}>")
                    .new_line()
                    .new_line()
                    .link("点击查看 MR", url)
                    .build()
                )
                send_wechat_message(message)

        elif action == "merge":
            message = (
                markdown.info(f"MR 已成功合并：<font color='green'>{title}</font>")
                .new_line()
                .new_line()
                .info(f"**仓库名**：{project_name}")
                .new_line()
                .info(f"**审核人**：{author_name}")
                .new_line()
                .new_line()
                .link("点击查看 MR", url)
                .build()
            )
            send_wechat_message(message)

        elif action == "update":
            message = (
                markdown.info(f"MR 有更新：<font color='green'>{title}</font>")
                .new_line()
                .new_line()
                .info(f"**仓库名**：{project_name}")
                .new_line()
                .info(f"**发起人**：{author_name}")
                .new_line()
                .info(f"**审核人**：<@{assignee_name}>")
                .new_line()
                .new_line()
                .link("点击查看 MR", url)
                .build()
            )
            send_wechat_message(message)

    return jsonify({"status": "success"}), 200


if __name__ == "__main__":
    ip_address = socket.gethostbyname(socket.gethostname())
    app.run(host=ip_address, port=SERVER_PORT)

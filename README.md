# GitLab MR 通知机器人

这是一个简单而强大的 GitLab 合并请求(MR)通知机器人，可以将 GitLab 的 MR 更新实时发送到企业微信群组中，提高团队协作效率。

## 功能特点

- 实时监控 GitLab MR 状态变更
- 支持多种 MR 事件通知（新建、更新、重开、合并等）
- 格式化的 Markdown 消息，包含关键信息展示
- 支持企业微信 @ 功能，确保相关人员及时获取通知
- 轻量级设计，依赖简单，便于部署和维护

## 依赖要求

项目依赖非常简单，仅需要以下几个 Python 库：
```
flask==2.0.3
requests==2.26.0
flask-cors==3.0.10
```

## 快速安装

1. 克隆仓库到您的服务器
```bash
git clone https://github.com/hunterzhang86/gitlab-mr-bot.git
cd gitlab-mr-bot
```

2. 安装依赖
```bash
pip install -r requirements.txt
```

3. 配置企业微信机器人
   - 在企业微信群组中添加机器人，获取 Webhook URL
   - 在 `app.py` 文件中更新 `WECHAT_WEBHOOK_URL` 变量
   ```python
   # 企业微信机器人 webhook URL
   WECHAT_WEBHOOK_URL = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=YOUR_WEBHOOK_KEY"
   ```

4. 配置服务端口（可选）
   - 默认端口为 16080，您可以在 `app.py` 中修改 `SERVER_PORT` 变量

## 使用方法

### 启动服务

使用提供的管理脚本启动服务：

```bash
chmod +x manage_app.sh  # 确保脚本有执行权限
./manage_app.sh start   # 启动服务
```

### 停止服务

```bash
./manage_app.sh stop
```

### 重启服务

```bash
./manage_app.sh restart
```

### 配置 GitLab Webhook

1. 登录您的 GitLab 仓库管理界面
2. 进入 Settings > Webhooks
3. 添加新的 Webhook:
   - URL: `http://your-server-ip:16080/gitlab_hook` (替换为您的服务器 IP)
   - 选择触发事件: Merge request events
4. 保存 Webhook 配置

## 自定义开发与调整

得益于简单的依赖和清晰的代码结构，本项目非常适合进行自定义开发：

1. 修改消息格式：在 `do_gitlab_hook` 函数中调整 Markdown 构建逻辑
2. 添加更多事件响应：扩展 action 处理逻辑，支持更多 GitLab 事件
3. 增加其他协作平台：除了企业微信，您可以轻松扩展支持钉钉、飞书等平台

### AI 辅助调整

项目的简洁结构特别适合使用 AI 工具（如 ChatGPT、Claude）进行快速调整：

1. 复制代码到 AI 对话中，描述您需要的调整
2. AI 可以轻松理解项目结构并提供代码修改建议
3. 实施 AI 建议的更改，快速获得自定义功能

## 日志查看

服务日志默认保存在 `app.log` 文件中，您可以使用以下命令查看：

```bash
tail -f app.log
```

## 贡献与反馈

欢迎通过 Issues 或 Pull Requests 提供反馈和改进建议！

## 许可证

[MIT License](LICENSE)

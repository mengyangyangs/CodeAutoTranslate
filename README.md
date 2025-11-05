# 智能代码注释生成器
## 这是一个基于大语言模型（LLM）的Web应用，旨在为用户上传的代码文件自动生成详细、高质量的注释。项目采用前后端分离架构，前端使用 React 构建交互界面，后端使用 Python 和 Flask 框架处理业务逻辑并与 Google Gemini API 对接。

✨ 主要功能
文件上传: 支持上传各种编程语言的代码文件。
多语言支持: 可选择生成中文、英文等多种语言的注释。
AI 驱动: 集成强大的 Google Gemini LLM，智能分析代码并生成注释。
实时预览: 在网页上直接预览添加了注释的代码。
文件下载: 一键下载处理完成的、带注释的代码文件。

🔧 技术栈
前端: React.js | axios | file-saver
后端: Python 3 | Flask | requests | python-dotenv
LLM API: Google Gemini AI

📚 环境准备 (Prerequisites)
在开始之前，请确保你的本地开发环境中安装了以下软件：
Node.js 和 npm:
推荐安装 Node.js 的 LTS (长期支持) 版本。npm 会随之一起安装。
在终端中运行 node -v 和 npm -v 来检查是否安装成功。
Python:
推荐安装 Python 3.8 或更高版本。
在终端中运行 python --version 或 python3 --version 来检查。
Google AI API 密钥:
你必须拥有一个有效的 Google AI API 密钥才能使用本项目的核心功能。
可以从 Google AI for Developers 获取。

🚀 部署与运行指南
请按照以下步骤在你的本地机器上部署并运行此项目。
1. 创建项目结构
首先，创建项目的主文件夹和前后端子文件夹。
`mkdir code-comment-agent
cd code-comment-agent
mkdir frontend backend`

2. 后端 (Backend) 设置
a. 进入后端目录并创建虚拟环境
`cd backend`

# 创建一个名为 venv 的虚拟环境
`python3 -m venv venv`

b. 激活虚拟环境
# 在 macOS / Linux 上
`source venv/bin/activate`

# 在 Windows (CMD) 上
`venv\Scripts\activate`

激活后，你的终端提示符前应该会显示 (venv)。

c. 安装 Python 依赖
`pip install Flask requests python-dotenv Flask-Cors`

d. 配置环境变量 (关键步骤！)
在 backend 文件夹中创建一个名为 .env 的文件，并填入以下内容。请务必将占位符替换为你自己的信息。

# backend/.env

# 你的 Google AI API 密钥
`LLM_API_KEY="YOUR_GOOGLE_AI_API_KEY"`

# Google Gemini Pro 模型的 API Endpoint
`LLM_API_ENDPOINT="YOUR_ENDPOINT"`

3. 前端 (Frontend) 设置
a. 进入前端目录
（请打开一个新的终端窗口，或者先在后端终端中运行 deactivate 退出虚拟环境）

# 假设你当前在项目根目录
`cd frontend`

b. 安装 Node.js 依赖
`npm install axios file-saver`

4. 运行应用
你需要同时运行两个独立的终端窗口来分别启动后端和前端服务。

终端 1: 启动后端服务
`cd path/to/code-comment-agent/backend # 导航到后端目录`

`source venv/bin/activate             # 激活虚拟环境`

`flask run --port=5001                # 启动 Flask 服务`

保持此终端窗口运行。

终端 2: 启动前端应用
`cd path/to/code-comment-agent/frontend # 导航到前端目录`

`npm start                              # 启动 React 开发服务器`

这会自动在你的默认浏览器中打开 http://localhost:3000

5. 开始使用
现在，你可以在打开的浏览器页面上：
点击 “选择文件” 按钮上传你的代码。
在下拉菜单中选择期望的注释语言。
点击 “生成注释” 按钮，等待 AI 处理。
在下方的文本框中查看结果，并点击下载按钮保存文件。

💡 常见问题排查 (Troubleshooting)
- 错误: "请求中缺少文件部分"
- 原因: 前端代码未能正确获取并发送文件。
- 解决: 确保你的 frontend/src/App.js 中 handleFileChange 函数使用了 event.target.files[0] 来获取单个文件。
- 错误: "服务器未配置 LLM API 密钥或终端地址"
- 原因: backend/.env 文件缺失或内容不完整。
- 解决: 检查 .env 文件是否存在，并确保 LLM_API_KEY 和 LLM_API_ENDPOINT 都已正确填写。修改后必须重启后端服务。
- 错误: "API 请求失败: 400" (Bad Request)
- 原因: 发送给 LLM API 的请求格式不正确，最常见的原因是模型名称已过时或错误。
- 解决: 检查你的 LLM_API_ENDPOINT URL 是否正确。例如，使用 gemini-1.0-pro 而不是旧的 gemini-pro。
- 错误: "API 请求失败: 403" (Forbidden)
- 原因: 你的 API 密钥可能没有被正确启用，或者你所在的地区不支持该服务。
- 解决: 访问你的 Google AI 控制台，确保 API 已为你的项目启用，并检查服务区域限制。

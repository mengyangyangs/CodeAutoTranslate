# 🤖 智能代码注释生成器 (Code Auto-Comment Agent)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
![Python](https://img.shields.io/badge/Backend-Python_Flask-blue)
![React](https://img.shields.io/badge/Frontend-React-61DAFB)
![API](https://img.shields.io/badge/AI-Gemini_%7C_DeepSeek-orange)

这是一个基于大语言模型（LLM）的 Web 应用，旨在为用户上传的代码文件自动生成详细、高质量的注释。项目采用前后端分离架构，前端使用 React 构建交互界面，后端使用 Python Flask 处理业务逻辑，支持动态切换 **Google Gemini** 和 **DeepSeek** 模型。

---

## ✨ 主要功能

- **📂 文件上传**: 支持上传多种编程语言的源代码文件。
- **🌐 多语言支持**: 可选择生成中文、英文等多种语言的注释。
- **🧠 双模型驱动**: 集成 **Google Gemini** 和 **DeepSeek**，可按需切换。
- **👀 实时预览**: 在网页上直接预览生成注释后的代码。
- **⬇️ 一键下载**: 处理完成后，直接下载带注释的代码文件。

---

## 🏗 项目结构

```
CodeAutoTranslateAgent/
├── backend/                # Python Flask 后端
│   ├── app.py              # 主应用程序入口
│   ├── .env.example        # 环境变量示例
│   └── requirements.txt    # Python 依赖列表
├── frontend/               # React 前端
│   ├── public/             # 静态资源
│   └── src/                # React 源代码
└── README.md               # 项目文档
```

---

## 🚀 快速开始 (Quick Start)

### 1. 环境准备

确保你的本地环境已安装：
- **Node.js** (LTS 版本)
- **Python 3.8+**

### 2. 后端设置 (Backend)

```bash
cd backend

# 1. 创建并激活虚拟环境
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# venv\Scripts\activate   # Windows

# 2. 安装依赖
pip install -r requirements.txt

# 3. 配置环境变量
cp .env.example .env
# 编辑 .env 文件，填入你的 API 密钥 (详见下文配置说明)

# 4. 启动服务
flask run --port=5001
```

### 3. 前端设置 (Frontend)

打开一个新的终端窗口：

```bash
cd frontend

# 1. 安装依赖
npm install

# 2. 启动开发服务器
npm start
```

浏览器将自动打开 `http://localhost:3000`。

---

## ⚙️ 配置说明 (Configuration)

在 `backend/.env` 文件中配置你的 API 密钥和首选项。

| 变量名 | 说明 | 示例值 |
| :--- | :--- | :--- |
| `ACTIVE_LLM_PROVIDER` | **总开关**：选择使用的 AI 服务 | `gemini` 或 `deepseek` |
| `GEMINI_API_KEY` | Google Gemini API 密钥 | `AIzaSy...` |
| `GEMINI_API_ENDPOINT` | Gemini API 端点 | (见 .env.example) |
| `DEEPSEEK_API_KEY` | DeepSeek API 密钥 | `sk-...` |
| `DEEPSEEK_MODEL` | DeepSeek 模型名称 | `deepseek-chat` |

> ⚠️ **注意**: 请勿将包含真实 API 密钥的 `.env` 文件提交到版本控制系统中。

---

## 🔧 技术栈

- **Frontend**: React.js, Axios, File-Saver
- **Backend**: Python 3, Flask, Requests, Python-Dotenv
- **AI Services**: Google Gemini API, DeepSeek API

---

## ❓ 常见问题 (Troubleshooting)

- **API 请求失败 (400/403)**:
  - 检查 `.env` 中的 `ACTIVE_LLM_PROVIDER` 是否设置正确。
  - 确认 API Key 是否有效，且账户有额度。
  - 检查 API Endpoint 是否为最新（DeepSeek 或 Gemini 官方文档）。

- **服务器未配置密钥**:
  - 确保你已经将 `.env.example` 复制为 `.env` 并填入了真实的 Key。
  - 修改 `.env` 后需要**重启后端服务**才能生效。
# backend/app.py (已更新为适配 Google Gemini API)
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from dotenv import load_dotenv

# 加载 .env 文件中定义的环境变量
load_dotenv()

app = Flask(__name__)

# 配置 CORS，允许来自前端开发服务器(http://localhost:3000)的请求
CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})

@app.route('/api/comment', methods=['POST'])
def generate_comment():
    """
    API 端点，用于接收代码文件，生成注释并返回结果。
    """
    if 'file' not in request.files:
        return jsonify({"error": "请求中缺少文件部分"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "未选择任何文件"}), 400

    try:
        code_content = file.read().decode('utf-8')
        target_lang = request.form.get('targetLang', '中文')

        api_key = os.getenv('LLM_API_KEY')
        api_endpoint = os.getenv('LLM_API_ENDPOINT')

        if not api_key or not api_endpoint:
            return jsonify({"error": "服务器未配置 LLM API 密钥或终端地址"}), 500

        # --- Gemini API 修改点 1: 构造请求 URL ---
        # Google API 通常将 key 作为查询参数
        url = f"{api_endpoint}?key={api_key}"
        
        headers = {
            'Content-Type': 'application/json'
        }
        
        prompt = f"""作为一个专业的程序员，请为以下代码添加详细的{target_lang}注释。
        请遵循以下规则：
        1.  对复杂的代码块、函数或逻辑进行高层次的概述。
        2.  对关键的单行代码进行解释。
        3.  保持原有的代码结构和缩进不变。
        4.  只返回添加了注释的完整代码，不要添加任何额外的解释或引言。

        代码如下:
        ```{file.filename.split('.')[-1]}
        {code_content}
        ```
        """
        
        # --- Gemini API 修改点 2: 构造请求体 (Payload) ---
        # 这是 Google Gemini API 的请求格式
        payload = {
            "contents": [{
                "parts": [{
                    "text": prompt
                }]
            }]
        }

        # 向 Google Gemini API 发送请求
        response = requests.post(url, headers=headers, json=payload, timeout=120)
        response.raise_for_status()

        response_data = response.json()
        
        # --- Gemini API 修改点 3: 解析响应 ---
        # 这是 Google Gemini API 的响应格式
        # 增加安全检查以防止因 API 返回错误内容而崩溃
        if 'candidates' not in response_data or not response_data['candidates']:
            # 如果 Gemini 因为安全策略等原因拒绝回答，它会返回一个空的 candidates 列表
            error_info = response_data.get('promptFeedback', {}).get('blockReason', '未知原因')
            return jsonify({"error": f"API 因安全策略拒绝回答: {error_info}"}), 500

        commented_code = response_data['candidates'][0]['content']['parts'][0]['text']
        
        # 清理模型可能返回的 Markdown 代码块标记
        if commented_code.strip().startswith("```"):
            commented_code = '\n'.join(commented_code.strip().split('\n')[1:-1])

        return jsonify({"commentedCode": commented_code})

    except requests.Timeout:
        return jsonify({"error": "调用大模型 API 超时，请稍后再试"}), 504
    except requests.HTTPError as http_err:
        # 捕获 HTTP 错误并尝试显示更详细的信息
        print(f"HTTP 错误: {http_err} - 响应内容: {http_err.response.text}")
        return jsonify({"error": f"API 请求失败: {http_err.response.status_code}"}), 502
    except Exception as e:
        # 捕获其他所有未知错误
        print(f"发生未知错误: {e}")
        return jsonify({"error": "处理文件时发生内部错误"}), 500

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5001, debug=True)

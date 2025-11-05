# backend/app.py (已重构以支持多 API)
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


# --- API 调用逻辑分离: Gemini ---
def call_gemini_api(api_key, api_endpoint, prompt):
    """专门用于调用 Google Gemini API 的函数"""
    url = f"{api_endpoint}?key={api_key}"
    headers = {'Content-Type': 'application/json'}
    payload = {
        "contents": [{"parts": [{"text": prompt}]}]
    }
    
    response = requests.post(url, headers=headers, json=payload, timeout=300)
    response.raise_for_status()
    response_data = response.json()

    if 'candidates' not in response_data or not response_data['candidates']:
        error_info = response_data.get('promptFeedback', {}).get('blockReason', '未知原因')
        raise Exception(f"API 因安全策略拒绝回答: {error_info}")

    return response_data['candidates'][0]['content']['parts'][0]['text']


# --- API 调用逻辑分离: DeepSeek ---
def call_deepseek_api(api_key, api_endpoint, model, prompt):
    """专门用于调用 DeepSeek API 的函数 (类 OpenAI 格式)"""
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}]
    }

    response = requests.post(api_endpoint, headers=headers, json=payload, timeout=300)
    response.raise_for_status()
    response_data = response.json()
    
    return response_data['choices'][0]['message']['content']


@app.route('/api/comment', methods=['POST'])
def generate_comment():
    """
    API 端点，现在可以根据 .env 配置动态选择 LLM 服务。
    """
    if 'file' not in request.files:
        return jsonify({"error": "请求中缺少文件部分"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "未选择任何文件"}), 400

    try:
        code_content = file.read().decode('utf-8')
        target_lang = request.form.get('targetLang', '中文')
        
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

        # --- 动态调度核心 ---
        # 从 .env 读取总开关，并转换为小写，默认为 'gemini'
        llm_provider = os.getenv('ACTIVE_LLM_PROVIDER', 'gemini').lower()
        commented_code = ""

        if llm_provider == 'gemini':
            print("--- 使用 Gemini API ---")
            api_key = os.getenv('GEMINI_API_KEY')
            api_endpoint = os.getenv('GEMINI_API_ENDPOINT')
            if not api_key or not api_endpoint:
                raise ValueError("Gemini API 密钥或终端地址未配置")
            commented_code = call_gemini_api(api_key, api_endpoint, prompt)
        
        elif llm_provider == 'deepseek':
            print("--- 使用 DeepSeek API ---")
            api_key = os.getenv('DEEPSEEK_API_KEY')
            api_endpoint = os.getenv('DEEPSEEK_API_ENDPOINT')
            model = os.getenv('DEEPSEEK_MODEL')
            if not api_key or not api_endpoint or not model:
                raise ValueError("DeepSeek API 密钥、终端地址或模型未配置")
            commented_code = call_deepseek_api(api_key, api_endpoint, model, prompt)
        
        else:
            return jsonify({"error": f"不支持的 API 提供商: {llm_provider}"}), 500

        # 清理模型可能返回的 Markdown 代码块标记
        if commented_code.strip().startswith("```"):
            commented_code = '\n'.join(commented_code.strip().split('\n')[1:-1])

        return jsonify({"commentedCode": commented_code})

    except ValueError as ve:
        # 捕获配置错误
        return jsonify({"error": str(ve)}), 500
    except requests.Timeout:
        return jsonify({"error": "调用大模型 API 超时，请稍后再试"}), 504
    except requests.HTTPError as http_err:
        print(f"HTTP 错误: {http_err} - 响应内容: {http_err.response.text}")
        return jsonify({"error": f"API 请求失败: {http_err.response.status_code}"}), 502
    except Exception as e:
        print(f"发生未知错误: {e}")
        return jsonify({"error": f"处理文件时发生内部错误: {e}"}), 500

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5001, debug=True)

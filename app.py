import os, re, json
from flask import Flask, render_template, request, jsonify, session
from knowledge_base import find_answer, format_response
import config as cfg

app = Flask(__name__)
app.secret_key = cfg.SECRET_KEY

SYSTEM_PROMPT = "你是一个C语言编程学习助手，精通C语言的基础语法、指针、数组、结构体、文件操作、内存管理等知识。请用中文回答用户的问题，给出清晰的代码示例和解释。回答要简洁实用，适合初学者理解。"


def call_llm_api(messages):
    if not cfg.API_KEY:
        return None
    try:
        import openai
        client = openai.OpenAI(api_key=cfg.API_KEY, base_url=cfg.API_BASE_URL)
        resp = client.chat.completions.create(
            model=cfg.MODEL_NAME,
            messages=messages,
            temperature=0.7,
            max_tokens=2000
        )
        return resp.choices[0].message.content
    except Exception as e:
        return None


@app.route("/")
def index():
    return render_template("index.html", app_name=cfg.APP_NAME, app_desc=cfg.APP_DESCRIPTION)


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    question = data.get("question", "").strip()
    if not question:
        return jsonify({"answer": "请输入你的问题。"})

    if "history" not in session:
        session["history"] = []

    history = session["history"][-cfg.MAX_HISTORY:]

    if cfg.API_KEY:
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        for h in history:
            messages.append({"role": "user", "content": h.get("q", "")})
            messages.append({"role": "assistant", "content": h.get("a", "")})
        messages.append({"role": "user", "content": question})

        ai_answer = call_llm_api(messages)
        if ai_answer:
            history.append({"q": question, "a": ai_answer})
            session["history"] = history
            return jsonify({"answer": ai_answer, "mode": "ai"})

    local_answer = find_answer(question)
    if local_answer:
        formatted = format_response(local_answer, question)
        history.append({"q": question, "a": formatted})
        session["history"] = history
        return jsonify({"answer": formatted, "mode": "local"})
    else:
        fallback = ("抱歉，我还没有学习到这个知识点。建议你配置API密钥使用AI模式，或尝试换个问法。\n\n"
                    "你可以问我这些方面的问题：\n"
                    "- C语言基础语法（变量、数据类型、输入输出）\n"
                    "- 控制流（if/switch条件、for/while循环）\n"
                    "- 数组（一维、二维数组）\n"
                    "- 指针（指针运算、指针与函数、动态内存）\n"
                    "- 函数（定义、传值传址、递归）\n"
                    "- 字符串（字符数组、字符串函数）\n"
                    "- 结构体与联合体\n"
                    "- 文件操作\n"
                    "- 内存管理（malloc/free）\n"
                    "- 预处理指令\n"
                    "- 常见编译/运行错误及调试")
        history.append({"q": question, "a": fallback})
        session["history"] = history
        return jsonify({"answer": fallback, "mode": "local"})


@app.route("/reset", methods=["POST"])
def reset():
    session.pop("history", None)
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    import socket
    local_ip = socket.gethostbyname(socket.gethostname())
    print("=" * 50)
    print("  %s 已启动!" % cfg.APP_NAME)
    print("  本地访问: http://127.0.0.1:5000")
    print("  局域网访问: http://%s:5000" % local_ip)
    print("  当前模式: %s" % ("AI模式" if cfg.API_KEY else "本地知识库模式"))
    print("=" * 50)
    app.run(debug=cfg.DEBUG, host="0.0.0.0", port=5000)

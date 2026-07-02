import os, re, json, time
from flask import Flask, render_template, request, jsonify, session, Response, stream_with_context
from knowledge_base import find_answer, format_response, get_suggestions
import config as cfg

app = Flask(__name__)
app.secret_key = cfg.SECRET_KEY
app.config["SESSION_PERMANENT"] = False

SYSTEM_PROMPT = """你是C语言学习小教练，一个专业、耐心的C语言编程导师。

## 教学原则
1. **苏格拉底式引导**：先问用户理解了没有，不要直接给答案，用提问引导思考
2. **由浅入深**：先给简单解释，再深入细节，适合大学生和自学者
3. **代码示例**：每个知识点都要有可运行的C代码示例
4. **对比教学**：容易混淆的概念（如指针 vs 数组、传值 vs 传址）一定要对比说明
5. **错误导向**：主动提醒常见错误和陷阱

## 回答结构
- 先一句话概括答案
- 然后给出代码示例（用`c标注）
- 解释关键代码行
- 提醒常见错误/注意事项
- 最后可以反问用户是否理解了某个关键点

## 语言
- 使用中文回答
- 代码注释用中文
- 术语首次出现时标注英文，如：指针（pointer）

## 禁止
- 不要一次性给出大段没有示例的理论
- 不要问用户私人信息
- 不要回答与C语言无关的问题"""


def call_llm_api(messages, stream=False):
    """调用 LLM API，支持流式和非流式"""
    if not cfg.API_KEY:
        return None
    try:
        import openai
        client = openai.OpenAI(api_key=cfg.API_KEY, base_url=cfg.API_BASE_URL)
        kwargs = {
            "model": cfg.MODEL_NAME,
            "messages": messages,
            "temperature": cfg.TEMPERATURE,
            "max_tokens": cfg.MAX_TOKENS,
        }
        if stream:
            kwargs["stream"] = True
            return client.chat.completions.create(**kwargs)
        else:
            resp = client.chat.completions.create(**kwargs)
            return resp.choices[0].message.content
    except Exception as e:
        return None


def build_messages(question, history):
    """构建带上下文的 messages"""
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    for h in history[-cfg.MAX_HISTORY:]:
        messages.append({"role": "user", "content": h.get("q", "")})
        messages.append({"role": "assistant", "content": h.get("a", "")})
    messages.append({"role": "user", "content": question})
    return messages


@app.route("/")
def index():
    return render_template("index.html", app_name=cfg.APP_NAME, app_desc=cfg.APP_DESCRIPTION)


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    question = data.get("question", "").strip()
    stream = data.get("stream", False)
    if not question:
        return jsonify({"answer": "请输入你的问题。"})

    if "history" not in session:
        session["history"] = []

    history = session["history"]

    # Try AI API first
    if cfg.API_KEY:
        messages = build_messages(question, history)
        if stream:
            return stream_response(messages, question, history)
        ai_answer = call_llm_api(messages)
        if ai_answer:
            history.append({"q": question, "a": ai_answer})
            session["history"] = history
            suggestions = []
            if cfg.ENABLE_SUGGESTIONS:
                suggestions = generate_suggestions(question, ai_answer)
            return jsonify({"answer": ai_answer, "mode": "ai", "suggestions": suggestions})

    # Fallback: local knowledge base
    local_answer = find_answer(question)
    if local_answer:
        formatted = format_response(local_answer, question)
        history.append({"q": question, "a": formatted})
        session["history"] = history
        return jsonify({"answer": formatted, "mode": "local"})

    # Final fallback
    fallback = get_fallback_message()
    history.append({"q": question, "a": fallback})
    session["history"] = history
    return jsonify({"answer": fallback, "mode": "fallback"})


def stream_response(messages, question, history):
    """流式 SSE 响应"""
    def generate():
        full_answer = ""
        stream_gen = call_llm_api(messages, stream=True)
        if stream_gen is None:
            # Stream failed, try local KB
            local_answer = find_answer(question)
            if local_answer:
                formatted = format_response(local_answer, question)
                yield "data: " + json.dumps({"chunk": formatted, "mode": "local", "done": True}) + "\n\n"
            else:
                yield "data: " + json.dumps({"chunk": get_fallback_message(), "mode": "fallback", "done": True}) + "\n\n"
            return

        try:
            for chunk in stream_gen:
                if chunk.choices[0].delta.content:
                    content = chunk.choices[0].delta.content
                    full_answer += content
                    yield "data: " + json.dumps({"chunk": content, "mode": "ai", "done": False}) + "\n\n"
        except Exception:
            yield "data: " + json.dumps({"chunk": "\n\n（连接中断，请重试）", "mode": "ai", "done": True}) + "\n\n"
            return

        # Save to history
        history.append({"q": question, "a": full_answer})
        session["history"] = history

        # Generate suggestions
        suggestions = []
        if cfg.ENABLE_SUGGESTIONS:
            suggestions = generate_suggestions(question, full_answer)
        yield "data: " + json.dumps({"chunk": "", "mode": "ai", "done": True, "suggestions": suggestions}) + "\n\n"

    return Response(stream_with_context(generate()), mimetype="text/event-stream")


def generate_suggestions(question, answer):
    """根据回答生成建议追问"""
    topics = []
    # Extract code keywords from the answer
    c_keywords = ["指针", "数组", "函数", "结构体", "字符串", "文件", "内存", "递归",
                  "排序", "链表", "队列", "栈", "二叉树", "宏", "编译", "调试"]
    found = [kw for kw in c_keywords if kw in answer and kw not in question]
    for kw in found[:4]:
        topics.append(f"能不能深入讲一下{kw}的原理？")
    if "错误" in answer or "报错" in answer:
        topics.append("如何调试这种错误？有什么工具推荐？")
    if "代码" in answer or "示例" in answer:
        topics.append("有没有更复杂的实际项目例子？")
    if not topics:
        topics = ["C语言中指针和数组有什么区别？",
                  "static关键字有什么作用？",
                  "如何避免内存泄漏？"]
    return topics[:4]


def get_fallback_message():
    """兜底回复"""
    return ("抱歉，我现在还无法回答这个问题。你可以尝试：\n\n"
            "1️⃣ **配置 API 密钥** — 在 Render Dashboard 设置 API_KEY 环境变量解锁 AI 模式\n"
            "2️⃣ **换个问法** — 试试更具体的提问方式\n"
            "3️⃣ **选择话题** — 目前内置知识库涵盖以下内容：\n\n"
            "| 话题 | 示例问题 |\n"
            "|------|---------|\n"
            "| 基础语法 | printf 怎么用？ |\n"
            "| 控制流 | if-else 和 switch 哪个好？ |\n"
            "| 数组 | 二维数组怎么遍历？ |\n"
            "| 指针 | 指针和数组是什么关系？ |\n"
            "| 函数 | 传值和传址有什么区别？ |\n"
            "| 字符串 | strlen 和 sizeof 有什么区别？ |\n"
            "| 结构体 | struct 和 typedef 怎么用？ |\n"
            "| 文件操作 | 怎么读写文件？ |\n"
            "| 内存管理 | malloc 怎么用？ |\n"
            "| 预处理 | #define 和 typedef 有什么区别？ |\n"
            "| 常见错误 | 段错误是什么？ |")


@app.route("/suggestions", methods=["POST"])
def suggestions():
    """根据当前问题推荐相关问题"""
    data = request.get_json()
    question = data.get("question", "").strip()
    if not question:
        default = ["C语言中指针和数组有什么区别？",
                   "static关键字的作用是什么？",
                   "malloc和calloc有什么区别？",
                   "如何避免内存泄漏？"]
        return jsonify({"suggestions": default})
    # Simple keyword-based suggestion
    topics = ["指针", "数组", "函数", "字符串", "文件", "结构体", "内存", "递归",
              "链表", "排序", "编译", "调试", "宏"]
    found = [t for t in topics if t in question]
    if "指针" in question:
        return jsonify({"suggestions": ["数组和指针到底有什么区别？", "什么是野指针？怎么避免？", "函数指针怎么用？"]})
    if "数组" in question:
        return jsonify({"suggestions": ["数组为什么从0开始？", "动态数组怎么实现？", "数组越界会怎样？"]})
    if "内存" in question or "malloc" in question:
        return jsonify({"suggestions": ["malloc和calloc的区别？", "什么是内存泄漏？怎么检测？", "栈和堆有什么区别？"]})
    return jsonify({"suggestions": [
        f"能不能详细讲讲{found[0]}的原理？" if found else "能不能给个代码示例？",
        "有什么常见的坑要注意？",
        "有没有相关的练习题？",
        "其他编程语言中这个概念是怎么样的？"
    ][:4]})


@app.route("/reset", methods=["POST"])
def reset():
    session.pop("history", None)
    return jsonify({"status": "ok"})


@app.route("/models", methods=["GET"])
def list_models():
    """返回可用的模型配置信息"""
    return jsonify({
        "current_model": cfg.MODEL_NAME,
        "api_base": cfg.API_BASE_URL,
        "has_api_key": bool(cfg.API_KEY),
        "suggestions_enabled": cfg.ENABLE_SUGGESTIONS,
        "providers": [
            {"name": "DeepSeek", "url": "https://api.deepseek.com/v1", "models": ["deepseek-chat", "deepseek-coder"]},
            {"name": "OpenAI", "url": "https://api.openai.com/v1", "models": ["gpt-4o", "gpt-4o-mini", "gpt-3.5-turbo"]},
            {"name": "Moonshot", "url": "https://api.moonshot.cn/v1", "models": ["moonshot-v1-8k", "moonshot-v1-32k"]},
            {"name": "Qwen (阿里)", "url": "https://dashscope.aliyuncs.com/compatible-mode/v1", "models": ["qwen-plus", "qwen-turbo"]},
        ]
    })


if __name__ == "__main__":
    import socket
    local_ip = socket.gethostbyname(socket.gethostname())
    print("=" * 55)
    print("  %s 已启动!" % cfg.APP_NAME)
    print("  本地访问: http://127.0.0.1:5000")
    print("  局域网访问: http://%s:5000" % local_ip)
    print("  当前模式: %s" % ("AI模式" if cfg.API_KEY else "本地知识库模式"))
    print("  默认模型: %s" % cfg.MODEL_NAME)
    print("  API地址: %s" % cfg.API_BASE_URL)
    print("=" * 55)
    app.run(debug=cfg.DEBUG, host="0.0.0.0", port=5000)
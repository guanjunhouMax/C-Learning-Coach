# C???????

????????C?????????????????AI?????

## ??

- 智能对话答疑（配置API后支持）
- 本地知识库（11个C语言主题）
- 代码高亮展示
- 移动端适配

## 一键部署到 Render（免费）

1. **Fork 这个??** 到你的 GitHub
2. 登录 https://render.com （支持 GitHub 登录，不需要信用卡）
3. 点“New +” > 选“Web Service”
4. 连接你的 GitHub 仓库
5. Render 会自动检测到 Procfile，直接点“Deploy”
6. 等待 2-3 分钟，应用就会在 `https://xxx.onrender.com` 上运行

## 本地运行

```bash
pip install -r requirements.txt
python app.py
```

访问 http://127.0.0.1:5000

## 配置 AI 模式

在 `config.py` 中填入 API Key：

```python
API_KEY = "你的 OpenAI API Key"
```

## 项目结构

```
C_CodeCoach/
├── app.py              # Flask 应用
├── knowledge_base.py  # C语言知识库
├── config.py          # 配置
├── templates/         # 前端模板
├── static/            # 样式文件
├── generate_report.py # 报告生成脚本
├── Procfile           # 部署配置
├── requirements.txt   # 依赖
└── start.bat          # 本地启动
```

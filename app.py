import os
from openai import OpenAI
from dotenv import load_dotenv
from PyPDF2 import PdfReader
import streamlit as st

# 加载环境变量
load_dotenv()

# 初始化 DeepSeek 客户端
client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)

# 页面配置
st.set_page_config(page_title="智能简历分析助手", page_icon="📄")
st.title("📄 智能简历分析助手")
st.markdown("上传你的 PDF 简历，AI 将从 5 个维度为你生成专业评估报告")

# PDF 文本提取函数
def extract_text_from_pdf(pdf_file):
    try:
        reader = PdfReader(pdf_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        st.error(f"读取 PDF 失败: {e}")
        return None

# AI 分析函数
def analyze_resume(text):
    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": """你是一位资深技术面试官。请分析候选人的简历，给出：
1. **技术栈评估**（0-100分）：评估候选人的技术广度和深度，并给出评分理由
2. **项目深度评估**（0-100分）：是否只停留在CRUD，有没有亮点，并给出评分理由
3. **简历措辞优化**：把被动句改成主动句，增加量化指标
4. **面试预测**：根据简历，列出面试官最可能问的5个问题
5. **学习路线**：给出一份1个月的冲刺学习计划

输出格式：用Markdown标题和列表清晰展示。"""},
                {"role": "user", "content": f"这是简历文本：\n{text}"}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"AI 分析失败: {e}")
        return None

# ==================== 界面主体 ====================

uploaded_file = st.file_uploader("📎 选择你的简历 PDF 文件", type=['pdf'])

if uploaded_file is not None:
    st.success(f"✅ 已上传: {uploaded_file.name}")

    with st.spinner("🤖 AI 正在分析简历，请稍候..."):
        text = extract_text_from_pdf(uploaded_file)

        if text:
            result = analyze_resume(text)

            if result:
                st.markdown("## 📊 分析报告")
                st.markdown(result)
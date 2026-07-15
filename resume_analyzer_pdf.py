import os
from openai import OpenAI
from dotenv import load_dotenv
from PyPDF2 import PdfReader

load_dotenv()

client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)

def extract_text_from_pdf(pdf_path):
    """从PDF文件中提取文本"""
    try:
        reader = PdfReader(pdf_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        print(f"❌ 读取PDF失败: {e}")
        return None

def analyze_resume(text):
    """分析简历内容"""
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": """你是一位资深技术面试官。请分析候选人的简历，给出：
1. **技术栈评估**（0-100分）：评估候选人的技术广度和深度，并给出评分理由
2. **项目深度评估**（0-100分）：是否只停留在CRUD，有没有亮点，并给出评分理由
3. **简历措辞优化**：把被动句改成主动句，增加量化指标
4. **面试预测**：根据简历，列出面试官最可能问的5个问题
5. **学习路线**：给出一份1个月的冲刺学习计划

输出格式：用Markdown标题和列表清晰展示，每项评估都要有具体理由。"""},
            {"role": "user", "content": f"这是简历文本：\n{text}"}
        ]
    )
    return response.choices[0].message.content

def save_report(content, output_path):
    """保存分析报告"""
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)

if __name__ == "__main__":
    print("=" * 50)
    print("📄 智能简历分析助手 (PDF版)")
    print("=" * 50)
    
    # 改成你的PDF文件名（放在同一个文件夹里）
    pdf_file = "陈雅娴-南京林业大学.pdf"
    
    # 检查文件是否存在
    if not os.path.exists(pdf_file):
        print(f"\n❌ 找不到文件: {pdf_file}")
        print("请确保PDF文件在同一个文件夹里，或者修改 pdf_file 变量")
        exit(1)
    
    print(f"\n📂 正在读取: {pdf_file}")
    text = extract_text_from_pdf(pdf_file)
    
    if text is None:
        exit(1)
    
    print(f"✅ 读取成功，共 {len(text)} 个字符")
    print("\n🤖 正在分析简历，请稍候...\n")
    
    result = analyze_resume(text)
    print(result)
    
    # 保存报告
    output_file = "resume_analysis_pdf.md"
    save_report(result, output_file)
    
    print("\n" + "=" * 50)
    print(f"✅ 分析报告已保存到 {output_file}")
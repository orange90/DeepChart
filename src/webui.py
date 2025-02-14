import streamlit as st
import yaml
import os
import base64
from llm_handler import DeepSeekHandler
from streamlit_mermaid import st_mermaid
from playwright.sync_api import sync_playwright
import tempfile
import time

# 添加示例输入
EXAMPLE_INPUTS = {
    "流程图": "画一个流程图，描述用户注册流程，包含输入信息、验证邮箱、设置密码等步骤",
    "时序图": "画一个时序图，描述用户、前端、后端、数据库之间的登录交互流程",
    "甘特图": "画一个甘特图，描述一个为期2周的小型开发项目，包含需求分析、设计、开发、测试等阶段",
    "状态图": "画一个状态图，描述订单从创建到完成的所有可能状态和转换条件"
}

def load_config():
    """加载配置文件"""
    config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config', 'config.yaml')
    with open(config_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def get_mermaid_config():
    """获取 Mermaid 图表配置"""
    return """
    %%{
        init: {
            'theme': 'base',
            'themeVariables': {
                'primaryColor': '#2196f3',
                'primaryTextColor': '#fff',
                'primaryBorderColor': '#2196f3',
                'lineColor': '#2196f3',
                'secondaryColor': '#4caf50',
                'tertiaryColor': '#fff',
                'fontFamily': 'system-ui'
            },
            'flowchart': {
                'curve': 'basis',
                'padding': 20,
                'nodeSpacing': 50,
                'rankSpacing': 50,
                'htmlLabels': true,
                'useMaxWidth': true
            }
        }
    }%%
    """

def capture_mermaid_png(mermaid_code):
    """将 Mermaid 图表转换为 PNG"""
    # 创建临时HTML文件
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
        <script>
            mermaid.initialize({{ startOnLoad: true }});
        </script>
    </head>
    <body style="margin: 0; background: white;">
        <div class="mermaid">
            {mermaid_code}
        </div>
    </body>
    </html>
    """
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False) as f:
        f.write(html_content)
        temp_path = f.name
    
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page(viewport={'width': 1920, 'height': 1080})
            page.goto(f'file://{temp_path}')
            # 等待 Mermaid 图表渲染完成
            time.sleep(2)
            # 获取 Mermaid 元素
            element = page.locator('.mermaid')
            # 捕获截图
            screenshot_bytes = element.screenshot()
            browser.close()
            
        return screenshot_bytes
    finally:
        # 清理临时文件
        os.unlink(temp_path)

def get_download_button(mermaid_code):
    """生成下载按钮"""
    try:
        # 生成 PNG 图片
        png_bytes = capture_mermaid_png(mermaid_code)
        
        return st.download_button(
            label="下载图表 (PNG)",
            data=png_bytes,
            file_name="mermaid_chart.png",
            mime="image/png",
        )
    except Exception as e:
        st.error(f"图表下载准备失败：{str(e)}")
        return None

def main():
    st.set_page_config(
        page_title="DeepChart",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    # 设置页面样式
    st.markdown("""
        <style>
        .stApp {
            max-width: 100%;
            padding: 0 2rem;
        }
        footer {visibility: hidden;}
        #MainMenu {visibility: hidden;}
        header {visibility: hidden;}
        </style>
    """, unsafe_allow_html=True)
    
    st.title("DeepChart - AI 图表生成器")
    
    # 示例按钮区域
    cols = st.columns(len(EXAMPLE_INPUTS))
    for col, (name, example) in zip(cols, EXAMPLE_INPUTS.items()):
        with col:
            if st.button(f"📋 {name}示例", use_container_width=True):
                st.session_state.user_input = example
    
    # 输入区域
    st.subheader("输入需求")
    
    if 'user_input' not in st.session_state:
        st.session_state.user_input = ""
        
    user_input = st.text_area(
        "请描述您需要的图表",
        value=st.session_state.user_input,
        height=100,
        placeholder="例如：画一个流程图，描述用户登录的过程...",
        key="input_area"
    )
    
    # 控制按钮区域
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        generate_button = st.button("生成图表 🎨", type="primary", use_container_width=True)
    show_code = st.checkbox("显示 Mermaid 代码", value=False)
    
    # 结果显示区域
    if generate_button and user_input:
        try:
            with st.spinner("正在生成图表..."):
                config = load_config()
                handler = DeepSeekHandler(config)
                mermaid_code = handler.generate_mermaid(user_input)
                styled_code = get_mermaid_config() + "\n" + mermaid_code
                
                st.subheader("生成结果")
                
                # 显示图表
                st_mermaid(styled_code, height=600)
                
                # 添加下载按钮
                col1, col2, col3 = st.columns([2, 1, 2])
                with col2:
                    get_download_button(styled_code)
                
                # 显示代码
                if show_code:
                    st.subheader("Mermaid 代码")
                    st.code(mermaid_code, language="mermaid")
                    if st.button("复制代码", key="copy_button"):
                        st.write(
                            f'<script>navigator.clipboard.writeText(`{mermaid_code}`)</script>',
                            unsafe_allow_html=True
                        )
            
        except Exception as e:
            st.error(f"生成失败：{str(e)}")
    else:
        # 显示示例
        st.subheader("示例")
        example_code = get_mermaid_config() + """
graph TD
    A[开始] --> B[输入用户名密码]
    B --> C{验证}
    C -->|成功| D[登录成功]
    C -->|失败| E[显示错误]
    E --> B
    D --> F[结束]
        """
        st_mermaid(example_code, height=600)

if __name__ == "__main__":
    main() 
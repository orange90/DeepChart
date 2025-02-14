import streamlit as st
import yaml
import os
from llm_handler import DeepSeekHandler
from streamlit_mermaid import st_mermaid

def load_config():
    """加载配置文件"""
    config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config', 'config.yaml')
    with open(config_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def main():
    st.set_page_config(
        page_title="DeepChart",
        page_icon="📊",
        layout="wide"
    )
    
    st.title("DeepChart - AI 图表生成器")
    
    # 创建两列布局
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("输入需求")
        user_input = st.text_area(
            "请描述您需要的图表",
            height=200,
            placeholder="例如：画一个流程图，描述用户登录的过程..."
        )
        
        show_code = st.checkbox("显示 Mermaid 代码", value=False)
        
        if st.button("生成图表", type="primary"):
            if user_input:
                try:
                    with st.spinner("正在生成图表..."):
                        # 加载配置并初始化模型
                        config = load_config()
                        handler = DeepSeekHandler(config)
                        
                        # 生成 Mermaid 代码
                        mermaid_code = handler.generate_mermaid(user_input)
                        
                        # 在右侧显示结果
                        with col2:
                            st.subheader("生成结果")
                            # 渲染图表
                            st_mermaid(mermaid_code, height="400px")
                            
                            # 如果选择显示代码，则显示代码
                            if show_code:
                                st.subheader("Mermaid 代码")
                                st.code(mermaid_code, language="mermaid")
                                st.button(
                                    "复制代码",
                                    key="copy_button",
                                    on_click=lambda: st.write(
                                        f'<script>navigator.clipboard.writeText(`{mermaid_code}`)</script>',
                                        unsafe_allow_html=True
                                    )
                                )
                            
                except Exception as e:
                    st.error(f"生成失败：{str(e)}")
            else:
                st.warning("请输入需求描述")
    
    with col2:
        if not user_input:
            st.subheader("示例")
            example_code = """
graph TD
    A[开始] --> B[处理]
    B --> C[判断条件]
    C -->|是| D[处理1]
    C -->|否| E[处理2]
    D --> F[结束]
    E --> F
            """
            st_mermaid(example_code, height="400px")

if __name__ == "__main__":
    main() 
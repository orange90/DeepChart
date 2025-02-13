import os
import datetime
from src.llm_handler import DeepSeekHandler
from src.mermaid_generator import MermaidGenerator
import yaml

def load_config():
    with open('config/config.yaml', 'r') as f:
        result = yaml.safe_load(f)
        print(result)
        return result
    
def main():
    config = load_config()
    
    # 初始化LLM处理器
    llm_handler = DeepSeekHandler(config)
    
    # 初始化Mermaid生成器
    mermaid_generator = MermaidGenerator(config['mermaid'])
    
    print("欢迎使用DeepChart！")
    print("请输入你想生成的主题和图表类型，例如：'做一个30天假期的增肌规划的甘特图'")
    
    while True:
        user_input = input("\n请输入你的需求（输入'q'退出）: ")
        if user_input.lower() == 'q':
            break
            
        # 生成Mermaid代码
        mermaid_code = llm_handler.generate_mermaid(user_input)
        
        # 生成图片并保存
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        chart_type = "chart"  # 可以从mermaid代码中提取
        filename = f"{timestamp}_{chart_type}"
        
        mermaid_generator.generate_image(mermaid_code, filename)
        print(f"图表已生成并保存为: {filename}")

if __name__ == "__main__":
    main() 
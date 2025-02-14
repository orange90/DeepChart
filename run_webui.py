import subprocess
import sys
import os

def main():
    # 获取项目根目录
    project_root = os.path.dirname(os.path.abspath(__file__))
    webui_path = os.path.join(project_root, "src", "webui.py")
    
    print("正在启动 Mermaid 图表生成器...")
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", webui_path])
    except KeyboardInterrupt:
        print("\n已关闭 Mermaid 图表生成器")
    except Exception as e:
        print(f"启动失败：{str(e)}")

if __name__ == "__main__":
    main() 
    
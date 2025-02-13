import os
import hashlib

def calculate_sha256(file_path):
    """计算文件的SHA256值"""
    sha256_hash = hashlib.sha256()
    try:
        with open(file_path, "rb") as f:
            # 分块读取文件以处理大文件
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    except Exception as e:
        return f"错误: {str(e)}"

def main():
    # 获取项目根目录
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    model_path = os.path.join(
        project_root,
        "models",
        "DeepSeek-R1-Distill-Qwen-7B-Q4_K_M.gguf",
        "DeepSeek-R1-Distill-Qwen-7B-Q4_K_M.gguf"
    )
    
    if os.path.exists(model_path):
        print(f"正在计算模型文件的SHA256...")
        print(f"模型路径: {model_path}")
        sha256 = calculate_sha256(model_path)
        print(f"SHA256: {sha256}")
    else:
        print(f"模型文件不存在: {model_path}")

if __name__ == "__main__":
    main() 
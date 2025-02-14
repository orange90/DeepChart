import os
from huggingface_hub import hf_hub_download
from llama_cpp import Llama
import requests
import torch
import platform
import json

class DeepSeekHandler:
    def __init__(self, config):
        self.config = config
        
        if config['llm']['type'] == 'local':
            self._init_local_model()
        else:
            self._check_api_key()
            self.api_url = "https://api.siliconflow.cn/v1/chat/completions"
            self.headers = {
                "Authorization": f"Bearer {config['llm']['api_key']}",
                "Content-Type": "application/json"
            }
    
    def _init_local_model(self):
        model_path = self.config['llm']['model_path']
        model_file = os.path.join(model_path, "DeepSeek-R1-Distill-Qwen-7B-Q4_K_M.gguf")
        
        # 检查本地模型是否存在
        if not os.path.exists(model_file):
            print(f"本地模型在 {model_file} 未找到，正在从Hugging Face下载...")
            try:
                # 设置模型ID和文件名
                repo_id = "unsloth/DeepSeek-R1-Distill-Qwen-7B-GGUF"
                filename = "DeepSeek-R1-Distill-Qwen-7B-Q4_K_M.gguf"
                
                print(f"正在从 {repo_id} 下载 {filename}...")
                
                # 创建模型目录
                os.makedirs(model_path, exist_ok=True)
                
                # 下载模型
                hf_hub_download(
                    repo_id=repo_id,
                    filename=filename,
                    local_dir=model_path,
                    local_dir_use_symlinks=False
                )
                
                print("模型下载完成！")
                
            except Exception as e:
                print(f"模型下载失败: {str(e)}")
                raise
        
        # 加载量化模型
        print("正在加载模型...")
        try:
            # 检测系统类型并设置相应参数
            model_params = {
                "model_path": model_file,
                "n_ctx": 4096,  # 上下文窗口大小
                "n_threads": 8,  # CPU线程数
            }
            
            # 在 MacOS 上启用 Metal
            if platform.system() == "Darwin":
                model_params["n_gpu_layers"] = -1  # 使用所有可用的 GPU 层
                model_params["main_gpu"] = 0
                print("在 MacOS 上启用 Metal 支持")
            else:
                model_params["n_gpu_layers"] = 50  # 其他系统使用默认 GPU 层数
            
            self.model = Llama(**model_params)
            print("模型加载完成！")
        except Exception as e:
            print(f"模型加载失败，错误信息: {str(e)}")
            raise
    
    def _check_api_key(self):
        if not self.config['llm']['api_key']:
            raise ValueError("请在配置文件中设置API_KEY")
    
    def generate_mermaid(self, prompt):
        system_prompt = """你是一个专业的 Mermaid 图表生成助手。按照下面实例输出

        正确示例1（请按此格式输出）：
        
        graph TD
            A[开始] --> B[处理]
            B --> C[判断条件]
            C -->|是| D[处理1]
            C -->|否| E[处理2]
            D --> F[结束]
            E --> F

        正确示例2（请按此格式输出）：
       gantt
        title 项目计划
        section 阶段1
        任务A :a1, 2025-02-13, 3d
        任务B :after a1, 2d
        section 阶段2
        任务C :2025-02-18, 4d
        """

        if self.config['llm']['type'] == 'local':
            # 使用本地模型生成
            input_text = f"系统：{system_prompt}\n\n用户需求：{prompt}\n\n请直接输出 Mermaid 图表代码，不要包含任何其他内容："
            
            try:
                response = self.model.create_completion(
                    input_text,
                    max_tokens=2000,
                    temperature=0.7,
                    top_p=0.95,
                    repeat_penalty=1.1,
                    stop=["用户", "Human:", "Assistant:"],  # 设置停止词
                    echo=False  # 不返回输入文本
                )
                
                # 提取生成的文本
                
                res = response['choices'][0]['text'].strip()
                # 提取</think>之后的内容
                print(res)
                if "</think>" in res:
                    res = res.split("</think>")[-1].strip()

                print(res)
                return res

            except Exception as e:
                print(f"生成失败，错误信息: {str(e)}")
                raise
        else:
            try:
                # 构建API请求
                payload = {
                    "model": "Pro/deepseek-ai/DeepSeek-R1",
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": f"请直接输出 Mermaid 图表代码，不要包含任何其他内容：{prompt}"}
                    ],
                    "stream": False,
                    "max_tokens": 512,
                    "stop": ["null"],
                    "temperature": 0.7,
                    "top_p": 0.7,
                    "top_k": 50,
                    "frequency_penalty": 0.5,
                    "n": 1,
                    "response_format": {"type": "text"}
                }

              
                

                response = requests.post(
                    self.api_url,
                    json=payload,
                    headers=self.headers
                    )
                
                # 检查响应状态
                response.raise_for_status()
                
                # 解析响应
                result = response.json()
                print(result)
                if 'choices' in result and len(result['choices']) > 0:
                    content = result['choices'][0]['message']['content'].strip()
                    
                    # 提取</think>之后的内容
                    if "</think>" in content:
                        content = content.split("</think>")[-1].strip()
                    
                    # 提取</think>之后的内容
                    print('------这是DeepSeek的输出------')
                    print(content)

                    return content
                else:
                    raise Exception("API返回的响应格式不正确")
                    
            except requests.exceptions.RequestException as e:
                print(f"API请求失败: {str(e)}")
                raise
            except Exception as e:
                print(f"生成失败，错误信息: {str(e)}")
                raise 
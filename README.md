# Mermaid 图表生成器

基于 DeepSeek 模型的 Mermaid 图表代码生成工具。

## 功能特性

- 支持本地模型和 API 模式
- 自动下载和加载模型
- 生成符合 Mermaid 语法的图表代码

## 安装

1. 克隆仓库
2. 安装依赖：`pip install -r requirements.txt`
3. 复制配置文件：`cp config/config.yaml.example config/config.yaml`
4. 修改配置文件，添加您的 API key

## 使用方法

...

## 许可证

MIT License 

## 安全说明

1. 不要直接在配置文件中存储 API Key
2. 使用环境变量存储敏感信息：
   ```bash
   # Linux/Mac
   export DEEPSEEK_API_KEY=your-api-key-here
   
   # Windows
   set DEEPSEEK_API_KEY=your-api-key-here
   ```
3. 或者创建 .env 文件（确保已添加到 .gitignore） 
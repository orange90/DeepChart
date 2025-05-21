# DeepChart - Mermaid 图表生成器

基于 DeepSeek 模型的 Mermaid 图表代码生成工具。

## 功能特性

- 支持本地模型和 API 模式
- 自动下载和加载模型
- 生成符合 Mermaid 语法的图表代码
- 提供图表下载功能（PNG 格式）
- 友好的用户界面，支持示例输入

## 安装

1. 克隆仓库：
   ```bash
   git clone https://github.com/yourusername/yourrepository.git
   cd yourrepository
   ```

2. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```

3. 复制配置文件：
   ```bash
   cp config/config.yaml.example config/config.yaml
   ```

4. 修改配置文件，添加您的 API Key：
   - 在 `.env` 文件中设置 API Key：
   ```bash
   DEEPSEEK_API_KEY=your-new-api-key-here
   ```

## 使用方法

1. 运行 Web UI：
   ```bash
   python run_webui.py
   ```

2. 打开浏览器，访问 `http://localhost:8501`。

3. 在输入框中描述您需要的图表，或点击示例按钮快速填充。

4. 点击"生成图表"按钮，查看生成的图表。

5. 可选择下载图表为 PNG 格式，或查看生成的 Mermaid 代码。

## 安全说明

1. 不要直接在配置文件中存储 API Key。
2. 使用环境变量存储敏感信息：
   ```bash
   # Linux/Mac
   export DEEPSEEK_API_KEY=your-api-key-here
   
   # Windows
   set DEEPSEEK_API_KEY=your-api-key-here
   ```
3. 或者创建 `.env` 文件（确保已添加到 `.gitignore`）。

## 许可证

MIT License

## 贡献

欢迎任何形式的贡献！请提交问题或拉取请求。

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=orange90/DeepChart&type=Date)](https://www.star-history.com/#orange90/DeepChart&Date)


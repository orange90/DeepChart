import os
from playwright.sync_api import sync_playwright

class MermaidGenerator:
    def __init__(self, config):
        self.output_dir = config['output_dir']
        os.makedirs(self.output_dir, exist_ok=True)
    
    def generate_image(self, mermaid_code, filename):
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            
            # 使用mermaid-js的在线渲染
            html_content = f"""
            <html>
                <body>
                    <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
                    <div class="mermaid">
                        {mermaid_code}
                    </div>
                </body>
            </html>
            """
            
            page.set_content(html_content)
            page.wait_for_selector(".mermaid")
            
            # 保存为PNG
            element = page.locator(".mermaid")
            element.screenshot(path=os.path.join(self.output_dir, f"{filename}.png"))
            
            browser.close() 
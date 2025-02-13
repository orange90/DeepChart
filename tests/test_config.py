import os
import yaml
import unittest

class TestConfig(unittest.TestCase):
    def setUp(self):
        # 获取项目根目录路径
        self.project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.config_path = os.path.join(self.project_root, 'config', 'config.yaml')
    
    def test_read_config(self):
        """测试读取配置文件"""
        # 确保配置文件存在
        self.assertTrue(os.path.exists(self.config_path), f"配置文件不存在: {self.config_path}")
        
        # 读取配置文件
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
            
            # 打印配置内容
            print("\n当前配置文件内容:")
            print("==================")
            print(yaml.dump(config, allow_unicode=True, default_flow_style=False))
            print("==================")
            
            # 检查必要的配置项
            self.assertIn('llm', config, "配置中缺少 'llm' 部分")
            self.assertIn('type', config, "配置中缺少 'type' 字段")
            
            if config['type'] == 'local':
                self.assertIn('model_path', config['llm'], "本地模式下缺少 'model_path' 配置")
            else:
                self.assertIn('api_key', config, "API模式下缺少 'api_key' 配置")
                
        except yaml.YAMLError as e:
            self.fail(f"解析配置文件失败: {str(e)}")
        except Exception as e:
            self.fail(f"读取配置文件时发生错误: {str(e)}")

if __name__ == '__main__':
    unittest.main() 
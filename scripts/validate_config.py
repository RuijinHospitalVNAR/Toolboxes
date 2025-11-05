#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Configuration Validation Script

This script validates the unified configuration file and checks tool availability.
"""

import os
import sys
import subprocess
import logging
from pathlib import Path

# Add src directory to Python path
src_dir = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_dir))

from vlpim.tools.config_loader import config_loader

def setup_logging():
    """Setup logging"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )

def check_tool_availability(tool_name: str) -> dict:
    """检查工具可用性"""
    logger = logging.getLogger(__name__)
    
    result = {
        'tool_name': tool_name,
        'available': False,
        'path': '',
        'executable': '',
        'error': ''
    }
    
    try:
        # 获取工具路径和可执行文件
        path = config_loader.get_tool_path(tool_name)
        executable = config_loader.get_tool_executable(tool_name)
        
        result['path'] = path
        result['executable'] = executable
        
        if not path:
            result['error'] = f"未配置 {tool_name} 路径"
            logger.warning(f"[ERROR] {tool_name}: {result['error']}")
            return result
        
        # 检查路径是否存在
        if not os.path.exists(path):
            result['error'] = f"路径不存在: {path}"
            logger.warning(f"[ERROR] {tool_name}: {result['error']}")
            return result
        
        # 检查可执行文件是否存在
        if tool_name == 'rosetta':
            # Rosetta 有特殊的路径结构
            if os.path.exists(executable):
                result['available'] = True
                logger.info(f"[OK] {tool_name}: 可用 ({executable})")
            else:
                result['error'] = f"可执行文件不存在: {executable}"
                logger.warning(f"[ERROR] {tool_name}: {result['error']}")
        else:
            # 其他工具
            if os.path.exists(executable):
                result['available'] = True
                logger.info(f"[OK] {tool_name}: 可用 ({executable})")
            else:
                # 尝试在 PATH 中查找
                try:
                    subprocess.run(['which', executable.split('/')[-1]], 
                                 capture_output=True, check=True)
                    result['available'] = True
                    logger.info(f"[OK] {tool_name}: 在 PATH 中找到 ({executable.split('/')[-1]})")
                except subprocess.CalledProcessError:
                    result['error'] = f"可执行文件不存在且不在 PATH 中: {executable}"
                    logger.warning(f"[ERROR] {tool_name}: {result['error']}")
        
    except Exception as e:
        result['error'] = f"检查工具时出错: {e}"
        logger.error(f"[ERROR] {tool_name}: {result['error']}")
    
    return result

def check_model_weights(tool_name: str) -> dict:
    """检查模型权重"""
    logger = logging.getLogger(__name__)
    
    result = {
        'tool_name': tool_name,
        'available': False,
        'path': '',
        'error': ''
    }
    
    try:
        model_weights_path = config_loader.get_model_weights_path(tool_name)
        result['path'] = model_weights_path
        
        if not model_weights_path:
            result['error'] = f"未配置 {tool_name} 模型权重路径"
            logger.warning(f"[ERROR] {tool_name} 模型权重: {result['error']}")
            return result
        
        if not os.path.exists(model_weights_path):
            result['error'] = f"模型权重路径不存在: {model_weights_path}"
            logger.warning(f"[ERROR] {tool_name} 模型权重: {result['error']}")
            return result
        
        # 检查模型权重文件
        model_files = list(Path(model_weights_path).glob("*.pkl"))
        if not model_files:
            model_files = list(Path(model_weights_path).glob("*.pt"))
        if not model_files:
            model_files = list(Path(model_weights_path).glob("*.pth"))
        
        if model_files:
            result['available'] = True
            logger.info(f"[OK] {tool_name} 模型权重: 可用 ({model_weights_path})")
        else:
            result['error'] = f"模型权重目录中未找到模型文件: {model_weights_path}"
            logger.warning(f"[ERROR] {tool_name} 模型权重: {result['error']}")
        
    except Exception as e:
        result['error'] = f"检查模型权重时出错: {e}"
        logger.error(f"[ERROR] {tool_name} 模型权重: {result['error']}")
    
    return result

def check_user_input_options() -> dict:
    """检查用户输入选项配置"""
    logger = logging.getLogger(__name__)
    
    result = {
        'user_epitopes': {
            'available': False,
            'path': '',
            'error': ''
        }
    }
    
    try:
        # 检查是否有用户提供的抗原位点文件
        user_epitopes_path = config_loader.get_user_input_path('epitopes')
        result['user_epitopes']['path'] = user_epitopes_path
        
        if user_epitopes_path and os.path.exists(user_epitopes_path):
            result['user_epitopes']['available'] = True
            logger.info("[OK] 用户抗原位点文件: 已提供")
        else:
            result['user_epitopes']['error'] = "未提供用户抗原位点文件，将使用NetMHCIIpan预测"
            logger.info("[INFO] 用户抗原位点: 未提供，将使用NetMHCIIpan预测")
    
    except Exception as e:
        result['user_epitopes']['error'] = f"检查用户输入配置时出错: {e}"
        logger.warning(f"[WARNING] 用户抗原位点: {result['user_epitopes']['error']}")
    
    return result

def validate_pipeline_parameters() -> dict:
    """验证管道参数"""
    logger = logging.getLogger(__name__)
    
    result = {
        'parameters': {},
        'valid': True,
        'errors': []
    }
    
    try:
        # 检查基本参数
        output_dir = config_loader.get_pipeline_param('basic', 'default_output_dir')
        log_level = config_loader.get_pipeline_param('basic', 'default_log_level')
        max_candidates = config_loader.get_pipeline_param('ranking', 'max_candidates')
        rmsd_threshold = config_loader.get_pipeline_param('alphafold3', 'default_rmsd_threshold')
        
        result['parameters'] = {
            'output_dir': output_dir,
            'log_level': log_level,
            'max_candidates': max_candidates,
            'rmsd_threshold': rmsd_threshold
        }
        
        # 验证参数合理性
        if max_candidates <= 0:
            result['errors'].append("max_candidates 必须大于 0")
            result['valid'] = False
        
        if rmsd_threshold <= 0:
            result['errors'].append("rmsd_threshold 必须大于 0")
            result['valid'] = False
        
        if log_level not in ['DEBUG', 'INFO', 'WARNING', 'ERROR']:
            result['errors'].append("log_level 必须是 DEBUG、INFO、WARNING 或 ERROR 之一")
            result['valid'] = False
        
        if result['valid']:
            logger.info("[OK] 管道参数: 验证通过")
        else:
            for error in result['errors']:
                logger.error(f"[ERROR] 管道参数: {error}")
    
    except Exception as e:
        result['errors'].append(f"验证管道参数时出错: {e}")
        result['valid'] = False
        logger.error(f"[ERROR] 管道参数: {e}")
    
    return result

def main():
    """主函数"""
    setup_logging()
    logger = logging.getLogger(__name__)
    
    print("=" * 60)
    print("免疫原性优化管道 - 配置验证")
    print("=" * 60)
    
    # 显示配置摘要
    config_loader.print_config_summary()
    print()
    
    # 检查工具可用性
    print("=== 工具可用性检查 ===")
    tools = ['alphafold3', 'proteinmpnn', 'netmhcii', 'rosetta']
    tool_results = {}
    
    for tool in tools:
        tool_results[tool] = check_tool_availability(tool)
    
    print()
    
    # 检查模型权重
    print("=== 模型权重检查 ===")
    model_tools = ['alphafold3', 'proteinmpnn']
    model_results = {}
    
    for tool in model_tools:
        model_results[tool] = check_model_weights(tool)
    
    print()
    
    # 检查用户输入选项
    print("=== 用户输入选项检查 ===")
    user_input_results = check_user_input_options()
    
    print()
    
    # 验证管道参数
    print("=== 管道参数验证 ===")
    param_results = validate_pipeline_parameters()
    
    print()
    
    # 总结
    print("=" * 60)
    print("配置验证总结")
    print("=" * 60)
    
    # 统计可用工具
    available_tools = sum(1 for result in tool_results.values() if result['available'])
    total_tools = len(tools)
    
    available_models = sum(1 for result in model_results.values() if result['available'])
    total_models = len(model_tools)
    
    print(f"工具可用性: {available_tools}/{total_tools}")
    print(f"模型权重: {available_models}/{total_models}")
    print(f"用户抗原位点: {'[OK]' if user_input_results['user_epitopes']['available'] else '[INFO]'}")
    print(f"管道参数: {'[OK]' if param_results['valid'] else '[ERROR]'}")
    
    # 给出建议
    print("\n建议:")
    if available_tools < total_tools:
        print("- 请配置缺失的工具路径")
    if available_models < total_models:
        print("- 请配置缺失的模型权重路径")
    if not user_input_results['user_epitopes']['available']:
        print("- 可以上传抗原位点文件，或使用NetMHCIIpan自动预测")
    if not param_results['valid']:
        print("- 请修正管道参数错误")
    
    if available_tools == total_tools and available_models == total_models and param_results['valid']:
        print("- 配置验证通过！可以运行管道了。")
    
    print("=" * 60)

if __name__ == "__main__":
    main()

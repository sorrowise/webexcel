# -*- coding: utf-8 -*-
"""
Excel 文件处理业务逻辑
这个文件包含可定制的处理逻辑，您可以根据需要修改 process_excel 函数
"""

import pandas as pd
import os
from logic import *


def process_excel(file_path, original_name=None):
    """
    处理 Excel 文件的主函数
    
    参数:
        file_path: 输入 Excel 文件的路径（文件系统中的安全文件名）
        original_name: 原始文件名（可选，用于生成输出文件名，支持中文）
        
    返回:
        输出文件的路径
    """
    # 读取 Excel 文件
    df = pd.read_excel(file_path)
    

    
    # ============================================
    # 以下为可定制的业务逻辑区域
    # 您可以根据需要修改这部分代码
    # ============================================
    
    df = get_hedge_fund_details(df)
    
    # ============================================
    # 业务逻辑区域结束
    # ============================================
    
    # 生成输出文件名
    # 如果提供了原始文件名，使用原始文件名（支持中文）
    if original_name:
        base_name = os.path.splitext(original_name)[0]
    else:
        base_name = os.path.splitext(os.path.basename(file_path))[0]
    
    # 清理文件名，移除可能导致问题的特殊字符，但保留中文
    safe_chars = []
    for c in base_name:
        # 保留中文字符、字母、数字、下划线、连字符、点、空格
        if (c.isalnum() or 
            c in ('_', '-', '.', ' ') or 
            ('\u4e00' <= c <= '\u9fff') or  # 中文
            ('\u3040' <= c <= '\u309f') or  # 日文平假名
            ('\u30a0' <= c <= '\u30ff')):   # 日文片假名
            safe_chars.append(c)
        else:
            safe_chars.append('_')
    safe_base_name = ''.join(safe_chars).strip()
    
    output_path = f"{safe_base_name}_processed.xlsx"
    
    # 保存处理后的文件
    # 在 Pyodide 环境中，确保使用正确的引擎和参数
    try:
        # 先尝试直接保存
        df.to_excel(output_path, index=False, engine='openpyxl')
        print(f"文件已保存到: {output_path}")
        
        # 验证文件是否成功创建
        if not os.path.exists(output_path):
            raise Exception(f"文件保存失败: {output_path} 不存在")
            
        # 验证文件大小（应该大于0）
        file_size = os.path.getsize(output_path)
        if file_size == 0:
            raise Exception(f"文件保存失败: {output_path} 大小为0")
            
        print(f"文件大小: {file_size} 字节")
        
    except Exception as e:
        error_msg = f"保存文件时出错: {str(e)}"
        print(f"错误详情: {error_msg}")
        raise Exception(error_msg)
    
    return output_path


# 如果您需要处理多个工作表，可以使用以下函数
def process_excel_multisheet(file_path):
    """
    处理包含多个工作表的 Excel 文件
    
    参数:
        file_path: 输入 Excel 文件的路径
        
    返回:
        输出文件的路径
    """
    excel_file = pd.ExcelFile(file_path)
    output_path = f"{os.path.splitext(os.path.basename(file_path))[0]}_processed.xlsx"
    
    with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
        for sheet_name in excel_file.sheet_names:
            df = pd.read_excel(file_path, sheet_name=sheet_name)
            
            # ============================================
            # 在这里添加您的业务逻辑
            # ============================================
            
            # 将处理后的数据写入新文件
            df.to_excel(writer, sheet_name=sheet_name, index=False)
    
    return output_path

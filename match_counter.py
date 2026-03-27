#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据匹配统计程序
用于统计b.txt中每个字符串在a.txt中的出现次数
"""

import os


def main():
    """
    主函数
    """
    # 文件路径
    base_dir = os.path.join(os.path.dirname(__file__), 'x')
    a_file = os.path.join(base_dir, 'a.txt')
    b_file = os.path.join(base_dir, 'b.txt')
    c_file = os.path.join(base_dir, 'c.txt')
    
    print("开始处理数据匹配统计...")
    
    try:
        # 读取a.txt的所有内容，过滤掉以Folder开头的行
        with open(a_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            # 过滤掉以Folder开头的行
            filtered_lines = [line for line in lines if not line.strip().startswith('Folder')]
            # 将过滤后的行重新组合成字符串
            a_content = ''.join(filtered_lines)
        
        # 读取b.txt的所有字符串
        with open(b_file, 'r', encoding='utf-8') as f:
            b_strings = [line.strip() for line in f if line.strip()]
        
        print(f"读取完成: a.txt 共 {len(lines)} 行, 过滤后剩余 {len(filtered_lines)} 行, b.txt 共 {len(b_strings)} 个字符串")
        
        # 统计每个字符串的出现次数
        results = {}
        for string in b_strings:
            if string:
                count = 0
                # 遍历a.txt的每一行，进行精确匹配
                for line in filtered_lines:
                    # 提取每行的路径部分（去掉Item Type部分）
                    path_part = line.strip().split('\t', 1)[1] if '\t' in line else line.strip()
                    # 条件1: b.txt中的字符串位于a.txt行文本的末尾
                    if path_part.endswith(string):
                        count += 1
                    # 条件2: a.txt的行文本中包含b.txt字符串+"的完整匹配
                    elif f"{string}/" in path_part:
                        count += 1
                results[string] = count
        
        # 写入结果到c.txt
        with open(c_file, 'w', encoding='utf-8') as f:
            for string, count in results.items():
                f.write(f"{string}\t{count}\n")
        
        print(f"处理完成: 已将统计结果写入 {c_file}")
        print(f"共统计 {len(results)} 个字符串")
        
    except Exception as e:
        print(f"处理过程中出现错误: {e}")


if __name__ == "__main__":
    main()

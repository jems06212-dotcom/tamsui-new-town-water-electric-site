#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Office 文件讀取工具 - 測試與示範"""

import sys
import os
from pathlib import Path

def read_excel(filepath, sheet_name=None):
    """讀取 Excel 檔案並回傳內容"""
    try:
        import pandas as pd
        
        # 嘗試讀取
        if sheet_name:
            df = pd.read_excel(filepath, sheet_name=sheet_name)
        else:
            # 讀取第一個工作表
            xl = pd.ExcelFile(filepath)
            sheet_names = xl.sheet_names
            print(f"📊 工作表列表: {sheet_names}")
            df = pd.read_excel(filepath, sheet_name=0)
        
        print(f"\n✅ 成功讀取: {filepath}")
        print(f"📏 資料筆數: {len(df)} 列 x {len(df.columns)} 欄")
        print(f"\n欄位名稱:\n{list(df.columns)}")
        print(f"\n前 5 筆資料:")
        print(df.head(5).to_string())
        
        return df
        
    except Exception as e:
        print(f"❌ 讀取失敗: {e}")
        return None

def read_word(filepath):
    """讀取 Word 檔案並回傳文字內容"""
    try:
        from docx import Document
        
        doc = Document(filepath)
        text = []
        for para in doc.paragraphs:
            text.append(para.text)
        
        full_text = '\n'.join(text)
        print(f"\n✅ 成功讀取 Word: {filepath}")
        print(f"📄 段落數: {len(doc.paragraphs)}")
        print(f"\n前 500 字:\n{full_text[:500]}")
        
        return full_text
        
    except Exception as e:
        print(f"❌ 讀取失敗: {e}")
        return None

if __name__ == "__main__":
    print("="*50)
    print("Office 文件讀取工具 - 測試模式")
    print("="*50)
    print("\n請提供 Excel 或 Word 檔案路徑來測試")
    print("用法: python read_office.py <檔案路徑>")
    print("\n已安裝套件:")
    print("  ✓ pandas (Excel 讀取)")
    print("  ✓ openpyxl (Excel 格式)")
    print("  ✓ python-docx (Word 讀取)")
    print("  ✓ Office MCP Skills (GitHub)")
    print("="*50)
    
    if len(sys.argv) > 1:
        filepath = sys.argv[1]
        if filepath.endswith(('.xlsx', '.xls', '.csv')):
            read_excel(filepath)
        elif filepath.endswith('.docx'):
            read_word(filepath)
        else:
            print(f"❌ 不支援的格式: {filepath}")
    else:
        print("\n等待檔案...")

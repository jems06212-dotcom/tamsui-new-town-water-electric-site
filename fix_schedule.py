#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""更新水電進度排程 HTML 文件 - 修復版"""

import json

def fix_schedule_html():
    """修復 HTML 中的 JSON 格式問題"""
    
    html_path = r'D:\OPENCODE專案\新市鎮網頁專案\pages\水電進度排程.html'
    json_path = r'D:\OPENCODE專案\新市鎮網頁專案\schedule_data.json'
    
    # 讀取 HTML
    with open(html_path, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # 讀取新數據
    with open(json_path, 'r', encoding='utf-8') as f:
        tasks = json.load(f)
    
    # 修復：去掉多餘的 [
    # 找到 "const tasks = [\n[" 替換為 "const tasks = [\n"
    html = html.replace('const tasks = [\n[', 'const tasks = [')
    
    # 修復結尾：找到最後的 "\n  ];" 確保只有一個 ]
    # 檢查是否有雙重結尾
    if ']];' in html:
        html = html.replace(']];', '];')
    
    # 寫入修復後的文件
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print('✅ 已修復 JSON 格式')
    
    # 驗證
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 檢查關鍵位置
    tasks_start = content.find('const tasks = [');
    if tasks_start == -1:
        print('❌ 找不到 tasks 起始！')
        return False
    
    # 檢查是否有多餘的 [
    next_char = content[tasks_start + len('const tasks = ['):tasks_start + len('const tasks = [') + 5]
    if next_char.strip().startswith('['):
        print('❌ 仍有雙重 [ 問題！')
        return False
    
    print('✅ JSON 格式驗證通過')
    print(f'📊 總工項: {len(tasks)} 筆')
    
    # 顯示前 3 筆和後 3 筆
    print('\n前 3 筆:')
    for t in tasks[:3]:
        print(f'  {t["main"]} | {t["detail"]} | {t["start"]}')
    
    print('\n後 3 筆:')
    for t in tasks[-3:]:
        print(f'  {t["main"]} | {t["detail"]} | {t["start"]}')
    
    return True

if __name__ == '__main__':
    fix_schedule_html()

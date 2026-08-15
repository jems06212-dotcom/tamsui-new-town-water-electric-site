#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""更新水電進度排程 HTML 使用新的 0704 數據"""

import json

def update_html():
    html_path = r'D:\OPENCODE專案\新市鎮網頁專案\pages\水電進度排程.html'
    json_path = r'D:\OPENCODE專案\新市鎮網頁專案\schedule_data.json'
    
    # 讀取 HTML
    with open(html_path, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # 讀取新數據
    with open(json_path, 'r', encoding='utf-8') as f:
        tasks = json.load(f)
    
    print('讀取到 ' + str(len(tasks)) + ' 筆新工項')
    
    # 更新來源說明
    html = html.replace(
        '來源：淡水新市段進度表_0704.xlsx / 1150602灌漿排程；由 Excel 工作表重新匯入',
        '來源：淡水新市段進度表0704.xlsx / 1150602灌漿排程；由 Excel 工作表重新匯入'
    )
    
    # 找到並替換 tasks JSON
    start_marker = 'const tasks = ['
    start_idx = html.find(start_marker)
    
    if start_idx == -1:
        print('找不到 tasks 起始位置')
        return False
    
    # 找到對應的結束位置
    bracket_count = 0
    json_start = start_idx + len(start_marker) - 1
    
    for i in range(json_start, len(html)):
        if html[i] == '[':
            bracket_count += 1
        elif html[i] == ']':
            bracket_count -= 1
            if bracket_count == 0:
                json_end = i + 1
                break
    
    # 生成新的 JSON
    new_json = json.dumps(tasks, ensure_ascii=False, indent=2)
    
    # 構建新 HTML
    new_html = html[:start_idx + len(start_marker)] + '\n' + new_json + '\n  ' + html[json_end:]
    
    # 寫入
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(new_html)
    
    print('已更新: ' + html_path)
    print('總工項: ' + str(len(tasks)) + ' 筆')
    
    # 驗證
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 檢查 JSON 格式
    test_start = content.find('const tasks = [')
    test_bracket = 0
    test_json_start = test_start + len('const tasks = [') - 1
    for i in range(test_json_start, len(content)):
        if content[i] == '[':
            test_bracket += 1
        elif content[i] == ']':
            test_bracket -= 1
            if test_bracket == 0:
                test_json_end = i + 1
                break
    
    test_json = content[test_json_start:test_json_end]
    try:
        test_tasks = json.loads(test_json)
        print('\nJSON 驗證通過')
        print('工項數量: ' + str(len(test_tasks)))
        
        # 顯示關鍵節點
        print('\n=== 關鍵進度節點 ===')
        for t in test_tasks:
            if '灌漿' in t['detail'] and any(x in t['detail'] for x in ['7FL', '8FL', '9FL', 'RFL']):
                print(t['main'] + ' | ' + t['detail'] + ' | ' + t['start'])
        
        return True
    except json.JSONDecodeError as e:
        print('JSON 驗證失敗: ' + str(e))
        return False

if __name__ == '__main__':
    update_html()

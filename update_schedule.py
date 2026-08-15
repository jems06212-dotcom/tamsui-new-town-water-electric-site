#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""更新水電進度排程 HTML 文件"""

import json
import re
from datetime import datetime

def update_schedule_html():
    """讀取舊 HTML，替換 tasks 數據和元數據"""
    
    # 讀取舊 HTML
    old_html_path = r'C:\Users\User\AppData\Local\Temp\opencode\tamsui-site\pages\水電進度排程.html'
    new_html_path = r'D:\OPENCODE專案\新市鎮網頁專案\pages\水電進度排程.html'
    json_path = r'D:\OPENCODE專案\新市鎮網頁專案\schedule_data.json'
    
    with open(old_html_path, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # 讀取新數據
    with open(json_path, 'r', encoding='utf-8') as f:
        tasks = json.load(f)
    
    print(f'讀取到 {len(tasks)} 筆新工項')
    
    # 更新元數據
    html = html.replace(
        '基準日：2026/06/24',
        '基準日：2026/07/04'
    )
    html = html.replace(
        '來源：淡水新市段進度表_0624.xlsx / 1150602灌漿排程；由 Excel 工作表重新匯入',
        '來源：淡水新市段進度表_0704.xlsx / 1150602灌漿排程；由 Excel 工作表重新匯入'
    )
    html = html.replace(
        '顯示 2026/03 至 2027/08',
        '顯示 2026/03 至 2027/09'
    )
    html = html.replace(
        '依 2026/06/01 與現場更新',
        '依 2026/07/04 與現場更新'
    )
    
    # 找到 tasks 數組並替換
    # 找到 "const tasks = [" 的位置
    start_marker = 'const tasks = ['
    end_marker = '];'
    
    start_idx = html.find(start_marker)
    if start_idx == -1:
        print('找不到 tasks 數組起始位置！')
        return False
    
    # 找到對應的結束位置（最後一個 "];"）
    # 從 script 結尾往前找
    script_end = html.find('</script>', start_idx)
    # 在 script 結尾前找最後一個 "];"
    end_idx = html.rfind(end_marker, start_idx, script_end)
    
    if end_idx == -1:
        print('找不到 tasks 數組結束位置！')
        return False
    
    # 生成新的 JSON 字符串
    new_tasks_json = json.dumps(tasks, ensure_ascii=False, indent=2)
    
    # 構建新的 HTML
    new_html = (
        html[:start_idx + len(start_marker)] + '\n' +
        new_tasks_json + '\n  ' +
        html[end_idx:]
    )
    
    # 寫入新文件
    with open(new_html_path, 'w', encoding='utf-8') as f:
        f.write(new_html)
    
    print(f'✅ 已更新: {new_html_path}')
    print(f'📊 總工項: {len(tasks)} 筆')
    
    # 顯示關鍵節點對比
    print('\n=== 關鍵節點對比 ===')
    key_tasks = ['7FL灌漿', '8FL灌漿', '9FL灌漿', '10FL灌漿', '11FL灌漿', '12FL灌漿', '13FL灌漿', '14FL灌漿', 'RFL灌漿']
    for key in key_tasks:
        for t in tasks:
            if key in t['detail']:
                print(f'{t["detail"]}: {t["start"]} ~ {t["end"]} ({t["days"]}天)')
                break
    
    return True

if __name__ == '__main__':
    update_schedule_html()

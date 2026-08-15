#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""修復民國日期格式問題"""

import json
import re

def fix_minguo_dates():
    """修復民國日期格式（0116-xx-xx → 2027-xx-xx）"""
    
    html_path = r'D:\OPENCODE專案\新市鎮網頁專案\pages\水電進度排程.html'
    json_path = r'D:\OPENCODE專案\新市鎮網頁專案\schedule_data.json'
    
    # 修復 JSON
    with open(json_path, 'r', encoding='utf-8') as f:
        tasks = json.load(f)
    
    fixed_count = 0
    for t in tasks:
        # 檢查開始日期
        if t['start'].startswith('0116-') or t['start'].startswith('116-'):
            # 民國116年 = 2027年
            new_date = '2027' + t['start'][4:]  # 保留月日部分
            t['start'] = new_date
            t['end'] = new_date
            fixed_count += 1
            print('修復: ' + t['detail'] + ' → ' + new_date)
    
    # 儲存修復後的 JSON
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(tasks, f, ensure_ascii=False, indent=2)
    
    # 修復 HTML
    with open(html_path, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # 替換所有 0116- 為 2027-
    html = html.replace('"0116-', '"2027-')
    html = html.replace('"116-', '"2027-')
    
    # 寫入修復後的 HTML
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print('\n✅ 已修復 ' + str(fixed_count) + ' 筆民國日期格式')
    print('📁 JSON 已更新: ' + json_path)
    print('📁 HTML 已更新: ' + html_path)
    
    # 驗證
    print('\n=== 驗證最後 5 筆 ===')
    for t in tasks[-5:]:
        print(t['main'] + ' | ' + t['detail'] + ' | ' + t['start'] + ' ~ ' + t['end'])

if __name__ == '__main__':
    fix_minguo_dates()

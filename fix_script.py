#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""重建水電進度排程 HTML - 保留所有 JavaScript 函數，只替換 tasks 數據"""

import json

def rebuild_html():
    # 原始檔案（從 GitHub clone 保留所有 JS 函數）
    orig_path = r'C:\Users\User\AppData\Local\Temp\opencode\tamsui-site\pages\水電進度排程.html'
    new_json_path = r'D:\OPENCODE專案\新市鎮網頁專案\schedule_data.json'
    output_path = r'D:\OPENCODE專案\新市鎮網頁專案\pages\水電進度排程.html'
    
    # 讀取原始 HTML
    with open(orig_path, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # 讀取新數據
    with open(new_json_path, 'r', encoding='utf-8') as f:
        tasks = json.load(f)
    
    print('原始檔案大小:', len(html), '字元')
    print('新工項:', len(tasks), '筆')
    
    # 更新元數據
    html = html.replace(
        '基準日：2026/06/24',
        '基準日：2026/07/04'
    )
    html = html.replace(
        '來源：淡水新市段進度表_0624.xlsx / 1150602灌漿排程；由 Excel 工作表重新匯入',
        '來源：淡水新市段進度表0704.xlsx / 1150602灌漿排程；由 Excel 工作表重新匯入'
    )
    html = html.replace(
        '顯示 2026/03 至 2027/08',
        '顯示 2026/03 至 2027/09'
    )
    html = html.replace(
        '依 2026/06/01 與現場更新',
        '依 2026/07/04 與現場更新'
    )
    html = html.replace(
        'reportDate = new Date("2026-06-24T00:00:00+08:00")',
        'reportDate = new Date("2026-07-04T00:00:00+08:00")'
    )
    
    # 找到 tasks 數組並替換
    start_marker = 'const tasks = ['
    start_idx = html.find(start_marker)
    
    if start_idx == -1:
        print('找不到 tasks 起始位置！')
        return False
    
    # 找到 JSON 結束位置
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
    
    print('JSON 範圍:', start_idx, '-', json_end)
    
    # 生成新的 JSON
    new_json = json.dumps(tasks, ensure_ascii=False, indent=2)
    
    # 構建新 HTML
    new_html = (html[:start_idx + len(start_marker)] + '\n' + 
                new_json + '\n  ' + 
                html[json_end:])
    
    # 添加灌漿高亮 CSS
    grout_css = """
    .grout-highlight { 
      background: linear-gradient(135deg, #fff8e8 0%, #ffe4b5 100%) !important; 
      border-left: 4px solid #ff6b35 !important;
      font-weight: 700;
    }
    .grout-text { 
      color: #d4380d !important; 
      font-weight: 700;
      font-size: 15px;
    }
    .grout-badge {
      display: inline-flex;
      align-items: center;
      background: #ff6b35;
      color: #fff;
      font-size: 11px;
      font-weight: 700;
      padding: 2px 8px;
      border-radius: 999px;
      margin-right: 6px;
      letter-spacing: 0.5px;
    }
    .bar.grout { 
      background: linear-gradient(90deg, #ff6b35, #ff8c5a) !important; 
      height: 28px;
      box-shadow: 0 2px 8px rgba(255, 107, 53, 0.4);
    }
    .time-row.grout-row {
      background: #fff8e8;
      border-radius: 6px;
      padding: 4px 8px;
      margin: 2px 0;
    }
    tr.grout-row td {
      background: linear-gradient(135deg, #fff8e8 0%, #ffe4b5 100%) !important;
      border-left: 4px solid #ff6b35;
    }
    tr.grout-row td strong {
      color: #d4380d;
      font-size: 15px;
    }
    tr.grout-row:hover td {
      background: linear-gradient(135deg, #fff0d6 0%, #ffd699 100%) !important;
    }"""
    
    new_html = new_html.replace('</style>', grout_css + '\n  </style>')
    
    # 修改 renderTimeline 添加灌漿高亮
    old_timeline = 'return `<div class="time-row"><div class="task-name">${task.main}｜${task.detail}</div><div class="bar-track"><div class="bar ${cls}" style="left:${left}%;width:${width}%"></div><div class="today-line" style="left:${todayLeft}%"></div></div><div class="task-date">${formatDate(task.start)}<br>${formatDate(task.end)}</div></div>`;'
    new_timeline = 'const isGrout = task.detail.includes("灌漿");\n        const groutCls = isGrout ? "grout" : "";\n        const rowCls = isGrout ? "grout-row" : "";\n        const badge = isGrout ? `<span class="grout-badge">灌漿</span>` : "";\n        return `<div class="time-row ${rowCls}"><div class="task-name">${badge}${task.main}｜<span class="${isGrout ? \'grout-text\' : \'\'}">${task.detail}</span></div><div class="bar-track"><div class="bar ${cls} ${groutCls}" style="left:${left}%;width:${width}%"></div><div class="today-line" style="left:${todayLeft}%"></div></div><div class="task-date">${formatDate(task.start)}<br>${formatDate(task.end)}</div></div>`;'
    
    if old_timeline in new_html:
        new_html = new_html.replace(old_timeline, new_timeline)
        print('✅ timeline 灌漿高亮已添加')
    else:
        print('⚠️ timeline 原始代碼不符，嘗試另一種格式')
        # 備用方案：用舊 JSON 裡的 timeline 代碼替換
        old_alt = '''return `<div class="time-row"><div class="task-name">${task.main}｜${task.detail}</div><div class="bar-track"><div class="bar ${cls}" style="left:${left}%;width:${width}%"></div><div class="today-line" style="left:${todayLeft}%"></div></div><div class="task-date">${formatDate(task.start)}<br>${formatDate(task.end)}</div></div>`'''
        if old_alt in new_html:
            new_html = new_html.replace(old_alt, new_timeline)
            print('✅ timeline (alt) 灌漿高亮已添加')
        else:
            print('❌ 找不到 timeline 代碼')
    
    # 修改 renderTable 添加灌漿高亮
    old_table = 'return `<tr><td><span class="tag ${cls}">${task.source}</span></td><td>${task.main}</td><td><strong>${task.detail}</strong></td><td>${formatDate(task.start)}</td><td>${formatDate(task.end)}</td><td>${task.days} 天</td><td>${task.note || ""}</td></tr>`;'
    new_table = 'const isGrout = task.detail.includes("灌漿");\n        const groutCls = isGrout ? "grout-row" : "";\n        const badge = isGrout ? `<span class="grout-badge">灌漿</span>` : "";\n        const detailText = isGrout ? `<span class="grout-text">${task.detail}</span>` : task.detail;\n        return `<tr class="${groutCls}"><td><span class="tag ${cls}">${task.source}</span></td><td>${task.main}</td><td>${badge}<strong>${detailText}</strong></td><td>${formatDate(task.start)}</td><td>${formatDate(task.end)}</td><td>${task.days} 天</td><td>${task.note || ""}</td></tr>`;'
    
    if old_table in new_html:
        new_html = new_html.replace(old_table, new_table)
        print('✅ table 灌漿高亮已添加')
    else:
        old_table_alt = 'return `<tr><td><span class="tag ${cls}">${task.source}</span></td><td>${task.main}</td><td><strong>${task.detail}</strong></td><td>${formatDate(task.start)}</td><td>${formatDate(task.end)}</td><td>${task.days} 天</td><td>${task.note || ""}</td></tr>`'
        if old_table_alt in new_html:
            new_html = new_html.replace(old_table_alt, new_table)
            print('✅ table (alt) 灌漿高亮已添加')
        else:
            print('❌ 找不到 table 代碼')
    
    # 寫入輸出
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(new_html)
    
    print('\n✅ 輸出檔案:', output_path)
    
    # 驗證
    print('\n=== 函數檢查 ===')
    for fn in ['function parseDate', 'function formatDate', 'function dayDiff', 'function isToday', 'function isSite', 'function filteredTasks', 'function renderSummary', 'function renderPhaseFilter', 'function renderTimeline', 'function renderTable']:
        if fn in new_html:
            print(f'  ✅ {fn}')
        else:
            print(f'  ❌ {fn} - 缺失！')
    
    # 驗證 JSON
    check_start = new_html.find('const tasks = [')
    check_bracket = 0
    check_json_start = check_start + len('const tasks = [') - 1
    for i in range(check_json_start, len(new_html)):
        if new_html[i] == '[':
            check_bracket += 1
        elif new_html[i] == ']':
            check_bracket -= 1
            if check_bracket == 0:
                check_json_end = i + 1
                break
    
    check_json = new_html[check_json_start:check_json_end]
    try:
        test_tasks = json.loads(check_json)
        print(f'\n✅ JSON 驗證通過, 工項數: {len(test_tasks)}')
    except json.JSONDecodeError as e:
        print(f'❌ JSON 錯誤: {e}')
    
    return True

if __name__ == '__main__':
    rebuild_html()

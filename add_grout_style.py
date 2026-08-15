#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""為灌漿項目添加高亮顯示"""

import re

def add_grout_highlight():
    html_path = r'D:\OPENCODE專案\新市鎮網頁專案\pages\水電進度排程.html'
    
    with open(html_path, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # 1. 添加 CSS 樣式
    css_additions = """
    /* 灌漿項目高亮 */
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
    
    # 在 </style> 前插入 CSS
    html = html.replace('</style>', css_additions + '\n  </style>')
    
    # 2. 修改 renderTimeline 函數
    # 找到 timeline 渲染部分，添加灌漿判斷
    old_timeline = '''const cls = isSite(task) ? "site" : "";
        return `<div class="time-row"><div class="task-name">${task.main}｜${task.detail}</div><div class="bar-track"><div class="bar ${cls}" style="left:${left}%;width:${width}%"></div><div class="today-line" style="left:${todayLeft}%"></div></div><div class="task-date">${formatDate(task.start)}<br>${formatDate(task.end)}</div></div>`;'''
    
    new_timeline = '''const cls = isSite(task) ? "site" : "";
        const isGrout = task.detail.includes("灌漿");
        const groutCls = isGrout ? "grout" : "";
        const rowCls = isGrout ? "grout-row" : "";
        const badge = isGrout ? `<span class="grout-badge">灌漿</span>` : "";
        return `<div class="time-row ${rowCls}"><div class="task-name">${badge}${task.main}｜<span class="${isGrout ? 'grout-text' : ''}">${task.detail}</span></div><div class="bar-track"><div class="bar ${cls} ${groutCls}" style="left:${left}%;width:${width}%"></div><div class="today-line" style="left:${todayLeft}%"></div></div><div class="task-date">${formatDate(task.start)}<br>${formatDate(task.end)}</div></div>`;'''
    
    html = html.replace(old_timeline, new_timeline)
    
    # 3. 修改 renderTable 函數
    old_table = '''const cls = isSite(task) ? "site" : "";
        return `<tr><td><span class="tag ${cls}">${task.source}</span></td><td>${task.main}</td><td><strong>${task.detail}</strong></td><td>${formatDate(task.start)}</td><td>${formatDate(task.end)}</td><td>${task.days} 天</td><td>${task.note || ""}</td></tr>`;'''
    
    new_table = '''const cls = isSite(task) ? "site" : "";
        const isGrout = task.detail.includes("灌漿");
        const groutCls = isGrout ? "grout-row" : "";
        const badge = isGrout ? `<span class="grout-badge">灌漿</span>` : "";
        const detailText = isGrout ? `<span class="grout-text">${task.detail}</span>` : task.detail;
        return `<tr class="${groutCls}"><td><span class="tag ${cls}">${task.source}</span></td><td>${task.main}</td><td>${badge}<strong>${detailText}</strong></td><td>${formatDate(task.start)}</td><td>${formatDate(task.end)}</td><td>${task.days} 天</td><td>${task.note || ""}</td></tr>`;'''
    
    html = html.replace(old_table, new_table)
    
    # 寫入文件
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print('✅ 已為灌漿項目添加高亮顯示')
    print('')
    print('新增樣式:')
    print('  - 灌漿標籤: 橙色底白字圓角徽章')
    print('  - 灌漿文字: 深紅色加粗大字')
    print('  - 表格行: 暖橙色漸層背景 + 左側橙色邊框')
    print('  - 甘特圖: 橙色漸層條形 + 陰影效果')
    print('  - 行高亮: hover 時加深橙色')

if __name__ == '__main__':
    add_grout_highlight()

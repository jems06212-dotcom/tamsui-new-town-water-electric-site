#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""從 Excel 提取進度數據並轉換為網頁 JSON 格式"""

import pandas as pd
import json
from datetime import datetime

def extract_schedule_data(excel_path, output_json_path):
    """從 Excel 提取進度數據"""
    
    # 讀取 Excel
    df = pd.read_excel(excel_path, sheet_name='1150709灌漿排程', header=None)
    
    tasks = []
    main_phase = ''
    
    for i in range(3, len(df)):
        row = df.iloc[i]
        
        # 檢查是否有編號
        if pd.notna(row[0]) and str(row[0]).strip().isdigit():
            no = str(row[0]).strip()
            milestone = str(row[1]).strip() if pd.notna(row[1]) else ''
            if milestone and milestone != 'nan' and milestone != '':
                main_phase = milestone
            
            detail = str(row[3]).strip() if pd.notna(row[3]) else ''
            start = str(row[4]).strip() if pd.notna(row[4]) else ''
            days = str(row[5]).strip() if pd.notna(row[5]) else ''
            end = str(row[6]).strip() if pd.notna(row[6]) else ''
            note = str(row[7]).strip() if pd.notna(row[7]) else ''
            mep_note = str(row[8]).strip() if pd.notna(row[8]) else ''
            
            # 只保留有詳細工項和開始日期的資料
            if detail and detail != 'nan' and start and start != 'nan':
                try:
                    # 轉換日期格式
                    start_dt = pd.to_datetime(start)
                    start_str = start_dt.strftime('%Y-%m-%d')
                    
                    if end and end != 'nan':
                        end_dt = pd.to_datetime(end)
                        end_str = end_dt.strftime('%Y-%m-%d')
                    else:
                        end_str = start_str
                    
                    # 計算天數
                    if days and days.replace('.','',1).replace('-','').isdigit():
                        days_num = int(float(days))
                    else:
                        days_num = max(1, (pd.to_datetime(end) - pd.to_datetime(start)).days + 1)
                    
                    # 處理備註（包含水電配合備註）
                    full_note = note if note and note != 'nan' else ''
                    if mep_note and mep_note != 'nan' and mep_note != '':
                        if full_note:
                            full_note += '; ' + mep_note
                        else:
                            full_note = mep_note
                    
                    # 處理 main_phase（如果為空，使用 detail 作為 main）
                    task_main = main_phase if main_phase else detail
                    
                    # 處理 mep 欄位（水電/消防配合備註）
                    mep_text = ''
                    if '水電' in detail or '消防' in detail or '配管' in detail or '放樣' in detail:
                        mep_text = f"水電/消防配合：{detail}"
                        if full_note:
                            mep_text += ' ' + full_note
                    
                    tasks.append({
                        'main': task_main,
                        'detail': detail,
                        'start': start_str,
                        'end': end_str,
                        'days': days_num,
                        'note': full_note,
                        'mep': mep_text,
                        'source': '淡水新市段進度表0709.xlsx / 1150709灌漿排程'
                    })
                    
                except Exception as e:
                    print(f"跳過第 {i} 行: {e}")
                    continue
    
    # 儲存 JSON
    with open(output_json_path, 'w', encoding='utf-8') as f:
        json.dump(tasks, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 成功提取 {len(tasks)} 筆工項")
    print(f"📁 已儲存至: {output_json_path}")
    
    return tasks

if __name__ == '__main__':
    excel_path = r'D:\OPENCODE專案\新市鎮網頁專案\淡水新市段進度表0709.xlsx'
    output_path = r'D:\OPENCODE專案\新市鎮網頁專案\schedule_data.json'
    
    tasks = extract_schedule_data(excel_path, output_path)
    
    # 顯示統計
    print(f"\n📊 數據統計:")
    phases = {}
    for t in tasks:
        p = t['main']
        if p not in phases:
            phases[p] = 0
        phases[p] += 1
    
    for phase in ['基礎工程', '大底到B4FL', 'B4FL牆面', 'B3FL版面', 'B2FL版面', 'B1F版面', '1F', '1MF', '2FL', '3FL', '4FL', '5FL', '6FL', '7FL', '8FL', '9FL', 'RF']:
        if phase in phases:
            print(f"  {phase}: {phases[phase]} 項")

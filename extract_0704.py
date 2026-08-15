#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""提取新的 0704 Excel 數據"""

import pandas as pd
import json

def extract_new_schedule():
    excel_path = r'D:\OPENCODE專案\新市鎮網頁專案\淡水新市段進度表0704.xlsx'
    output_path = r'D:\OPENCODE專案\新市鎮網頁專案\schedule_data.json'
    
    df = pd.read_excel(excel_path, sheet_name='1150602灌漿排程', header=None)
    
    tasks = []
    main_phase = ''
    
    for i in range(3, len(df)):
        row = df.iloc[i]
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
            
            if detail and detail != 'nan' and start and start != 'nan':
                try:
                    start_dt = pd.to_datetime(start)
                    start_str = start_dt.strftime('%Y-%m-%d')
                    
                    if end and end != 'nan':
                        end_dt = pd.to_datetime(end)
                        end_str = end_dt.strftime('%Y-%m-%d')
                    else:
                        end_str = start_str
                    
                    if days and days.replace('.','',1).replace('-','').isdigit():
                        days_num = int(float(days))
                    else:
                        days_num = max(1, (pd.to_datetime(end) - pd.to_datetime(start)).days + 1)
                    
                    full_note = note if note and note != 'nan' else ''
                    if mep_note and mep_note != 'nan' and mep_note != '':
                        if full_note:
                            full_note += '; ' + mep_note
                        else:
                            full_note = mep_note
                    
                    task_main = main_phase if main_phase else detail
                    
                    # 修復民國日期
                    if start_str.startswith('0116'):
                        start_str = '2027' + start_str[4:]
                        end_str = '2027' + end_str[4:]
                    
                    mep_text = ''
                    if '水電' in detail or '消防' in detail or '配管' in detail or '放樣' in detail:
                        mep_text = '水電/消防配合：' + detail
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
                        'source': '淡水新市段進度表0704.xlsx / 1150602灌漿排程'
                    })
                except:
                    pass
    
    # 儲存 JSON
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(tasks, f, ensure_ascii=False, indent=2)
    
    print('成功提取 ' + str(len(tasks)) + ' 筆工項')
    print('\n前 3 筆:')
    for t in tasks[:3]:
        print('  ' + t['main'] + ' | ' + t['detail'] + ' | ' + t['start'])
    print('\n後 3 筆:')
    for t in tasks[-3:]:
        print('  ' + t['main'] + ' | ' + t['detail'] + ' | ' + t['start'])
    
    return tasks

if __name__ == '__main__':
    extract_new_schedule()

from bs4 import BeautifulSoup
import json
import re
import pandas as pd
from tqdm import tqdm
import os

def clean_name(raw_name):
    """清洗姓名中的冗余信息"""
    if raw_name:
        cleaned = re.split(r'查看|的档案', raw_name)[0].strip()
        return cleaned.replace('\u200b', '')  # 移除零宽空格
    return "--"

def clean_position(position):
    if position:
        cleaned=position.replace('&','and')
        return cleaned
    return '--'

def init_output_files(organization):
    """初始化输出文件"""
    # JSON文件初始化
    json_file = f"{organization}.json"
    if not os.path.exists(json_file):
        with open(json_file, 'w', encoding='utf-8') as f:
            f.write('[]')
    
    # Excel文件初始化
    excel_file = f"{organization}.xlsx"
    if not os.path.exists(excel_file):
        pd.DataFrame(columns=['姓名', '公司及职位', '个人主页']).to_excel(excel_file, index=False)

def append_to_json(new_data, organization):
    """增量写入JSON文件"""
    json_file = f"{organization}.json"
    
    # 读取现有数据
    with open(json_file, 'r+', encoding='utf-8') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            data = []
        
        # 追加新数据
        data.extend(new_data)
        f.seek(0)
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.truncate()

def append_to_excel(new_data, organization):
    """增量写入Excel文件"""
    excel_file = f"{organization}.xlsx"
    
    # 读取现有数据
    try:
        df_existing = pd.read_excel(excel_file)
    except:
        df_existing = pd.DataFrame()
    
    # 合并数据
    df_new = pd.DataFrame(new_data)
    df_combined = pd.concat([df_existing, df_new], ignore_index=True)
    
    # 覆盖写入
    df_combined.to_excel(excel_file, index=False)

def process_html(file_path, organization):
    """处理单个HTML文件"""
    with open(file_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')

    profiles = []
    
    # 解析用户条目
    for item in soup.find_all('li', class_='kZRArQqqhjjrHYceWaFbyEGWHRZbtqjTMawKA'):
        # 姓名提取
        name_span = item.find('span', {'aria-hidden': 'true'}, class_=False)
        raw_name = name_span.get_text(strip=True) if name_span else None
        name = clean_name(raw_name)
        
        # 个人主页
        profile_link = item.find('a', {'data-test-app-aware-link': True})
        profile_url = profile_link['href'] if profile_link else "--"
        
        # 公司职位
        company_tag = item.find('div', class_=lambda x: x and 'kFTZPhxHBbvnnRxiRPmTxafKGLUNSiaeInag' in x)
        company_position = company_tag.get_text(strip=True) if company_tag else "--"
        company_position = clean_position(company_position)
        
        profiles.append({
            "姓名": name,
            "公司及职位": company_position,
            "个人主页": profile_url
        })
    
    # 增量写入文件
    if profiles:
        append_to_json(profiles, organization)
        append_to_excel(profiles, organization)

if __name__ == "__main__":

    #organizations = ['作业帮','Stealth Health',','StepFun','ModelBest','A4X','','Shopee','OpenAI','Amazon']
    organizations = ['Liblib','voc.ai']
    
    for org in organizations:
        print(f"正在处理组织：{org}")
        init_output_files(org)
        
        html_dir = f"./{org}"
        files = [f for f in os.listdir(html_dir) if f.endswith('.html')]
        # 创建进度条
        with tqdm(total=len(files), unit='file', desc=org) as pbar:
            for file in files:
                file_path = os.path.join(html_dir, file)
                process_html(file_path, org)
                pbar.update(1)
    
    print("数据处理完成，输出文件：")
    for org in organizations:
        print(f"- {org}.json")
        print(f"- {org}.xlsx")

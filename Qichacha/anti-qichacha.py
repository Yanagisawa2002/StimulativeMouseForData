from bs4 import BeautifulSoup
import pandas as pd

def extract_finance_data(html_content):
    """从HTML内容中提取融资事件数据"""
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # 定位表格主体
    tbody = soup.find('tbody', class_='qccd-table-tbody')
    if not tbody:
        print("未找到数据表格")
        return []
    
    rows = tbody.find_all('tr')
    data = []
    
    for row in rows:
        cells = row.find_all('td')
        if len(cells) < 9:  # 确保有足够的列
            continue
            
        # 提取各列数据
        serial = cells[0].get_text(strip=True)
        date = cells[1].get_text(strip=True)
        
        # 品牌产品名称可能有嵌套结构
        brand_cell = cells[2]
        brand = brand_cell.get_text(strip=True)
        if not brand:
            brand_link = brand_cell.find('a')
            if brand_link:
                brand = brand_link.get_text(strip=True)
        
        # 行业信息
        industry_new = cells[3].get_text(strip=True)
        industry_national = cells[4].get_text(strip=True)
        
        # 融资信息
        round_ = cells[5].get_text(strip=True)
        amount = cells[6].get_text(strip=True)
        
        # 投资方可能有多个
        investors_cell = cells[7]
        investors = []
        for a_tag in investors_cell.find_all('a'):
            investors.append(a_tag.get_text(strip=True))
        investors_str = ", ".join(investors)
        
        country = cells[8].get_text(strip=True)
        
        data.append([
            serial, date, brand, industry_new, 
            industry_national, round_, amount, 
            investors_str, country
        ])
    
    return data

# 主程序
if __name__ == "__main__":
    html_files = [str(i) + '.html' for i in range(1, 37)]
    #html_files = ['1.html', '2.html', '3.html']
    all_finance_data = []

    for html_file in html_files:
        try:
            with open(html_file, 'r', encoding='utf-8') as file:
                html_content = file.read()
            print(f"开始解析文件 {html_file} ...")
            finance_data = extract_finance_data(html_content)
            if finance_data:
                all_finance_data.extend(finance_data)
            else:
                print(f"文件 {html_file} 未获取到数据，请检查HTML文件内容")
        except Exception as e:
            print(f"读取文件 {html_file} 时出错: {e}")

    if all_finance_data:
        # 创建DataFrame
        df = pd.DataFrame(all_finance_data, columns=[
            '序号', '融资日期', '品牌产品名称', '新兴行业',
            '国标行业', '融资轮次', '融资金额', 
            '投资方', '所属国家'
        ])
        
        # 导出到Excel
        output_file = "企查查融资事件.xlsx"
        df.to_excel(output_file, index=False)
        print(f"成功导出数据到 {output_file}")
    else:
        print("所有文件均未获取到数据，请检查HTML文件内容")
import os
import time
import requests
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
import csv
from bs4 import BeautifulSoup

def scrape_detail_page(url):
    """
    使用 requests 和 BeautifulSoup 爬取详情页
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        dl = soup.find('dl', class_='tw-grid')
        
        result = {}
        result['Details URL'] = url
        
        # 遍历所有基本信息
        for div in dl.find_all('div', class_='tw-border-t'):
            dt = div.find('dt')
            dd = div.find('dd')
            
            if dt and dd:
                title = dt.text.strip()
                content = dd.text.strip()
                
                if title == 'Institution':
                    result['Institution'] = content
                elif title == 'Program':
                    result['Program'] = content
                elif title == 'Degree Type':
                    result['Degree Type'] = content
                elif "Country of Origin" in title:
                    result['Country'] = content
                elif title == 'Decision':
                    result['Decision'] = content
                elif title == 'Notification':
                    # 分离通知日期和方式
                    if 'via' in content:
                        date, method = content.split('via')
                        result['Notification Date'] = date.strip()
                        result['Notification Method'] = method.strip()
                    else:
                        result['Notification Date'] = content
                        result['Notification Method'] = ''
                elif 'Undergrad GPA' in title:
                    result['Undergrad GPA'] = content
        
        # 获取GRE分数
        gre_ul = dl.find('ul', class_='tw-list-none')
        if gre_ul:
            for li in gre_ul.find_all('li'):
                spans = li.find_all('span')
                if len(spans) >= 2:
                    title = spans[0].text.strip()
                    value = spans[1].text.strip()
                    
                    if 'GRE General:' in title:
                        result['GRE General'] = value
                    elif 'GRE Verbal:' in title:
                        result['GRE Verbal'] = value
                    elif 'Analytical Writing:' in title:
                        result['Analytical Writing'] = value
        
        # 获取Notes
        notes_div = dl.find('div', class_='tw-border-y')
        if notes_div:
            notes_dd = notes_div.find('dd')
            if notes_dd:
                result['Notes'] = notes_dd.text.strip()
        
        # 确保所有字段都存在，没有的设为空字符串
        required_fields = [
            'Institution', 'Program', 'Degree Type', 'Country', 
            'Decision', 'Notification Date', 'Notification Method',
            'Undergrad GPA', 'GRE General', 'GRE Verbal', 
            'Analytical Writing', 'Notes', 'Details URL'
        ]
        
        for field in required_fields:
            if field not in result:
                result[field] = ''
        
        return result
        
    except Exception as e:
        print(f"爬取详情页出错 {url}: {e}")
        return None

def get_phd_results(institution, degree_type=None, program=None, start_date=None, end_date=None, max_pages=None):
    """
    使用 requests + BeautifulSoup 获取搜索结果页面的项目
    参数:
        institution: 院校名称
        degree_type: 学位类型 ('PhD' 或 'Masters')
        program: 专业名称
        start_date: 起始日期 (格式: YYYY-MM-DD)
        end_date: 结束日期 (格式: YYYY-MM-DD)
        max_pages: 最大爬取页数，None表示不限制页数
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    encoded_institution = institution.replace(' ', '+')
    details_urls = []
    page = 1
    
    while True:
        # 如果设置了最大页数且已达到，则退出
        if max_pages and page > max_pages:
            break
            
        search_url = f"https://www.thegradcafe.com/survey/?q={encoded_institution}&page={page}"
        
        try:
            response = requests.get(search_url, headers=headers)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            rows = soup.select("tbody.tw-divide-y tr:not(.tw-border-none)")
            
            # 如果没有结果或页面不存在，退出循环
            if not rows:
                break
                
            for row in rows:
                try:
                    # 检查学位类型
                    degree_info = row.select_one("td:nth-child(2) div.tw-text-gray-900")
                    if degree_type and degree_info:
                        if degree_type not in degree_info.text:
                            continue
                    
                    # 检查专业
                    program_info = row.select_one("td:nth-child(2) span:first-child")
                    if program and program_info:
                        if program.lower() not in program_info.text.lower():
                            continue
                    
                    # 获取日期
                    date_cell = row.select_one("td:nth-child(3)")
                    if date_cell:
                        date_str = date_cell.text.strip()
                        try:
                            date_obj = pd.to_datetime(date_str)
                            
                            if start_date and date_obj < pd.to_datetime(start_date):
                                continue
                            if end_date and date_obj > pd.to_datetime(end_date):
                                continue
                                
                            see_more_link = row.select_one("a[href^='/result/']")
                            if see_more_link:
                                detail_url = "https://www.thegradcafe.com" + see_more_link['href']
                                details_urls.append(detail_url)
                        except:
                            continue
                except Exception as e:
                    print(f"处理行时出错: {e}")
                    continue
            
            print(f"已处理第 {page} 页")
            time.sleep(1)
            page += 1
            
        except Exception as e:
            print(f"获取第 {page} 页搜索结果出错: {e}")
            break
    
    return details_urls

def run_crawler(input_file_path, output_folder_path, degree_type=None, program=None, start_date=None, end_date=None, max_pages=None, start_index=0):
    """
    爬虫主函数
    参数:
        degree_type: 学位类型 ('PhD' 或 'Masters')
        program: 专业名称
        start_date: 起始日期 (格式: YYYY-MM-DD)
        end_date: 结束日期 (格式: YYYY-MM-DD)
        max_pages: 最大爬取页数，None表示不限制页数
    """
    output_file_path = os.path.join(output_folder_path, 'results.csv')
    temp_file_path = os.path.join(output_folder_path, 'temp_results.csv')

    # 读取院校列表
    institutions = read_institution_file(input_file_path)
    
    # 读取已有的结果（如果存在）
    all_results = []
    if os.path.exists(temp_file_path):
        with open(temp_file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            all_results = list(reader)

    for i, institution in enumerate(institutions[start_index:], start=start_index):
        print(f"正在搜索院校 [{i+1}/{len(institutions)}]: {institution}")
        
        try:
            details_urls = get_phd_results(institution, degree_type, program, start_date, end_date, max_pages)
            
            for url in details_urls:
                result = scrape_detail_page(url)
                if result:
                    all_results.append(result)
                    save_results_to_csv(all_results, temp_file_path)
                time.sleep(1)
                
        except Exception as e:
            print(f"处理院校 {institution} 时出错: {e}")
            save_results_to_csv(all_results, temp_file_path)
            continue

    # 全部完成后，保存最终结果
    save_results_to_csv(all_results, output_file_path)
    # 删除临时文件
    if os.path.exists(temp_file_path):
        os.remove(temp_file_path)

    return all_results

def read_institution_file(file_path):
    if file_path.endswith('.csv'):
        return pd.read_csv(file_path)['Institution'].tolist()
    elif file_path.endswith('.xlsx'):
        return pd.read_excel(file_path)['Institution'].tolist()
    else:
        raise ValueError("文件格式不支持，请使用CSV或Excel文件。")

def save_results_to_csv(results, output_file):
    # 更新表头以匹配新的数据结构
    keys = [
        'Institution', 'Program', 'Degree Type', 'Country', 
        'Decision', 'Notification Date', 'Notification Method',
        'Undergrad GPA', 'GRE General', 'GRE Verbal', 
        'Analytical Writing', 'Notes', 'Details URL'
    ]
    
    with open(output_file, 'w', newline='', encoding='utf-8') as output_csv:
        dict_writer = csv.DictWriter(output_csv, fieldnames=keys)
        dict_writer.writeheader()
        dict_writer.writerows(results)

def main():
    input_file_path = input("请输入输入文件的路径（CSV或Excel）：")
    output_folder_path = input("请输入输出结果的文件夹路径：")
    
    # 添加学位类型输入
    degree_type = input("请输入学位类型 (PhD/Masters，直接回车则不限制)：").strip()
    degree_type = degree_type if degree_type else None
    
    # 添加专业输入
    program = input("请输入专业名称（直接回车则不限制）：").strip()
    program = program if program else None
    
    # 添加日期范围输入
    start_date = input("请输入起始日期 (YYYY-MM-DD，直接回车则不限制)：").strip()
    end_date = input("请输入结束日期 (YYYY-MM-DD，直接回车则不限制)：").strip()
    
    start_date = start_date if start_date else None
    end_date = end_date if end_date else None
    
    # 添加最大页数输入
    max_pages = input("请输入最大爬取页数（直接回车则不限制）：").strip()
    max_pages = int(max_pages) if max_pages else None
    
    run_crawler(input_file_path, output_folder_path, degree_type, program, start_date, end_date, max_pages)
    
# 运行主程序
if __name__ == "__main__":
    main()

from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

import time
import sqlite3
import random
import re

db_path = './info.db'

def sleep_wait():
    # 随机生成6到8秒之间的浮点数时间
    sleep_time = random.uniform(3, 5)
    time.sleep(sleep_time)
    pass

def save_html(path, html_text):
    html_text_utf8 = html_text.encode('gb2312').decode('gb2312').encode('utf-8')
    with open(path,'wb') as f:
        f.write(html_text_utf8)
    pass

def create_db():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS apartments")
    cursor.execute('''
        CREATE TABLE apartments (
            location TEXT,
            number TEXT,
            floor INT,
            inner_area REAL,
            shared_area REAL,
            balcony_area REAL,
            sale_area REAL,
            build_area REAL,
            type TEXT
        )
    ''')
    conn.commit()
    conn.close()
    pass

def insert_apartment_info(html_text):
    # Connect to the database
    conn = sqlite3.connect('info.db')
    cursor = conn.cursor()

    # Use BeautifulSoup to parse the HTML
    soup = BeautifulSoup(html_text, 'html.parser')

    # Initialize an empty dictionary to hold the apartment data
    apartment_data = {
        'location': '',
        'number': '',
        'floor': 0,
        'inner_area': 0.0,
        'shared_area': 0.0,
        'balcony_area': 0.0,
        'sale_area': 0.0,
        'build_area': 0.0,
        'type': ''
    }

    # Find the specific table that contains the data
    table = soup.find_all('table')[3]  # This assumes that the correct table is the fourth one in your HTML
    rows = table.find_all('tr')

    # Map the text to the correct dictionary key
    for row in rows:
        cells = row.find_all('td')
        if len(cells) == 2:
            key = cells[0].get_text(strip=True).replace('：', '')
            value = cells[1].get_text(strip=True)

            if value == '':
                continue

            if key == '座落':
                apartment_data['location'] = value
            elif key == '门牌':
                apartment_data['number'] = value
                pattern = r'-(\d+)-'
                match = re.search(pattern, value)
                if match:
                    apartment_data['floor'] = int(match.group(1))
                else:
                    apartment_data['floor'] = 0
            elif key == '套内面积':
                apartment_data['inner_area'] = float(value)
            elif key == '分摊面积':
                apartment_data['shared_area'] = float(value)
            elif key == '阳台面积':
                apartment_data['balcony_area'] = float(value)
            elif key == '销售面积':
                apartment_data['sale_area'] = float(value)
            elif key == '建筑面积':
                apartment_data['build_area'] = float(value)
            elif key == '房屋类型':
                apartment_data['type'] = value

    # Insert the data into the database
    cursor.execute('''
        INSERT INTO apartments (location, number, floor, inner_area, shared_area, balcony_area, sale_area, build_area, type)
        VALUES (:location, :number, :floor, :inner_area, :shared_area, :balcony_area, :sale_area, :build_area, :type)
    ''', apartment_data)

    # Commit changes and close the connection
    conn.commit()
    conn.close()
    pass

def start_web_browser():
    # 指定Edge WebDriver的路径
    webdriver_path = './msedgedriver.exe'
    service = Service(webdriver_path)

    # 设置无头模式
    # options = Options()
    # options.add_argument('--headless')
    # options.add_argument('--disable-gpu')  # 这有助于在某些系统中防止某些问题，虽然不一定需要

    driver = webdriver.Edge(service=service)
    # driver.maximize_window()
    # 打开网页
    url = '''http://124.95.133.164/work/xjlp/build_list.jsp?xmmcid=2021_DC_00_1376&xmmc=%BE%D3%D7%A1%C9%CC%D2%B5%A3%A8HN-20006%BA%C5%B8%DF%C9%EE%B6%AB%C2%B7%B1%B1-1%B5%D8%BF%E9%A3%A9'''
    driver.get(url)
    sleep_wait()

    # save_html('./temp1.html',driver.page_source)

    # 获取所有的行元素
    rows = driver.find_elements(By.CSS_SELECTOR, 'tr')

    for row in rows:
        # 尝试获取第一个td元素并检查它是否align="left"
        left_td = row.find_elements(By.CSS_SELECTOR, 'td[align="left"]')
        if left_td:  # 存在align="left"的td
            # 检查旁边的td中的值
            next_td = left_td[0].find_element(By.XPATH, './following-sibling::td')
            if next_td.text != "0":
                # 查找并点击链接
                link = left_td[0].find_element(By.TAG_NAME, 'a')
                link_href = link.get_attribute('href')
                driver.execute_script("window.open(arguments[0]);", link_href)
                driver.switch_to.window(driver.window_handles[1])  # 切换到新窗口
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
                sleep_wait()

                # 切换到iframe
                iframe = driver.find_element(By.CSS_SELECTOR, 'iframe')
                driver.switch_to.frame(iframe)


                # 查找具有特定背景色的元素，并检查它们内部是否含有可点击的<a>标签
                elements_with_bg = driver.find_elements(By.CSS_SELECTOR, '[bgcolor="#00FF00"]')


                for element in elements_with_bg:
                    links = []
                    try:
                        links = element.find_elements(By.CSS_SELECTOR, 'a[href]')
                    except Exception as e:
                        print(f"发生错误：{e}")
                        pass
                    if len(links) > 0:
                        link =links[0]
                        # 打开链接前先保存当前窗口句柄
                        original_window = driver.current_window_handle
                        # 点击链接，假设这会打开一个新窗口
                        link.click()

                        # 等待新窗口打开
                        WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(len(driver.window_handles)))
                        # 切换到新窗口
                        driver.switch_to.window(driver.window_handles[2])  # 切换到新窗口

                        # 获取新窗口中的HTML并保存
                        final_html = driver.page_source
                        # save_html('./temp3.html', final_html)
                        insert_apartment_info(final_html)
                        sleep_wait()
                        # 关闭新窗口并返回到iframe所在的窗口
                        driver.close()
                        # driver.switch_to.window(original_window)

                        driver.switch_to.window(driver.window_handles[1])
                        temp_iframe = driver.find_element(By.CSS_SELECTOR, 'iframe')
                        driver.switch_to.frame(temp_iframe)

                    else:
                        print("No clickable <a> tags found inside this element with bgcolor #00FF00.")
                    pass


                # 最后，从iframe返回到主窗口
                driver.switch_to.default_content()

                # 关闭新窗口并返回主窗口
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
                sleep_wait()

    # 关闭浏览器
    driver.quit()

    pass


if __name__ == '__main__':
    create_db()
    start_web_browser()

    # with open('./temp3.html','rb') as f:
    #     html_text = f.read()
    #     insert_apartment_info(html_text)

    print('ended..')
    pass
import requests
from bs4 import BeautifulSoup

import download_files

res = requests.get('http://interesting-sky.china-vo.org/telescope_astronomical/data_astronomical/astronomical_data/').text


soup = BeautifulSoup(res, 'html.parser')  # 文档对象
# print(soup)
for tr in soup.find_all('tr'):
    # print(tr.find('a'))
    try:
        name_py = tr.find('a').get('href')
        print(name_py)
        if '.py' in name_py and 'upload_node' not in name_py:
            download_files.download_file(fr"http://interesting-sky.china-vo.org/telescope_astronomical/data_astronomical/astronomical_data/{name_py}", f"{name_py}")
    except:
        pass
print('更新py脚本完成！')
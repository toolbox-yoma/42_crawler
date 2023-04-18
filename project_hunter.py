from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random
from datetime import datetime
import csv
import os
import requests

### set_init_info
# 상위 폴더에 있는 id_info.info에
# 첫줄에   ID
# 둘째줄에 PASS
# 셋째줄에 target path
f = open("../id_info.info", "r")
file_lines = f.readlines()
f.close()
user_id = file_lines[0].strip()
user_pass = file_lines[1].strip()
target_path = file_lines[2].strip()
to_path = '../' + target_path + '/'
def dic_to_string(key, value):
    return key + "," + value + "\n"

def save_url_list(dict):
    with open(to_path + 'project_url.csv', mode='w+') as file:
        file.write("")
        for key, value in dict.items():
            file.write(dic_to_string(key, value))

project_dict = {}
is_change = 0

with open(to_path + 'project_url.csv', mode='r') as file:
    csv_reader = csv.reader(file)
    for row in csv_reader:
        project_dict[row[0]] = row[1]


options = webdriver.ChromeOptions()
prefs = {'profile.default_content_setting_values': {'cookies': 1, 'images': 2, 'javascript': 1,
                            'plugins': 2, 'popups': 1, 'geolocation': 2,
                            'notifications': 2, 'auto_select_certificate': 2, 'fullscreen': 2,
                            'mouselock': 2, 'mixed_script': 2, 'media_stream': 2,
                            'media_stream_mic': 2, 'media_stream_camera': 2, 'protocol_handlers': 2,
                            'ppapi_broker': 2, 'automatic_downloads': 2, 'midi_sysex': 2,
                            'push_messaging': 2, 'ssl_cert_decisions': 2, 'metro_switch_to_desktop': 2,
                            'protected_media_identifier': 2, 'app_banner': 2, 'site_engagement': 2,
                            'durable_storage': 2}}
options.add_experimental_option('prefs', prefs)
### headlest mode
# options.add_argument('headless')
options.add_argument('User-Agent: xxxxxxxxxxxxxxx')
options.add_argument("disable-infobars")
options.add_argument("--disable-extensions")
#driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
# add your chromedriver path
service = Service(executable_path="./chromedriver_m1")
driver = webdriver.Chrome(service=service, options=options)

url = 'https://intra.42.fr'
projects_url = 'https://projects.intra.42.fr/projects/list'

###  init_intra_macro
driver.get(url)
wait = WebDriverWait(driver, 5)
driver.implicitly_wait(2)
driver.find_element(By.CLASS_NAME, 'btn-login-student').click()

#driver.get_screenshot_as_file('intra_main_headless.png')
driver.find_element(By.NAME, 'username').send_keys(user_id)
driver.find_element(By.NAME, 'password').send_keys(user_pass)
driver.find_element(By.NAME, 'login').click()
print("\n\nlogin success   >>>>")

driver.get(projects_url)
print("\n\nproject url success   >>>>")

actions = ActionChains(driver)

index = 0
target_project_list = driver.find_elements(By.CLASS_NAME, 'project-name')
project_size = len(target_project_list)

while index < project_size:
    target_project_list[index].find_element(By.TAG_NAME, 'a').click()

    #per project site
    name = driver.find_element(By.CLASS_NAME, 'project-header')
    attach_list = driver.find_elements(By.CLASS_NAME, 'project-attachment-item')
    result = 'pass  '
    old_id = ''
    if name.text in project_dict:
        old_id = project_dict[name.text]

    project_id = ''
    update_subject = 0
    save_path = to_path + name.text
    for item in attach_list:
        link = item.find_element(By.TAG_NAME, 'a')
        if link.text == 'subject.pdf':
            download_link = link.get_attribute('href')
            project_id = download_link.split('/')[-2]
            if name.text not in project_dict:
                project_dict[name.text] = project_id
                update_subject = 1
                result = '\033[92m' + 'New   ' + '\033[0m'
            elif project_dict[name.text] != project_id:
                project_dict[name.text] = project_id
                update_subject = 1
                result = '\033[93m' + 'Update' + '\033[0m'
    if update_subject:
        is_change = 1
        temp = name.text
        if temp.count('-') == 2:
            split_list = temp.split('-')
            check_is_number = split_list[1].strip()
            if check_is_number.isdigit():
                print("- {} - : found number!".format(check_is_number))
                opti_name = split_list[0]
                opti_path = to_path + opti_name
                save_path = opti_path + '/[' + split_list[1] + '] ' + split_list[2]
                if not os.path.exists(opti_path):
                    os.mkdir(opti_path)

        if not os.path.exists(save_path):
            os.mkdir(save_path)
        driver.save_screenshot(save_path + '/image.png')
        for item in attach_list:
            link = item.find_element(By.TAG_NAME, 'a')
            download_link = link.get_attribute('href')
            response = requests.get(download_link)
            with open(save_path + '/' + link.text, 'wb') as f:
                f.write(response.content)
    if is_change:
        save_url_list(project_dict)
    is_change = 0
    print('{}] {} - [{:<6}]->[{:<6}] : {}'.format(index, result, old_id, project_id, name.text))

    parent_name = name.text
    parent_path = save_path

    item_list = driver.find_elements(By.CLASS_NAME,'project-list-item')
    other_project_size = len(item_list)
    other_index = 0
    while other_index < other_project_size:
        item_list[other_index].find_element(By.TAG_NAME, 'a').click()
        name = driver.find_element(By.CLASS_NAME, 'project-header')
        temp = name.text
        child_name = temp.split('>')[-1]
        csv_name = parent_name + ':' + child_name
        other_attach_list = driver.find_elements(By.CLASS_NAME, 'project-attachment-item')
        result = 'pass  '
        old_id = ''
        if csv_name in project_dict:
            old_id = project_dict[csv_name]

        project_id = ''
        update_subject = 0
        need_pdf_surfix = 0
        for item in other_attach_list:
            link = item.find_element(By.TAG_NAME, 'a')
            if link.text == 'subject.pdf' or link.text == 'subject':
                if link.text == 'subject':
                    need_pdf_surfix = 1
                download_link = link.get_attribute('href')
                project_id = download_link.split('/')[-2]
                if csv_name not in project_dict:
                    project_dict[csv_name] = project_id
                    update_subject = 1
                    result = '\033[92m' + 'New   ' + '\033[0m'
                elif project_dict[csv_name] != project_id:
                    project_dict[csv_name] = project_id
                    update_subject = 1
                    result = '\033[93m' + 'Update' + '\033[0m'
        if update_subject:
            is_change = 1
            save_path = to_path + parent_name + '/[' + str(other_index + 1) + ']' + child_name
            if not os.path.exists(parent_path):
                os.mkdir(parent_path)
            if not os.path.exists(save_path):
                os.mkdir(save_path)
            driver.save_screenshot(save_path + '/image.png')
            for item in other_attach_list:
                link = item.find_element(By.TAG_NAME, 'a')
                download_link = link.get_attribute('href')
                response = requests.get(download_link)
                if need_pdf_surfix:
                    with open(save_path + '/' + link.text + ".pdf", 'wb') as f:
                        f.write(response.content)
                else:
                    with open(save_path + '/' + link.text, 'wb') as f:
                        f.write(response.content)
        if is_change:
            save_url_list(project_dict)
        is_change = 0
        print('{}:{}] {} - [{:<6}]->[{:<6}] : {}'.format(index, other_index, result, old_id, project_id, name.text))
        driver.back()
        item_list = driver.find_elements(By.CLASS_NAME,'project-list-item')
        other_index += 1

    print('')
    driver.back()
    target_project_list = driver.find_elements(By.CLASS_NAME, 'project-name')
    index += 1


driver.quit()

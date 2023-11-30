import csv
import os
import time
from datetime import datetime

import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


# from webdriver_manager.chrome import ChromeDriverManager
class Account:
    def __init__(self):
        # file_lines = ""
        with open("../id_info.info", "r") as f:
            file_lines = f.readlines()
        self.user_id = file_lines[0].strip()
        self.user_pass = file_lines[1].strip()
        self.target_path = file_lines[2].strip()
        self.save_path = "../" + self.target_path + "/"

    def __str__(self):
        print(self.user_id)
        print(self.user_pass)
        print(self.target_path)
        print(self.save_path)


class Driver:
    def __init__(self, id, password, save) -> None:
        self.id = id
        self.password = password
        self.save = save
        self.url = "https://intra.42.fr"
        self.projects_url = "https://projects.intra.42.fr/projects/list"
        self.project_dict = {}
        now = datetime.now()
        self.current_date = now.strftime("%Y-%m-%d")
        self.load_url_dict()
        options = webdriver.ChromeOptions()
        prefs = {
            "profile.default_content_setting_values": {
                "cookies": 1,
                "images": 2,
                "javascript": 1,
                "plugins": 2,
                "popups": 1,
                "geolocation": 2,
                "notifications": 2,
                "auto_select_certificate": 2,
                "fullscreen": 2,
                "mouselock": 2,
                "mixed_script": 2,
                "media_stream": 2,
                "media_stream_mic": 2,
                "media_stream_camera": 2,
                "protocol_handlers": 2,
                "ppapi_broker": 2,
                "automatic_downloads": 2,
                "midi_sysex": 2,
                "push_messaging": 2,
                "ssl_cert_decisions": 2,
                "metro_switch_to_desktop": 2,
                "protected_media_identifier": 2,
                "app_banner": 2,
                "site_engagement": 2,
                "durable_storage": 2,
            }
        }
        options.add_experimental_option("prefs", prefs)
        ### headlest mode
        # options.add_argument('headless')
        options.add_argument("User-Agent: xxxxxxxxxxxxxxx")
        options.add_argument("disable-infobars")
        options.add_argument("--disable-extensions")
        # driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        # add your chromedriver path
        service = Service(executable_path="./chromedriver")
        self.driver = webdriver.Chrome(service=service, options=options)

    def run_driver(self):
        ###  init_intra_macro
        self.driver.get(self.url)
        self.wait = WebDriverWait(self.driver, 5)
        self.driver.implicitly_wait(2)

    def login(self):
        # driver.get_screenshot_as_file('intra_main_headless.png')
        self.driver.find_element(By.NAME, "username").send_keys(self.id)
        self.driver.find_element(By.NAME, "password").send_keys(self.password)
        self.driver.find_element(By.NAME, "login").click()
        print("\n - login success   >>>>")
        self.driver.get(self.projects_url)
        print("\n - project url success   >>>>")

    def quit(self):
        self.driver.quit()
        print("--- ends")

    def run(self):
        self.run_driver()
        self.login()
        self.crawl()
        self.quit()

    def new_tab(self, element_to_click, with_base=1):
        actions = ActionChains(self.driver)
        actions.key_down(Keys.COMMAND).click(element_to_click).key_up(Keys.COMMAND)

        actions.perform()

        time.sleep(1)
        if with_base:
            self.wait.until(EC.number_of_windows_to_be(2))
        else:
            self.wait.until(EC.number_of_windows_to_be(3))

        self.driver.switch_to.window(self.driver.window_handles[-1])

        self.wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "project-header"))
        )

    def close_tab(self):
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[-1])

    def get_attachment(self, with_base):
        name = self.driver.find_element(By.CLASS_NAME, "project-header").text
        if with_base:
            self.base_name = name
        attach_list = self.driver.find_elements(
            By.CLASS_NAME, "project-attachment-item"
        )
        flag_new = 0
        if attach_list is not None:
            for item in attach_list:
                link = item.find_element(By.TAG_NAME, "a")
                if link.text == "subject.pdf":
                    download_link = link.get_attribute("href")
                    project_id = download_link.split("/")[-2]
                    if name not in self.project_dict:
                        self.project_dict[name] = project_id
                        flag_new = 1
                        print("\033[92m" + "New   " + "\033[0m" + name)
                    elif self.project_dict[name] != project_id:
                        self.project_dict[name] = project_id
                        flag_new = 1
                        print("\033[93m" + "Update   " + "\033[0m" + name)
                    else:
                        print("pass  " + name)

        if flag_new:
            if with_base:
                save_path = self.save + name
            else:
                save_path = self.save + self.base_name + "/" + name
            # "-" + self.current_date
            print(save_path)
            if not os.path.exists(save_path):
                os.mkdir(save_path)
            self.driver.save_screenshot(
                save_path + "/" + self.current_date + " image.png"
            )
            for item in attach_list:
                link = item.find_element(By.TAG_NAME, "a")
                download_link = link.get_attribute("href")
                response = requests.get(download_link)
                with open(
                    save_path + "/" + self.current_date + " " + link.text, "wb"
                ) as f:
                    f.write(response.content)
            self.save_url_list(self.project_dict)

    def get_sublist(self, with_base):
        sub_item_list = self.driver.find_elements(By.CLASS_NAME, "project-list-item")
        sub_project_size = len(sub_item_list)

        # for debug
        # i = 0
        # while i < sub_project_size:
        #     print("{}: {}".format(i, sub_item_list[i].text))
        #     i += 1
        # return

        for i in range(sub_project_size):
            element_to_click = sub_item_list[i].find_element(By.TAG_NAME, "a")
            self.new_tab(element_to_click, with_base)
            self.get_attachment(with_base)
            self.close_tab()

    def crawl(self):
        print("\n - crawl start   >>>>")
        target_project_list = self.driver.find_elements(By.CLASS_NAME, "project-name")
        project_size = len(target_project_list)

        # for debug
        # i = 0
        # while i < project_size:
        #     print("{}: {}".format(i, target_project_list[i].text))
        #     i += 1
        # return

        # for debug
        # element_to_click = target_project_list[32].find_element(By.TAG_NAME, "a")
        # self.new_tab(element_to_click)
        # self.get_attachment(True)
        # self.get_sublist(False)
        # self.close_tab()
        # return

        i = 270
        while i < project_size:
            element_to_click = target_project_list[i].find_element(By.TAG_NAME, "a")
            self.new_tab(element_to_click)
            self.get_attachment(True)
            self.get_sublist(False)
            self.close_tab()
            i += 1
        return

        for i in range(project_size):
            # self.target_project_list[i].find_element(By.TAG_NAME, "a").click()
            element_to_click = target_project_list[i].find_element(By.TAG_NAME, "a")
            self.new_tab(element_to_click)
            self.get_attachment(True)
            self.get_sublist(False)
            self.close_tab()

    def dic_to_string(self, key, value):
        return key + "," + value + "\n"

    def save_url_list(self, dict):
        with open(self.save + "project_url.csv", mode="w+") as file:
            file.write("")
            for key, value in dict.items():
                file.write(self.dic_to_string(key, value))

    def load_url_dict(self):
        with open(self.save + "project_url.csv", mode="r") as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                self.project_dict[row[0]] = row[1]


class ProjectHunter(Account, Driver):
    def __init__(self):
        Account.__init__(self)
        Driver.__init__(self, self.user_id, self.user_pass, self.save_path)

    def hello(self):
        print("hello")

    def run(self):
        # super().__str__()
        # print("run")
        Driver.run(self)

    def __str__(self):
        print("ProjectHunter")


run = ProjectHunter()
run.run()

# now = datetime.now()
# current_date = now.strftime("%Y-%m-%d")
# print(current_date + " / ")

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import random
from datetime import datetime






### set target date
targetdate = ["10", "14"]

### set_init_info
# 상위 폴더에 있는 id_info.info에
# 첫줄에   ID
# 둘째줄에 PASS
f = open("../id_info.info", "r")






file_lines = f.readlines()
f.close()
user_id = file_lines[0].strip()
user_pass = file_lines[1].strip()

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
options.add_argument('headless')
options.add_argument('User-Agent: xxxxxxxxxxxxxxx')
options.add_argument("disable-infobars")
options.add_argument("--disable-extensions")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

url = 'https://intra.42.fr'
### set target || skip || pass word
target = ["rush", "봉사", "피신", "Piscine", "piscine", "PISCINE", "EXAM", "exam", "Exam", "Rush", "RUSH", "러쉬", "라피신"]
regi = "REGISTEREDRegisteredregistered"
full = "FULLFullfull"
skip = ["cursus", "Cursus", "CURSUS","test", "Test", "TEST", "테스트", "테슷트", "테슷흐", "테슽흐", "제발", "마세요", "금지", "don", "Don", "DON", "not", "tig", "TIG", "Tig", "주의", "🚨", "하지", "본과정"]

###  init_intra_macro
driver.get(url)
driver.implicitly_wait(2)

#driver.get_screenshot_as_file('intra_main_headless.png')
driver.find_element(By.NAME, 'user[login]').send_keys(user_id)
driver.find_element(By.NAME, 'user[password]').send_keys(user_pass)
driver.find_element(By.NAME, 'commit').click()
print("\n\nlogin success   >>>>")


x = 0
suc_list = []
while True:
    allevent = driver.find_elements(By.CLASS_NAME, 'event-item')
    allpop = driver.find_element(By.CLASS_NAME, 'modal-content')

    key = 0
    found = 0
    for i in allevent:
        event_subname = i.find_element(By.CLASS_NAME, 'event-subname').text
#        print("   > check event - {0} ".format(event_subname))
        date = i.find_element(By.CLASS_NAME,'date-day').text
        if date in targetdate:
#            print("   > [found collect date] - {0}".format(date))
#            print("    > [check trap event...]")
            event_name = i.find_element(By.CLASS_NAME, 'event-name').text
            for skip_word in skip:
                if skip_word in event_name or skip_word in event_subname:
#                    print("   > [pass this event] trap event - {0}".format(skip_word))
                    found_skipword = skip_word
                    key += 1
                    break
            if not key:
#                print("    >>[clear trap event]")
#                print("     > [check keyword...]")
                event_theme = i.find_element(By.CLASS_NAME, 'event-theme').text
                if not event_theme:
                    for keyword in target:
                        if keyword in event_name or keyword in event_subname:
                            found = 1
                            found_keyword = keyword
                            break
                else :
                    for keyword in target:
                        if keyword in event_name or keyword in event_subname or keyword in event_theme:
                            found = 1
                            found_keyword = keyword
                            break
                if found:
#                    print("     >>[found keyword] - {0}".format(found_keyword))
#                    print("      > [check over-flow...]")
                    over = i.find_element(By.CLASS_NAME, 'event-overflow').text
                    if not over:
                        now = time.localtime()
                        print("%04d/%02d/%02d %02d:%02d:%02d" % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec))
                        print(">  try event - {0} ".format(event_subname))
                        print("     > [new agenda!!]")
                        print("     > [try subscribe...]")
                        i.find_element(By.CLASS_NAME, 'event-main').click()
                        time.sleep(1)
                        sub = allpop.find_element(By.CLASS_NAME, 'modal-footer')
                        button_text = sub.find_element(By.TAG_NAME, 'a').get_attribute("textContent").strip()
                        if button_text == "Subscribe":
                            sub.find_element(By.TAG_NAME, 'a').click()
                            print("   >>>> success [subscribe] <<<<")
                            x += 1
                            suc_list.append("%04d/%02d/%02d %02d:%02d:%02d" % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec))
                            suc_list.append("\n")
                            suc_list.append(event_subname)
                            suc_list.append("   [subscribe]\n\n")
                        else :
                            suc_list.append("fail case\n")
                        break
                    else :
                        if over in full:
                            now = time.localtime()
                            print("\n%04d/%02d/%02d %02d:%02d:%02d" % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec))
                            print(">  try event - {0} ".format(event_subname))
                            print("     > [full agenda!!]")
                            print("     > [try waitlist...]")
                            i.find_element(By.CLASS_NAME, 'event-main').click()
                            sub = allpop.find_element(By.CLASS_NAME, 'modal-footer')
                            check_sub = sub.find_element(By.TAG_NAME, 'a').get_attribute("textContent").strip()
                            if check_sub == "Subscribe to waitlist":
                                sub.find_element(By.TAG_NAME, 'a').click()
                                print("   >>>> success [waitlist] <<<<")
                                sub_check = 1
                            else :
                                sub.find_element(By.TAG_NAME, 'button').click()
                                print("   >>>> already wait]\n")
                                sub_check = 0
                                targetdate.remove(date)
                            if sub_check == 1:
                                x += 1
                                suc_list.append("%04d/%02d/%02d %02d:%02d:%02d" % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec))
                                suc_list.append("\n")
                                suc_list.append(event_subname)
                                suc_list.append("   [waitlist]\n\n")
                            break
                        else :
                            if over in regi:
                                now = time.localtime()
                                print("\n%04d/%02d/%02d %02d:%02d:%02d" % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec))
                                print(">  try event - {0} ".format(event_subname))
                                print("     > [regi agenda!!]")
                                print("   >>>> already regi]\n")
                                x += 1
                                targetdate.remove(date)
                                break


    ### while
    if len(targetdate) == 0:
        print("<<<<>>>>   all done  <<<<>>>>")
        f = open("result.loop", 'a')
        for i in suc_list:
            f.write(i)
        f.close()
        driver.quit()

    time.sleep(random.randrange(3,5))
    driver.refresh()
    now = datetime.now()
    c_time = now.strftime("%H")

    if int(c_time) >= 21:
        print("time to sleep\n")
        driver.quit()
###


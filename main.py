#! /usr/bin/python3
# behrouz_ashraf
# garpozir@gmail.com

from selenium import webdriver
from PIL import Image, ImageChops
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.proxy import Proxy,ProxyType
import os, random, time
from config import url_pas as conf
import read_write as rw

def cls():
    if os.name == 'nt':
        _ = os.system('cls')
    else:
        _ = os.system('clear')

def read_csv():
    try:
        cm = sys.argv[1]
        with open(cm, 'r', encoding='utf-8') as file:
            code_melli = file.readlines()
            code_melli.append('mofid')
            file.close()
        if cm.split('.')[-1] != 'csv':
            sys.exit('مثال صحیح\npython main.py code_melli.csv')
        code_melli = list(dict.fromkeys(code_melli))
        return code_melli
    except Exception as e:
        print(e)
        sys.exit('مثال صحیح\npython main.py code_melli.csv')

def main() -> None:
    cls()
    code_melli = read_csv()
    print('روزهای کاری همه روزه از شنبه تا چهارشنبه. بجز روزهای تعطیل'+'\n'+'ساعات کاری 9 الی 12:30 ظهر')
    url = conf.url
    out = conf.out
    pas = conf.pas
    prox = Proxy()
    prox.proxy_type = ProxyType.MANUAL
    pr,ad,bad = (0,5,True)
    lp,bl,one = [input(' '+'مقدار شروع را وارد کنید یا برای شروع از ابتدا اینتر بزنید '),True,True]
    speed = int(input('سرعت برنامه را با عددی بین 5 تا 15 تعیین کنید'+'\n'+'هر چه عدد کوچکتر باشد برنامه سریعتر کار میکند'+' '))
    if speed < 5:
        speed = 5
    if speed > 15:
        speed = 15
    if lp == '':
        lp = '0'
    if lp.isdigit() != True:
        sys.exit('فقط میتوان یک مقدار عددی وارد کرد. صفر یا بیشتر')
    if int(lp) >= len(code_melli) - 1:
        sys.exit('مقدار شروع باید کمتر از تعداد کدهای ملی باشد')
    lp = int(lp)
    dell_invalid = rw.W_r('invalid.txt')
    dell_invalid.dell()
    dell_invalid = rw.W_r('num.txt')
    dell_invalid.dell()
    dell_invalid = rw.W_r('razavi_no.txt')
    dell_invalid.dell()
    dell_invalid = rw.W_r('red.txt')
    dell_invalid.dell()
    dell_invalid = rw.W_r('green.txt')
    dell_invalid.dell()
    dell_invalid = rw.W_r('unknow_red_green.txt')
    dell_invalid.dell()
    dell_invalid = rw.W_r('sabt_num.txt')
    dell_invalid.dell()
    lst_ap = []
    driver = webdriver.Chrome(executable_path='./chromedriver')
    driver.implicitly_wait(0.5)
    driver.maximize_window()
    while bl:
        if code_melli[lp] == 'mofid':
            break
        elif code_melli[lp][:-1].isdigit() and len(code_melli[lp]) == 11:
            melli = True
            if one:
                one = False
                driver.get(url)
            driver.find_element_by_xpath("//input[@id='Username']").send_keys(code_melli[lp])
            driver.find_element_by_xpath("//input[@id='Password']").send_keys(pas)
            driver.find_element_by_xpath("//button[@id='submit_btn']").click()
            time.sleep(0.5)

            try:
                elem = driver.find_element_by_xpath("//span[contains(text(),'ورود به سامانه ثبت نام')]")
                if elem.is_displayed():
                    with open('sabt_num.txt', 'a') as file:
                        file.write(f'{code_melli[lp]}\n')
                        file.close()
                    lp += 1
                    cls()
                    print(f'{lp} of {len(code_melli) - 1}')
                    with open('num.txt', 'w') as file:
                        file.write(str(lp))
                        file.close()
                    
            except:pass

            try:
                elem = driver.find_element_by_xpath("//img[@id='OLoginCaptcha_CaptchaImage']")
                if elem.is_displayed():
                    try:
                        ip_proxy = conf.ip_port[pr]
                    except IndexError:
                        lp += 1
                        with open('num.txt', 'w') as file:
                            file.write(str(lp))
                            file.close()
                        with open('invalid.txt', 'a') as file:
                            file.write(f'{code_melli[lp]}\n')
                            file.close()
                        driver.quit()
                        cls()
                        sys.exit('پروکسی تمام شد. 20 دقیقه دیگر ادامه دهید')
                    prox.http_proxy = ip_proxy
                    prox.ssl_proxy = ip_proxy
                    capabilities = webdriver.DesiredCapabilities.CHROME
                    prox.add_to_capabilities(capabilities)

                    driver = webdriver.Chrome(executable_path='./chromedriver',desired_capabilities=capabilities)
                    driver.implicitly_wait(0.5)
                    driver.maximize_window()
                    pr += 1
                    with open('invalid.txt', 'a') as file:
                        file.write(f'{code_melli[lp]}\n')
                        file.close()
                    melli = False
                    lp += 1
                    cls()
                    print(f'{lp} of {len(code_melli) - 1}')
                    with open('num.txt', 'w') as file:
                        file.write(str(lp))
                        file.close()
                    driver.get(out)
                    continue
            except:pass

            time.sleep(0.5)
            try:
                elem = driver.find_element_by_xpath("//a[@class='d-none d-md-block']//span[@class='d-none d-md-inline'][contains(text(),'ایزی‌تریدر')]")
                if elem.is_displayed():
                    driver.find_element_by_xpath("//a[@class='d-none d-md-block']//span[@class='d-none d-md-inline'][contains(text(),'ایزی‌تریدر')]").click()
                    driver.implicitly_wait(speed + ad)
                    if bad:
                        ad = 0
            except:pass

            try:
                button =driver.find_element_by_xpath("//i[@class='mdi mdi-20px mdi-chart-arc line-height-none ml-1 mdi-rotate-270']")
                driver.implicitly_wait(1)
                ActionChains(driver).move_to_element(button).click(button).perform()
                driver.implicitly_wait(5)
            except:
                driver.get(out)
                continue

            try:
                elem = driver.find_element_by_xpath("//div[@class='text-decoration cup']")
                if elem.is_displayed():
                    driver.find_element_by_xpath("//div[@class='text-decoration cup']").click()
                    driver.implicitly_wait(1)

                    try:
                        elemi = driver.find_element_by_xpath("//button[@title='(Enter)']")
                        time.sleep(1)
                        if elemi.is_displayed():
                            driver.implicitly_wait(1)
                            driver.find_element_by_xpath("//button[@title='(Enter)']").click()
                            cir,cir_chr = [True,0]
                            while cir:
                                el = driver.find_element_by_tag_name('body')
                                el.screenshot('after.png')
                                rw.crp('after')
                                img_f = Image.open('after.png')
                                img_f = img_f.convert('RGBA')
                                ppix = img_f.load()
                                red = 0
                                green = 0
                                yellow = 0
                                for x in range(img_f.size[1]):
                                    for y in range(img_f.size[0]):
                                        if (ppix[y, x][0]) > 185 and (ppix[y, x][1]) < 100 and (ppix[y, x][2]) < 100:
                                            red += 1
                                        if (ppix[y, x][0]) < 60 and (ppix[y, x][1]) > 110 and (ppix[y, x][2]) < 100:
                                            green += 1
                                        if (ppix[y, x][0]) > 190 and (ppix[y, x][1]) > 170 and (ppix[y, x][2]) < 80:
                                            yellow += 1
                                if red > 800 or green > 800 or yellow > 800:
                                    cir = False
                                    if red > green and red > yellow:
                                        with open('red.txt', 'a') as file:
                                            file.write(f'{code_melli[lp]}\n')
                                            file.close()
                                    elif red < green and green > yellow:
                                        with open('green.txt', 'a') as file:
                                            file.write(f'{code_melli[lp]}\n')
                                            file.close()
                                    else:
                                        lp -= 1
                                else:
                                    cir = True
                                cir_chr += 1
                                if cir_chr == 10:
                                    cir = False
                                    with open('unknow_red_green.txt', 'a') as file:
                                        file.write(f'{code_melli[lp]}\n')
                                        file.close()
                            try:
                                time.sleep(0.5)
                                driver.find_element_by_xpath("//i[@class='mdi mdi-24px mdi-power']").click()
                                driver.implicitly_wait(5)
                            except:
                                driver.get(out)
                    except:
                        driver.get(out)
                        continue

            except:
                try:
                    lst_ap.index(code_melli[lp])
                except ValueError:
                    lst_ap.append(code_melli[lp])
                    driver.get(out)
                    continue
                with open('razavi_no.txt', 'a') as file:
                    file.write(f'{code_melli[lp]}\n')
                    file.close()
                driver.find_element_by_xpath("//i[@class='mdi mdi-24px mdi-power']").click()

            if melli:
                time.sleep(random.randint(3,6))
        lp += 1
        cls()
        print(f'{lp} of {len(code_melli) - 1}')
        with open('num.txt', 'w') as file:
            file.write(str(lp))
            file.close()

    if lp == len(code_melli) - 1:
        with open('num.txt', 'w') as file:
            file.write('full')
            file.close()
    driver.quit()
    dell_invalid = rw.W_r('after.jpg')
    dell_invalid.dell()
    dell_invalid = rw.W_r('after.png')
    dell_invalid.dell()
    dell_invalid = rw.W_r('before.jpg')
    dell_invalid.dell()
    dell_invalid = rw.W_r('before.png')
    dell_invalid.dell()
    sys.exit('کار تمام است. برای خروج اینتر بزنید')

if __name__ == '__main__':
    import sys
    main()

import json, socket, requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def get_middle_text(text, prefix, suffix, index=0):
    """
    Simple implementation of obtaining intermediate text

    :param text:Full text to get
    :param prefix:To get the first part of the text
    :param suffix: To get the second half of the text
    :param index: Where to get it from
    :return:
    """
    try:
        index_1 = text.index(prefix, index)
        index_2 = text.index(suffix, index_1 + len(prefix))
    except ValueError:
        return ''
    return text[index_1 + len(prefix):index_2]


def get_ip_area(ip):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0"
    }
    url = "https://www.ip138.com/iplookup.asp?ip=%s&action=2" % (ip)
    resp = requests.get(url, headers=headers)
    resp.encoding = "gb2312"
    return get_middle_text(resp.text, "result = ", ";")


if __name__ == '__main__':
    with open("config.json", "r", encoding="utf8") as f:
        config = json.load(f)
    with open("template.json", "r", encoding="utf8") as f:
        tpl = json.load(f)

    variables = tpl.get("variables")
    if "site_ip" not in variables.keys():
        # 如果没有ip则从url中获取域名解析
        domain = variables.get("url").split('/')[2].split(':')[0]
        variables["site_ip"] = socket.gethostbyname(domain)
    print(variables["site_ip"])
    print(get_ip_area(variables["site_ip"]))

    fields = tpl.get("fields")
    print(fields)


    def render(tpl_text: str) -> str:
        for key, value in variables.items():
            tpl_text = tpl_text.replace("{{ " + key + " }}", value)
        return tpl_text


    cookies = [{'domain': 'src.360.net', 'name': name, 'value': value} for name, value in
               config.get("cookies").items()]
    browser = webdriver.Chrome(executable_path=r"D:\Program Files\Google\Chrome\Application\chromedriver.exe")
    browser.get("https://src.360.net/help")
    try:
        WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div/div[1]/div/div[1]/div[1]/div[1]/img'))
        )
    except Exception as e:
        browser.quit()
        exit(1)

    browser.delete_all_cookies()
    for cookie in cookies:
        browser.add_cookie(cookie)

    browser.get("https://src.360.net/submit-bug")
    # browser.quit()
    try:
        # 同意协议打勾
        xpath = '//*[@id="app"]/div/div[1]/div/div[2]/div/div[1]/div[1]/section/form/div[16]/div/div/label/span[1]/span'
        WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, xpath))).click()

        # 通用漏洞选中
        xpath = '//*[@id="app"]/div/div[1]/div/div[2]/div/div[1]/div[1]/section/form/div[6]/div[1]/div/div/label[2]'
        browser.execute_script("arguments[0].click();", browser.find_element_by_xpath(xpath))

        # 填充配置字段
        xpath_list = config.get("xpath")
        fields = tpl.get("fields")
        for key, value in fields.items():
            browser.find_element_by_xpath(xpath_list.get(key)).send_keys(render(value))

    except Exception as e:
        print(e)
        browser.quit()
        exit(1)

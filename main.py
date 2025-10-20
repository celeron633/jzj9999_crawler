import time
import json
from typing import List

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class GoldPriceItem(object):
    def __init__(self):
        self.good_name = ""
        self.good_buy_price = ""
        self.good_sell_price = ""
        self.high_price = ""
        self.low_price = ""

    def __str__(self):
        return str(self.good_name+":"+self.good_buy_price+","+self.good_sell_price+","+self.high_price+","+self.low_price)

class GoldPrices(object):
    def __init__(self):
        self.container: List[GoldPriceItem] = []

    def clear(self):
        self.container.clear()

    def append(self, price_item: GoldPriceItem):
        self.container.append(price_item)

    def to_json(self) -> str:
        my_dict = {"timestamp": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), "data": self.container, "count": len(self.container)}
        return json.dumps(my_dict, default=lambda o: o.__dict__, sort_keys=True, indent=4)

Gold = GoldPrices()

options = Options()
# options.add_argument("--headless")  # 无界面运行（可去掉看浏览器）
# options.add_argument("--disable-gpu")

service = Service(executable_path="D:\chromedriver-win64\chromedriver.exe")
driver = webdriver.Chrome(service=service, options=options)

try:
    driver.get("https://i.jzj9999.com/quoteh5/?ivk_sa=1025883i")

    # 等待某个元素加载完毕
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/div/div/div/div/div[5]/div/div[2]/div/div[1]/div/div"))
    )

    while True:
        Gold.clear()
        for i in range(1, 22):
            target_xpath: str = "/html/body/div/div/div/div/div[5]/div/div[2]/div/div[{index}]/div/div".format(index=i)
            str_data = driver.find_element(By.XPATH, target_xpath).text.replace("\n", " ")
            item = GoldPriceItem()
            item.good_name = str_data.split(" ")[0]
            item.good_buy_price = str_data.split(" ")[1]
            item.good_sell_price = str_data.split(" ")[2]
            item.high_price = str_data.split(" ")[3]
            item.low_price = str_data.split(" ")[4]
            Gold.append(item)
            # print(item)
        # print(price_list)
        print(Gold.to_json())
        time.sleep(0.3)

except KeyboardInterrupt:
    driver.quit()
    print("quit!")

finally:
    driver.quit()
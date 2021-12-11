from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pandas as pd
from functools import partial, reduce
import time

driver = webdriver.Firefox()
page = driver.get("https://dashboard.kerala.gov.in/covid/index.php")
daily = driver.find_element_by_xpath("/html/body/div/aside/div/nav/ul/li[2]/a/p/i")
daily.click()
diswise = driver.find_element_by_xpath("/html/body/div/aside/div/nav/ul/li[2]/ul/li[2]/a")
diswise.click()
dist_xpath = "/html/body/div[1]/div[1]/section[2]/div/section/div/div[1]/div[1]/div/div/div/div/form/div/div[1]"
wait = WebDriverWait(driver, 10)
element = wait.until(EC.element_to_be_clickable((By.XPATH, dist_xpath)))
dist_list = driver.find_element_by_xpath(dist_xpath).click()
driver.implicitly_wait(5)

dist_dict = {0: 'Kerala', 1: 'KSD', 2: 'KNR', 3: 'WYD', 4: 'KKD', 5: 'MLP', 6: 'PKD', 7: 'TSR', 8: 'EKM', 9: 'IDK', 10: 'KTM', 11: 'ALP', 12: 'PTA',
                13: 'KLM', 14: 'TVM'}
"""
for option in dist_list.find_elements_by_tag_name('option'):
    options.append(option.text)

"""
dfs = []

for key, value in dist_dict.items():
    dist_name = driver.find_element_by_xpath(f"/html/body/div[1]/div[1]/section[2]/div/section/div/div[1]/div[1]/div/div/div/div/form/div/div[1]/select/option[{key + 1}]")
    dist_name.click()
    view = driver.find_element_by_name("hw")
    view.click()
    time.sleep(15)
    dist_data = driver.find_element_by_xpath("/html/body/div[1]/div[1]/section[2]/div/section/div/div[2]/section[6]/div/div[2]/div/div/div[2]/button[1]")
    dist_data.click()
    df = pd.read_clipboard(sep = "\t", header = 1)
    s_df = df[["Date","Confirmed"]].copy()
    s_df.rename(columns = {'Confirmed': value}, inplace = True)
    dfs.append(s_df)
    time.sleep(5)

driver.quit()
merge = partial(pd.merge, on=['Date'], how='outer')
result_df = reduce(merge, dfs)
final_df = result_df[['Date','Kerala', 'TVM', 'KLM', 'PTA','ALP','KTM','IDK','EKM','TSR','PKD','MLP','KKD', 'WYD','KNR','KSD']]
final_df.fillna(0,inplace=True)
out = final_df.set_index("Date").astype(int)
out.to_excel("covid_data_up.xlsx") 

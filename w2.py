from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd
df = pd.read_excel('login2.xlsx')

# Initialize an empty DataFrame
output_df = pd.DataFrame()

for i in range(0,1):
    uid = str(df.iloc[i,1])
    pas = str(df.iloc[i,2])

    driver = webdriver.Chrome()

    def login(url, usernameid, passwordid, submitid, username, password):
        driver.get(url)
        el = driver.find_element(By.NAME, usernameid)
        el.send_keys(username)
        el1 = driver.find_element(By.NAME, passwordid)
        el1.send_keys(password)
        el2 = driver.find_element(By.CLASS_NAME, submitid)
        el2.click()

    login("https://www.rajagiritech.ac.in/stud/ktu/student/", "Userid", "Password", "ibox1", uid, pas)
    
    el3 = driver.find_element(By.LINK_TEXT,"End Semester Marks")
    el3.click()
    el4 = driver.find_element(By.XPATH, '//input[@type="submit" and @value="SUBMIT" and contains(@class, "ibox1")]')
    el4.click()

    #time.sleep(5)

    table = driver.find_element(By.ID, "extable")
    rows = table.find_elements(By.TAG_NAME, "tr")

    temp_data = []
    t1_data = ['samp']
    
    for row in rows[1:]:
        cells = row.find_elements(By.TAG_NAME, "td")
        samp = [cells[1].text]
        if(len(cells)>=9):
            row_data = [cells[7].text]
        else:
            row_data = [cells[0].text]
        t1_data.append(samp)
        temp_data.append(row_data)


    temp_df = pd.DataFrame([temp_data])

    temp_df.insert(0, 'Student_ID', df.iloc[i, 0])

# Concatenate temp_df with output_df
    output_df = pd.concat([output_df, temp_df], ignore_index=True)
    driver.close()

column_names = [col[0] for col in t1_data]

# Iterate over column_names to rename columns in output_df
for k, new_column_name in enumerate(column_names):
    # Skip renaming the first column as it's already renamed as 'Student_ID'
    if k == 0:
        continue
    output_df.rename(columns={output_df.columns[k]: new_column_name}, inplace=True)


output_df = output_df.map(lambda x: str(x).strip("['']"))
output_df.to_excel('output.xlsx', index=False)


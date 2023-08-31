from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import random, string, time
from selenium.webdriver.support.wait import WebDriverWait

# Locating the path of Chromedriver.
service = Service(executable_path='chromedriver.exe')

options = webdriver.ChromeOptions()

# Locating the Chrome.exe 
options.binary_location = "C:\Program Files\Google\Chrome Dev\Application\chrome.exe"

driver = webdriver.Chrome(service=service, options=options)
driver.implicitly_wait(66)

driver.get('https://commerceos.staging.devpayever.com/registration/fashion')

# Locating all the tags associated with the input fields
input_fields = driver.find_elements(By.TAG_NAME, 'peb-form-field-input')

# Creating a random gmail and name generator to avoid Unique Constraint error 
gmail = ''
while len(gmail) < 18:
    gmail = gmail + random.choices(string.ascii_lowercase)[0]

# Defining inputs
input_list = ['yazdan', 'akhoondi', f'{gmail}@gmail.com', '!@#$1234QWERqwer', '!@#$1234QWERqwer']
zero = 0

for field in input_fields:

    # Clicking on the elemnet to make the input field be able to receive data
    span = field.find_element(By.TAG_NAME, 'span').click()
    time.sleep(0.5)

    # Locating input the input field
    input_field = field.find_element(By.TAG_NAME, 'input')
    time.sleep(0.2)

    # inserting data
    input_field.send_keys(input_list[zero])
    time.sleep(0.2)

    zero += 1

# Locating and clicking on sign up button
signup_button = driver.find_element(By.CLASS_NAME, 'signup-button').click()

# Loacting the business page form div for ease of locating other elements
div = driver.find_element(By.CLASS_NAME, 'form-background-wrapper')
print('Form div is located.')

peb_select_found = False

# I prefere to use this instead of explicit wait
while peb_select_found is False:
    time.sleep(0.3)
    try:
        # Locating the form div again in the case if it wrongly located the previous page form div
        div = driver.find_element(By.CLASS_NAME, 'form-background-wrapper')

        # Trying to locate Fields which input tags are in them. 
        peb_selects = div.find_elements(By.TAG_NAME, 'peb-select')
        peb_select_found = True

    except:
        peb_select_found = False
        print('Fields are not located. Trying again..')

n = 1
LINE_CLEAR = '\x1b[2K' # <-- ANSI sequence

for peb in peb_selects:

    # Clicking on the choice field so the div of choice gets visible and therefore, locatable
    peb.click()
    time.sleep(1)
    print(f'{n} peb...', end='/r')
    print(end=LINE_CLEAR)

    # Locating all the options of the currently open choice field
    peb_options = driver.find_elements(By.TAG_NAME, 'peb-select-option')
    time.sleep(0.5)

    # Trying to click the last one, if unable, the first one
    try:
        peb_options[-1].click()
    except:
        peb_options[0].click()
    n += 1

# Locating fileds that are not choice field
field_inputs = driver.find_elements(By.TAG_NAME, 'peb-form-field-input')


field_inputs[0].click()
time.sleep(0.2)
field_inputs[0].find_element(By.TAG_NAME, 'input').send_keys(gmail)
time.sleep(0.2)

field_inputs[2].click()
time.sleep(0.2)
field_inputs[2].find_element(By.TAG_NAME, 'input').send_keys('333666999')
time.sleep(0.2)

# Trying to click on proceed button, if it is not loaded, trying to click on signup button
while True:
    time.sleep(0.3)
    try:
        print('trying to click on welcome button')
        proceed_button = driver.find_element(By.CLASS_NAME, 'welcome-screen-content-button').click()
        break
    except:
        signup_button = driver.find_element(By.CLASS_NAME, 'signup-button').click()
        print('proceed button not located. trying to click on prevous signup button')

# 2. After step 7, validate the following apps to be present on the dashboard:
# - Transactions, Checkout, Connect, Products, Shop, Message, settings

apps = 'Transactions, Checkout, Connect, Products, Shop, Message, settings'.lower().split(', ')
time.sleep(3)

# Making a list of all available apps
icon_titles = driver.find_elements(By.CLASS_NAME, "icons__title")

# Cheking to see if the desired apps are available
for i in icon_titles:
    if i.text.lower() in apps:
        print(f'app {i.text} is present on the dashboard') 

print('Automation finished')

# Ending session, closing browser. 
driver.quit()
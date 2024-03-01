
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

# создание драйвера с автоматическим поиском браузера и вебдрайвера
# driver = webdriver.Chrome()

# создание драйвера с автоматическим поиском браузера и указанием путя к вебдрайверу
# service = Service(executable_path='/chromedriver')
# options = webdriver.ChromeOptions()
# driver = webdriver.Chrome(service=service, options=options)

# создание драйвера
chromedriver = "chromedriver/chromedriver"
option = webdriver.ChromeOptions()
option.binary_location = 'указать путь до браузера Chrome или Chromium-based (Yandex browser etc)'
s = Service(chromedriver)
driver = webdriver.Chrome(service=s, options=option)

driver.get("https://oauth.vk.com/authorize?client_id=51792477&response_type=token")

# Для удобства сохраняем XPath формы авторизации
username = '//*[@id="login_submit"]/div/div/input[6]'
password = '//*[@id="login_submit"]/div/div/input[7]'
login = '//*[@id="install_allow"]'

# Заполняем форму авторизации
#driver.find_element_by_xpath(username).send_keys('your_login') # необязательно, если сессия VK активна
#driver.find_element_by_xpath(password).send_keys('your_password!@#$') # необязательно, если сессия VK активна
driver.find_element_by_xpath(login).click()

print(driver.current_url)
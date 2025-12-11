from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import os
import time

# Thông tin
url = "https://dangkyquamang.dkkd.gov.vn/inf/Forms/Searches/EnterpriseInfo.aspx"
ma_so_thue = "0110488703"

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
output_pdf = os.path.expanduser(f"~/Documents/DKKD_{timestamp}.pdf")

# Tuỳ chọn Chrome
options = Options()
options.add_argument("--kiosk-printing")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--no-sandbox")
options.add_argument("--disable-gpu")
# options.add_argument("--headless=new")  # Chạy headless nếu cần

prefs = {
    "printing.print_preview_sticky_settings.appState":
        '{"recentDestinations":[{"id":"Save as PDF","origin":"local","account":""}],'
        '"selectedDestinationId":"Save as PDF","version":2}',
    "savefile.default_directory": os.path.dirname(output_pdf)
}
options.add_experimental_option("prefs", prefs)

chrome_driver_path = r"C:\Users\phucn\Downloads\chromedriver-win32\chromedriver-win32\chromedriver.exe"

# Khởi tạo Chrome
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service, options=options)
driver.set_page_load_timeout(100)

try:
    driver.get(url)

    wait = WebDriverWait(driver, 10)
    search_input = wait.until(EC.element_to_be_clickable((By.ID, "ctl00_FldSearch")))
    search_input.send_keys(ma_so_thue)

    suggestion = WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.XPATH, f"//div[contains(@class, 'ui-menu-item-wrapper') and contains(., '{ma_so_thue}')]"))
)
    # Di chuyển chuột tới và click bằng ActionChains
    actions = ActionChains(driver)
    actions.move_to_element(suggestion).click().perform()

    # Click chọn dòng gợi ý
    suggestion.click()

    time.sleep(10)  # Chờ kết quả hiện ra nếu có

    driver.execute_script('window.print();')
    print(f"Đã in ra PDF. Kiểm tra tại: {output_pdf}")
finally:
    time.sleep(10)
    driver.quit()

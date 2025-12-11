import subprocess
import requests
import json
import time
from openpyxl import load_workbook

class MyChromeDriver:
    def __init__(self, chromedriver_path="chromedriver.exe", port=9515):
        self.port = port
        self.url = f"http://localhost:{port}"
        self.headers = {"Content-Type": "application/json"}

        # 👉 Khởi động ChromeDriver
        self.process = subprocess.Popen([chromedriver_path, f"--port={port}"])
        time.sleep(1.5)  # Đợi khởi động xong

        # 👉 Gửi yêu cầu tạo phiên làm việc (session)
        body = {
            "capabilities": {
                "alwaysMatch": {
                    "browserName": "chrome",
                    "goog:chromeOptions": {
                        "args": [
                            "--start-maximized",
                            "--disable-blink-features=AutomationControlled"
                        ],
                        "excludeSwitches": ["enable-automation"]
                    }
                }
            }
        }

        # Gửi POST tạo session
        res = requests.post(f"{self.url}/session", headers=self.headers, json=body)
        self.session_id = res.json()["value"]["sessionId"]
        self.session_url = f"{self.url}/session/{self.session_id}"

    def get(self, target_url):
        """Mở trang web"""
        requests.post(f"{self.session_url}/url", headers=self.headers, json={"url": target_url})

    def find_element(self, using, value):
        """Tìm phần tử (element) bằng strategy và value"""
        res = requests.post(
            f"{self.session_url}/element",
            headers=self.headers,
            json={"using": using, "value": value}
        )

        # In để debug (nếu cần)
        # print(json.dumps(res.json(), indent=2))

        data = res.json().get("value", {})
        return data.get("element-6066-11e4-a52e-4f735466cecf") or data.get("ELEMENT")

    def wait_until_element(self, using, value, timeout=10, poll_interval=0.5):
        """Chờ cho đến khi phần tử xuất hiện (tối đa `timeout` giây)"""
        end_time = time.time() + timeout
        while time.time() < end_time:
            try:
                element_id = self.find_element(using, value)
                if element_id:
                    return element_id
            except Exception:
                pass
            time.sleep(poll_interval)
        raise Exception(f"Timeout: Không tìm thấy phần tử '{value}' bằng '{using}'")

    def send_keys(self, element_id, text):
        """Gửi chuỗi ký tự vào phần tử"""
        body = {"text": text, "value": list(text)}
        requests.post(
            f"{self.session_url}/element/{element_id}/value",
            headers=self.headers,
            json=body
        )
        
    def click_element(self, element_id):
        """Click vào phần tử"""
        requests.post(
            f"{self.session_url}/element/{element_id}/click",
            headers=self.headers,
            json={}
        )
        
    def get_element_text(self, element_id):
        """Lấy text từ phần tử"""
        res = requests.get(
            f"{self.session_url}/element/{element_id}/text",
            headers=self.headers
        )
        return res.json().get("value", "")

    def quit(self):
        """Kết thúc session và đóng Chrome"""
        requests.delete(f"{self.session_url}")
        self.process.terminate()

    def read_excel_column(file_path, sheet_name="Sheet1", column="A"):
        wb = load_workbook(file_path)
        sheet = wb[sheet_name]
        data = []
        for cell in sheet[column]:
            if cell.value:  # bỏ ô trống
                data.append(str(cell.value).strip())
        return data


# === Sử dụng ===
if __name__ == "__main__":
    driver = MyChromeDriver("C:/Users/phucn/Downloads/chromedriver-win32-ver/chromedriver-win32/chromedriver.exe")
    driver.get("https://dangkyquamang.dkkd.gov.vn/auth/Public/LogOn.aspx?ReturnUrl=%2fonline%2fDefault.aspx")

     # Chờ ô tìm kiếm
    search_box = driver.wait_until_element("css selector", "#ctl00_FldSearch")
    
    
    # Gửi từ khóa và Enter//////////
    driver.send_keys(search_box, "0101245486\n")
    time.sleep(2)  # chờ kết quả hiện ra

    # Bước 2: nhập số MST + Enter
    driver.send_keys(search_box, "0101245486\n")

    time.sleep(2)  # Chờ load kết quả

    # Bước 3: tìm dòng kết quả đầu tiên (tên doanh nghiệp)
    first_result = driver.wait_until_element(
        "css selector",
        "#ctl00_ContentPlaceHolder1_grResult tr:nth-child(2) td:nth-child(1) a"
    )

    # Bước 4: in ra kết quả
    print("Tên doanh nghiệp đầu tiên:", driver.get_element_text(first_result))

    # (tuỳ chọn) Click vào chi tiết
    driver.click_element(first_result)


    time.sleep(5)
    driver.quit()

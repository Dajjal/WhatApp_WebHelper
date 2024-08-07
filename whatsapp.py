from time import sleep
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait


class WhatsApp:
    is_authorized = False

    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument('user-data-dir=user_data')
        self.driver = webdriver.Chrome(options=options)
        self.driver.get('https://web.whatsapp.com/')

    def check_auth(self):
        try:
            if self.driver.find_element(
                By.XPATH,'/html/body/div[2]/div/div/div[2]/div[3]/div[1]/div/div/div[2]/div/canvas'
            ).get_attribute('aria-label') == 'scan_me':
                self.is_authorized = False
                return False
        except Exception as e:
            self.is_authorized = True
            return True

    def element_presence(self, by, xpath, time):
        element_present = ec.presence_of_element_located((by, xpath))
        WebDriverWait(self.driver, time).until(element_present)

    def send_message_to_number(self, phone_no, text):
        if not self.check_auth():
            print('Please authorize the app')
            return
        self.driver.get('https://web.whatsapp.com/send?phone={}&source=&data=#'.format(phone_no))
        try:
            self.send_message(text)
        except Exception as e:
            print('invalid phone no :' + str(phone_no))

    def send_message(self, text):
        if not self.check_auth():
            print('Please authorize the app')
            return
        text_input = '/html/body/div[1]/div/div/div[2]/div[4]/div/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[1]/p'
        self.element_presence(by=By.XPATH, xpath=text_input, time=30)
        txt_box = self.driver.find_element(By.XPATH, text_input)
        txt_box.send_keys(text)
        txt_box.send_keys('\n')
        sleep(1)

    def check_for_new_messages(self):
        if not self.check_auth():
            print('Please authorize the app')
            return
        if self.driver.current_url != 'https://web.whatsapp.com/':
            self.driver.get('https://web.whatsapp.com/')
        else:
            try:
                all_chats = '/html/body/div[1]/div/div/div[2]/div[3]/div/div[3]/div[1]/div/div/div'
                self.element_presence(by=By.XPATH, xpath=all_chats, time=30)
                chats = self.driver.find_elements(By.XPATH, all_chats)
                for chat in chats:
                    user_name_or_phone = chat.find_element(By.XPATH, 'div/div/div/div[2]/div[1]/div[1]').text
                    try:
                        unread_messages_text = (chat.find_element(
                            By.XPATH,
                            'div/div/div/div[2]/div[2]/div[2]/span[1]/div/span'
                        ).get_attribute('aria-label'))
                        print(user_name_or_phone, ' - ', unread_messages_text)
                        chat.click()
                        last_message = self.driver.find_elements(
                            By.XPATH,
                            '/html/body/div[1]/div/div/div[2]/div[4]/div/div[3]/div/div[2]/div[3]/div'
                        )[-1].find_element(
                            By.XPATH, 'div/div/div[1]/div[1]/div[1]/div/div[1]/div/span/span'
                        ).text
                        self.send_message(last_message)
                        self.close_chat()
                    except Exception as e:
                        pass
            except Exception as e:
                print(e)

    def close_chat(self):
        if not self.check_auth():
            print('Please authorize the app')
            return
        self.driver.find_element(
            By.XPATH, '/html/body/div[1]/div/div/div[2]/div[4]/div/header/div[3]/div/div[3]/div/div'
        ).click()
        self.driver.find_element(
            By.XPATH, '/html/body/div[1]/div/div/span[5]/div/ul/div/div/li[3]/div'
        ).click()

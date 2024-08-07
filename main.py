from utils import Utils
from whatsapp import WhatsApp

mobile_numbers_list = [77781234567]

if __name__ == '__main__':
    whatsapp = WhatsApp()
    Utils.set_interval(func=whatsapp.check_for_new_messages, sec=1)

    # for mobile_number in mobile_numbers_list:
    #     whatsapp.send_whatsapp_msg(mobile_number, 'Тестовое сообщение')

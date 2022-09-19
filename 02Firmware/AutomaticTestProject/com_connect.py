# # Init_STM32_COM()
# # 配置STM32控制板串口
# # st = serial.Serial('com3', 115200)
import serial

#
STM32_uart_com = 'com6'  # STM32上位机，用于修改芯片寄存器
# E3632A_COM = 'com4'  # E3632A

STM32_com = serial.Serial(STM32_uart_com, 115200)
# PWR_Supply_E3632A_COM_cfg = serial.Serial(E3632A_COM, 9600)


def ComConfig():
    if STM32_com.isOpen():
        print(STM32_uart_com, "STM32 open success")
    else:
        print(STM32_uart_com, "STM32 open failed")

    # if PWR_Supply_E3632A_COM_cfg.isOpen():
    #     print(E3632A_COM, "open success")
    # else:
    #     print(E3632A_COM, "open failed")

    # if PWR_Supply_E36311A_COM_cfg.isOpen():
    #     print(E36311A_COM, "open success")
    # else:
    #     print(E36311A_COM, "open failed")

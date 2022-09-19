import math
import time

from com_connect import STM32_com
from Data_handle import receive_data_manual, receive_reg_data_handle
from mylog import print_2bytes_hex

CMD_Pre = ([0x50])  # 包头
# CMD_len = ([0x00, 0x00])  # 命令包总长度
CMD_version = ([0x00])  # 软件版本信息

# CMD_Read = ([0x02, 0x00, 0x3c, 0x00, 0x02])  # 单寄存器读命令
# CMD_Write = ([0x02, 0x01, 0x3c, 0x00, 0x03])  # 单寄存器写命令

CMD_batch_Write = ([0x02, 0x02, 0x3c])  # 多寄存器批量读命令
CMD_batch_Read = ([0x02, 0x03, 0x3c])  # 多寄存器批量写命令


# CMD_reg_len = ([0x00, 0x00])  # 待操作的寄存器和数据的长度
# Reg_w_configer = ([])  # 多寄存器批量写 寄存器地址与写入值
# Reg_r_configer = ([])  # 多寄存器批量度 寄存器地址
# # CMD_crc = ([0x00]) # crc校验值，为数据包除了crc以外的异或值
# CMD_crc = 0x00 # crc校验值，为数据包除了crc以外的异或值

# def comPackData(wr_mode, reg_batch_write, reg_batch_read):  # wr_mode为读写模式，addr_h,addr_l为地址高位和低位，value为写入的寄存器值
# Reg_w_configer = reg_batch_write
#     Reg_r_configer = reg_batch_read
#     CMD_crc = 0x00
#     if wr_mode == 0x02:  # batch write
#         # CMD_reg_len = [len(Reg_configer) / 256, len(Reg_configer) % 256]
#         CMD_reg_len = [math.trunc(len(Reg_w_configer) / 256), len(Reg_w_configer) % 256]  # 操作的寄存器长度
#         # print(CMD_reg_len)
#         # print_2bytes_hex(CMD_reg_len)
#         # CMD_len = ([0x00, 0x09])
#
#         CMD_payload = (CMD_batch_Write + CMD_reg_len + Reg_w_configer)
#         # print(CMD_payload)
#         CMD_data_len = [math.trunc((len(CMD_payload)+1) / 256), (len(CMD_payload)+1) % 256]
#         # print('CMD_len:', CMD_data_len)
#
#         CMD_data = (CMD_Pre + CMD_data_len + CMD_version + CMD_payload)
#         # print('CMD_dat:', CMD_data)
#         # print_2bytes_hex(CMD_data)
#
#         for index in range(len(CMD_data)):
#             CMD_crc ^= CMD_data[index]
#         # print(hex(CMD_crc))
#         Send_data_pack = (CMD_data + [CMD_crc])
#         # print(Send_data_pack)
#         # print(len(Send_data_pack))

#     return Send_data_pack


# 发送寄存器写入命令
def CMD_batch_write(reg_batch_write):  # batch write
    Reg_w_configer = reg_batch_write
    CMD_crc = 0x00
    CMD_reg_len = [math.trunc(len(Reg_w_configer) / 256), len(Reg_w_configer) % 256]  # 操作的寄存器长度
    CMD_payload = (CMD_batch_Write + CMD_reg_len + Reg_w_configer)
    CMD_data_len = [math.trunc((len(CMD_payload) + 1) / 256), (len(CMD_payload) + 1) % 256]
    CMD_data = (CMD_Pre + CMD_data_len + CMD_version + CMD_payload)

    for index in range(len(CMD_data)):
        CMD_crc ^= CMD_data[index]
    Send_w_data_pack = (CMD_data + [CMD_crc])

    print('Write_cmd : ')
    print_2bytes_hex(Send_w_data_pack)
    STM32_com.write(Send_w_data_pack)  # 串口发送成功

    return Send_w_data_pack


# 发送寄存器读取命令
def CMD_batch_read(reg_batch_read):  # batch read
    Reg_r_configer = reg_batch_read
    CMD_crc = 0x00
    CMD_reg_len = [math.trunc(len(Reg_r_configer) / 256), len(Reg_r_configer) % 256]  # 操作的寄存器长度
    CMD_payload = (CMD_batch_Read + CMD_reg_len + Reg_r_configer)
    CMD_data_len = [math.trunc((len(CMD_payload) + 1) / 256), (len(CMD_payload) + 1) % 256]
    CMD_data = (CMD_Pre + CMD_data_len + CMD_version + CMD_payload)

    for index in range(len(CMD_data)):
        CMD_crc ^= CMD_data[index]
    Send_r_data_pack = (CMD_data + [CMD_crc])

    print('Read_cmd : ')
    print_2bytes_hex(Send_r_data_pack)
    STM32_com.write(Send_r_data_pack)  # 串口发送成功

    return Send_r_data_pack


# 发送寄存器批写入命令并接受回复
def CMD_batch_w_Query(reg_batch_write):  # batch write and receive ack immediately
    Reg_w_configer = reg_batch_write
    CMD_crc = 0x00
    CMD_reg_len = [math.trunc(len(Reg_w_configer) / 256), len(Reg_w_configer) % 256]  # 操作的寄存器长度
    CMD_payload = (CMD_batch_Write + CMD_reg_len + Reg_w_configer)
    CMD_data_len = [math.trunc((len(CMD_payload) + 1) / 256), (len(CMD_payload) + 1) % 256]
    CMD_data = (CMD_Pre + CMD_data_len + CMD_version + CMD_payload)

    for index in range(len(CMD_data)):
        CMD_crc ^= CMD_data[index]
    Send_w_data_pack = (CMD_data + [CMD_crc])

    print('Write_cmd : ')
    print_2bytes_hex(Send_w_data_pack)
    STM32_com.write(Send_w_data_pack)  # 串口发送成功

    time.sleep(0.1)
    receive_data_manual()

    return Send_w_data_pack


# 发送寄存器批读取命令并接受回复
def CMD_batch_r_Query(reg_batch_read):  # batch read
    Reg_r_configer = reg_batch_read
    CMD_crc = 0x00
    CMD_reg_len = [math.trunc(len(Reg_r_configer) / 256), len(Reg_r_configer) % 256]  # 操作的寄存器长度
    CMD_payload = (CMD_batch_Read + CMD_reg_len + Reg_r_configer)
    CMD_data_len = [math.trunc((len(CMD_payload) + 1) / 256), (len(CMD_payload) + 1) % 256]
    CMD_data = (CMD_Pre + CMD_data_len + CMD_version + CMD_payload)

    for index in range(len(CMD_data)):
        CMD_crc ^= CMD_data[index]
    Send_r_data_pack = (CMD_data + [CMD_crc])

    # print('Read_cmd : ')
    # print_2bytes_hex(Send_r_data_pack)
    STM32_com.write(Send_r_data_pack)  # 串口发送成功

    time.sleep(0.1)
    read_reg_addr_data = receive_reg_data_handle()
    # print('read_reg_data:', read_reg_addr_data)
    return read_reg_addr_data

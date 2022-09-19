"""
# main.py
# ~~~~~~~~~~
#
# 自动配置芯片，并读取PN
"""
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
import math

# from chip_reg import REG_W
import chip_reg
from excel_handle import xlsx_Handle, xlsx_init, GPADC_xlsx_Handle
from folder import mkdir, TEST_DATA_FOLDER, TEST_LOG_FOLDER
import time
import kwargs as kwargs
import pyvisa

import datetime
import sys
# import numpy
# import visa
import pandas as pd
import pymysql

import mylog
import threading

from numpy import char
from sqlalchemy.engine import cursor
from sqlalchemy.testing import db

import encode
# from Data_handle import receive_data
from Data_handle import receive_data_manual
from encode import CMD_batch_write
from encode import CMD_batch_read
from encode import CMD_batch_w_Query
from encode import CMD_batch_r_Query
import Keysight_Instrument
from Keysight_Instrument import KsInstr_PN_Test, KsInstr_Freq_Test, KsInstr_Power_Test, PXA_N9030B, KsInstr_IF_Test
from Keysight_Instrument import PS_E3632A_on, PS_E3632A_off
from Keysight_Instrument import PS_E36311A, PS_E36311A_init_cfg, PS_E36311A_on, PS_E36311A_off, \
    PS_E36311A_read_volt_curr
from gpadc_test_process import gpadc_dc_test
from mylog import print_2bytes_hex
from com_connect import STM32_com, STM32_uart_com, ComConfig
# from com_connect import E3632A_COM, PWR_Supply_E3632A_COM_cfg
import serial.tools.list_ports

# from test_process import fn_pn_test

# def Init_PXA_N9030B():
# def Init_STM32_COM():

"""
# port_init 
"""

TEST_MODE_REG_INIT = ([0x10, 0x40, 0x00,  # CP1_CTRL0
                       0x10, 0x41, 0x00,  # CP1_CTRL1
                       0x10, 0x42, 0x86,  # CP1_CTRL2
                       0x10, 0x43, 0x00,  # CP1_CTRL3
                       0x10, 0x44, 0x00,  # CP1_CTRL4
                       0x12, 0xF0, 0xA8,  # CSAMODE0
                       0x12, 0xF3, 0x20,  # FLAG
                       0x12, 0xF5, 0x04,  # FLAG
                       0x13, 0x47, 0x67,  # FMCW
                       0x13, 0x48, 0x67,  # FMCW
                       0x13, 0x49, 0x07,  # FMCW
                       0x13, 0x4A, 0x07,  # FMCW
                       0x13, 0x82, 0x09,  # LODIST
                       0x13, 0xB2, 0x00  # CAL
                       ])

CONFIG_REG_INIT_RF76P8G_F19P2G = ([0x10, 0x40, 0x00,  # CP1_CTRL0
                                   0x10, 0x41, 0x00,  # CP1_CTRL1
                                   0x10, 0x42, 0x80,  # CP1_CTRL2
                                   0x10, 0x43, 0x00,  # CP1_CTRL3
                                   0x10, 0x44, 0x00,  # CP1_CTRL4
                                   0x12, 0xF0, 0xA8,  # CSAMODE0
                                   0x12, 0xF3, 0x20,  # FLAG
                                   0x12, 0xF5, 0x04,  # FLAG
                                   0x13, 0x47, 0x67,  # FMCW
                                   0x13, 0x48, 0x67,  # FMCW
                                   0x13, 0x49, 0x07,  # FMCW
                                   0x13, 0x4A, 0x07,  # FMCW
                                   0x13, 0x82, 0x09,  # LODIST
                                   0x13, 0xB2, 0x00  # CAL
                                   ])

CONFIG_REG_INIT_RF78P0G_F19P5G = ([0x10, 0x40, 0x00,  # CP1_CTRL0
                                   0x10, 0x41, 0x00,  # CP1_CTRL1
                                   0x10, 0x42, 0x86,  # CP1_CTRL2
                                   0x10, 0x43, 0x00,  # CP1_CTRL3
                                   0x10, 0x44, 0x00,  # CP1_CTRL4
                                   0x12, 0xF0, 0xA8,  # CSAMODE0
                                   0x12, 0xF3, 0x20,  # FLAG
                                   0x12, 0xF5, 0x04,  # FLAG
                                   0x13, 0x47, 0x67,  # FMCW
                                   0x13, 0x48, 0x67,  # FMCW
                                   0x13, 0x49, 0x07,  # FMCW
                                   0x13, 0x4A, 0x07,  # FMCW
                                   0x13, 0x82, 0x09,  # LODIST
                                   0x13, 0xB2, 0x00  # CAL
                                   ])

CONFIG_REG_INIT_RF80P0G_F20P0G = ([0x10, 0x40, 0x00,  # CP1_CTRL0
                                   0x10, 0x41, 0x00,  # CP1_CTRL1
                                   0x10, 0x42, 0x90,  # CP1_CTRL2
                                   0x10, 0x43, 0x00,  # CP1_CTRL3
                                   0x10, 0x44, 0x00,  # CP1_CTRL4
                                   0x12, 0xF0, 0xA8,  # CSAMODE0
                                   0x12, 0xF3, 0x00,  # FLAG
                                   0x12, 0xF5, 0x04,  # FLAG
                                   0x13, 0x47, 0x67,  # FMCW
                                   0x13, 0x48, 0x67,  # FMCW
                                   0x13, 0x49, 0x07,  # FMCW
                                   0x13, 0x4A, 0x07,  # FMCW
                                   0x13, 0x82, 0x09,  # LODIST
                                   0x13, 0xB2, 0x00  # CAL
                                   ])

READ_REG_ADDR_0001 = ([0x00, 0x01  # SPI_CTRL
                       ])

CONFIG_REG_SOFT_FSM_RESET = ([0x00, 0x01, 0x02  # SPI_CTRL SOFT_FSM_RESET
                              ])

# 1
PN_PROCESS_NAME = r"PN_Test"
PN_SHEET_TITLE = ['芯片编号',
                  'Voltage(V)', 'Current(A)',
                  'Frequency1(GHz)', 'PN1@1MHz(dBc/Hz)',
                  'Frequency2(GHz)', 'PN2@1MHz(dBc/Hz)',
                  '备注']


def pn_test_flow():
    # PN_data_list = []
    data_list = [glob_chip_num_cnt]
    # PS_E3632A_on()
    PS_E36311A_on()

    # PN Test 19.2GHz 整数分频
    CMD_batch_w_Query(CONFIG_REG_INIT_RF76P8G_F19P2G)  # 19.2GHz
    time.sleep(1)
    CMD_batch_w_Query(CONFIG_REG_SOFT_FSM_RESET)
    time.sleep(0.5)
    # CMD_batch_r_Query(READ_REG_ADDR_FREQ)
    # time.sleep(1)

    ps_value = PS_E36311A_read_volt_curr()
    data_list.append(float(ps_value[0]))
    data_list.append(float(ps_value[1]))

    PN_Value = KsInstr_PN_Test()
    time.sleep(2)
    data_list.append(float(PN_Value[0]) / 1000000000)
    data_list.append(float(PN_Value[1]))
    # PN Test 19.5GHz
    CMD_batch_w_Query(CONFIG_REG_INIT_RF78P0G_F19P5G)  # 19.5GHz
    time.sleep(1)
    CMD_batch_w_Query(CONFIG_REG_SOFT_FSM_RESET)
    time.sleep(0.5)
    # CMD_batch_r_Query(READ_REG_ADDR_FREQ)
    # time.sleep(1)

    PN_Value = KsInstr_PN_Test()
    data_list.append(float(PN_Value[0]) / 1000000000)
    data_list.append(float(PN_Value[1]))
    time.sleep(0.5)

    # PS_E3632A_off()
    PS_E36311A_off()

    # 往Sheet中写入数据（不能覆盖之前的数据），传参：excel地址、sheet名、表头、数据
    xlsx_Handle(excel_full_path, PN_PROCESS_NAME, PN_SHEET_TITLE, data_list)

    # print('PN_data_list:', PN_data_list)
    # return PN_data_list


def fn_pn_test():
    # chip_num_cnt = 0  # default
    global glob_chip_num_cnt
    while True:
        InputNum = input("Please enter your test chip number:  ")
        print("The input data received is : ", InputNum)
        if InputNum.isalpha():
            if InputNum.upper() == 'ESC':
                print("Quit 'PN_Test', Back to Test")
                break
            elif InputNum.upper() == 'N':  # 用于验证测试数据写入Excel是否成功
                glob_chip_num_cnt += 1
                print('It is only used to verify that the function of Excel is normal.')
                print('ChipNum Increases automatically. ChipNum: ', glob_chip_num_cnt)
                useful_data_list = [1, 'n', 1, 'n', 'PN_Test']
                data_list = [glob_chip_num_cnt] + useful_data_list
                # 往Sheet中写入数据（不能覆盖之前的数据），传参：excel地址、sheet名、表头、数据
                xlsx_Handle(excel_full_path, PN_PROCESS_NAME, PN_SHEET_TITLE, data_list)
            else:
                print("illegal input")
                continue
        elif InputNum.isdigit():  # 手动输入测试编号
            glob_chip_num_cnt = int(InputNum)
            print('input ChipNum: ', glob_chip_num_cnt)
            # useful_data_list = pn_test_flow()
            pn_test_flow()
        elif InputNum == '':  # 回车用于累加 测试编号
            glob_chip_num_cnt += 1
            print('ChipNum increase: ', glob_chip_num_cnt)
            # useful_data_list = pn_test_flow()
            pn_test_flow()
        else:
            print("illegal input")
            continue
        print('Chip', glob_chip_num_cnt, 'PN test is finished')


# 2
PWR_PROCESS_NAME = r"PWR_Test"
PWR_SHEET_TITLE = ['芯片编号', 'Voltage(V)', 'Current(A)', 'Freq(GHz)', 'Power(dBm)', '备注']


def pwr_test_flow():
    # PWR_data_list = [glob_chip_num_cnt]
    data_list = [glob_chip_num_cnt]
    # PS_E3632A_on()
    PS_E36311A_on()

    # PN Test 19.2GHz 整数分频
    CMD_batch_w_Query(CONFIG_REG_INIT_RF76P8G_F19P2G)  # 19.2GHz
    time.sleep(1)
    CMD_batch_w_Query(CONFIG_REG_SOFT_FSM_RESET)
    time.sleep(0.5)

    ps_value = PS_E36311A_read_volt_curr()
    data_list.append(float(ps_value[0]))
    data_list.append(float(ps_value[1]))

    Power_Value = KsInstr_Power_Test()
    time.sleep(1)
    # data_list.append(Power_Value[0])
    # data_list.append(Power_Value[1])
    data_list.append(float(Power_Value[0]) / 1000000000)
    data_list.append(float(Power_Value[1]))
    # print('PWR data_list: ', data_list)

    # PS_E3632A_off()
    PS_E36311A_off()

    # 往Sheet中写入数据（不能覆盖之前的数据），传参：excel地址、sheet名、表头、数据
    xlsx_Handle(excel_full_path, PWR_PROCESS_NAME, PWR_SHEET_TITLE, data_list)

    # return data_list


def fn_pwr_test():
    # chip_num_cnt = 0  # default
    global glob_chip_num_cnt
    while True:
        InputNum = input("Please enter your test chip number:  ")
        print("The input data received is : ", InputNum)
        if InputNum.isalpha():
            if InputNum.upper() == 'ESC':
                print("Quit 'PWR_Test', Back to Test")
                break
            elif InputNum.upper() == 'N':  # 用于验证测试数据写入Excel是否成功
                glob_chip_num_cnt += 1
                print('It is only used to verify that the function of Excel is normal.')
                print('ChipNum Increases automatically. ChipNum: ', glob_chip_num_cnt)
                useful_data_list = [5, 1, 2, 'n', 'PWR_Test']
                data_list = [glob_chip_num_cnt] + useful_data_list
                # 往Sheet中写入数据（不能覆盖之前的数据），传参：excel地址、sheet名、表头、数据
                xlsx_Handle(excel_full_path, PWR_PROCESS_NAME, PWR_SHEET_TITLE, data_list)
            else:
                print("illegal input")
                continue
        elif InputNum.isdigit():  # 手动输入测试编号
            glob_chip_num_cnt = int(InputNum)
            print('input ChipNum: ', glob_chip_num_cnt)
            # useful_data_list = pwr_test_flow()
            pwr_test_flow()
        elif InputNum == '':  # 回车用于累加 测试编号
            glob_chip_num_cnt += 1
            print('ChipNum increase: ', glob_chip_num_cnt)
            # useful_data_list = pwr_test_flow()
            pwr_test_flow()
        else:
            print("illegal input")
            continue
        print('Chip', glob_chip_num_cnt, 'PWR test is finished')


# 3
PLL_PROCESS_NAME = r"PLL_Test"
PLL_SHEET_TITLE = ['芯片编号',
                   '0x1345', '0x1372',
                   'Voltage(V)', 'Current(A)',
                   'Sync_out_Freq MAX(GHz)', 'Sync_out_Power(dBm)',
                   'Sync_out_Freq MIN(GHz)', 'Sync_out_Power(dBm)',
                   '备注']


def pll_freq_response_range_test_flow():
    # PLL frequency response range
    PLL_TEST_READ_REG_ADDR = ([0x13, 0x45,  # FMCW
                               0x13, 0x72  # SYSPLL
                               ])
    PLL_CONFIG_FREQ_MAX = ([0x12, 0xF4, 0x01,  # FLAG
                            0x12, 0xF5, 0x44,  # FLAG
                            0x13, 0x41, 0xE1,  # FMCW
                            0x13, 0x45, 0x08,  # FMCW
                            ])
    PLL_CONFIG_FREQ_MIN = ([0x13, 0x45, 0xF8,  # FMCW
                            ])
    PLL_RESET_CONFIG = ([0x12, 0xF4, 0x00,  # FLAG
                         0x12, 0xF5, 0x04,  # FLAG
                         ])

    # PLL_data_list = [glob_chip_num_cnt]
    data_list = [glob_chip_num_cnt]
    # PS_E3632A_on()
    PS_E36311A_on()

    read_data = CMD_batch_r_Query(PLL_TEST_READ_REG_ADDR)
    time.sleep(0.5)
    read_data_len = len(read_data)
    for num in range(math.trunc(read_data_len / 2)):
        data_list.append(read_data[2 * num + 1])

    CMD_batch_w_Query(TEST_MODE_REG_INIT)  # 19.5GHz
    time.sleep(0.5)
    CMD_batch_w_Query(CONFIG_REG_SOFT_FSM_RESET)
    time.sleep(0.5)

    ps_value = PS_E36311A_read_volt_curr()
    data_list.append(float(ps_value[0]))
    data_list.append(float(ps_value[1]))

    CMD_batch_w_Query(PLL_CONFIG_FREQ_MAX)  # config PLL
    time.sleep(0.2)
    # CMD_batch_w_Query(SOFT_FSM_RESET)
    # time.sleep(2)
    Max_Freq_Value = KsInstr_Freq_Test()
    time.sleep(0.5)
    data_list.append(float(Max_Freq_Value[0]) / 1000000000)
    data_list.append(float(Max_Freq_Value[1]))

    CMD_batch_w_Query(PLL_CONFIG_FREQ_MIN)  # config PLL
    time.sleep(0.2)
    # CMD_batch_w_Query(SOFT_FSM_RESET)
    # time.sleep(2)
    Min_Freq_Value = KsInstr_Freq_Test()
    time.sleep(0.5)
    data_list.append(float(Min_Freq_Value[0]) / 1000000000)
    data_list.append(float(Min_Freq_Value[1]))
    # print('PLL_data_list:', PLL_data_list)
    CMD_batch_w_Query(PLL_RESET_CONFIG)  # config PLL
    time.sleep(0.1)
    CMD_batch_w_Query(CONFIG_REG_SOFT_FSM_RESET)
    time.sleep(0.5)

    # PS_E3632A_off()
    PS_E36311A_off()
    # print('PLL test is finished')

    # 往Sheet中写入数据（不能覆盖之前的数据），传参：excel地址、sheet名、表头、数据
    xlsx_Handle(excel_full_path, PLL_PROCESS_NAME, PLL_SHEET_TITLE, data_list)

    # return True


def fn_pll_test():
    global glob_chip_num_cnt
    while True:
        InputNum = input("Please enter your test chip number:  ")
        print("The input data received is : ", InputNum)
        if InputNum.isalpha():
            if InputNum.upper() == 'ESC':
                print("Quit 'PLL_Test', Back to Test")
                break
            elif InputNum.upper() == 'N':  # 用于验证测试数据写入Excel是否成功
                glob_chip_num_cnt += 1
                print('It is only used to verify that the function of Excel is normal.')
                print('ChipNum Increases automatically. ChipNum: ', glob_chip_num_cnt)
                useful_data_list = ['Test', 'test1', 3, 'n', 'PLL测试']
                data_list = [glob_chip_num_cnt] + useful_data_list
                # 往Sheet中写入数据（不能覆盖之前的数据），传参：excel地址、sheet名、表头、数据
                xlsx_Handle(excel_full_path, PLL_PROCESS_NAME, PLL_SHEET_TITLE, data_list)
            else:
                print("illegal input")
                continue
        elif InputNum.isdigit():  # 手动输入测试编号
            glob_chip_num_cnt = int(InputNum)
            print('input ChipNum: ', glob_chip_num_cnt)
            # useful_data_list = pll_freq_response_range_test_flow()  # PLL频响范围测试
            pll_freq_response_range_test_flow()  # PLL频响范围测试
        elif InputNum == '':  # 回车用于累加 测试编号
            glob_chip_num_cnt += 1
            print('ChipNum increase: ', glob_chip_num_cnt)
            # useful_data_list = pll_freq_response_range_test_flow()  # PLL频响范围测试
            pll_freq_response_range_test_flow()  # PLL频响范围测试
        else:
            print("illegal input")
            continue
        print('chip', glob_chip_num_cnt, 'PLL test is finished')


# 4
PLL_DC_PROCESS_NAME = r"PLL_DC_Test"
PLL_DC_SHEET_TITLE = ['芯片编号',
                      '0x1345', '0x1372',
                      'Voltage(V)', 'Current(A)',
                      'Sync_out_Freq MAX(GHz)', 'Sync_out_Power(dBm)',
                      'MUX_SEL(0x135B)', 'GPADC_IN[11:8](0x135D)', 'GPADC_IN[7:0](0x135C)',
                      'GPADC_IN(DEC)', 'GPADC_IN Voltage(V)',
                      '备注']


# def pll_dc_test_flow(chip_cnt):
def pll_dc_test_flow():
    # PLL frequency response range
    PLL_TEST_READ_REG_ADDR = ([0x13, 0x45,  # FMCW
                               0x13, 0x72  # SYSPLL
                               ])
    # PLL_CONFIG_FREQ_MAX = ([0x12, 0xF4, 0x01,  # FLAG
    #                         0x12, 0xF5, 0x44,  # FLAG
    #                         0x13, 0x41, 0xE1,  # FMCW
    #                         0x13, 0x45, 0x08,  # FMCW
    #                         ])
    # PLL_CONFIG_FREQ_MIN = ([0x13, 0x45, 0xF8,  # FMCW
    #                         ])
    # PLL_RESET_CONFIG = ([0x12, 0xF4, 0x00,  # FLAG
    #                      0x12, 0xF5, 0x01,  # FLAG
    #                      ])

    # data_list = [chip_cnt]
    data_list = [glob_chip_num_cnt]
    # PS_E3632A_on()
    PS_E36311A_on()

    read_data = CMD_batch_r_Query(PLL_TEST_READ_REG_ADDR)
    time.sleep(0.5)
    read_data_len = len(read_data)
    for num in range(math.trunc(read_data_len / 2)):
        data_list.append(read_data[2 * num + 1])

    # PN Test 19.2GHz 整数分频
    CMD_batch_w_Query(CONFIG_REG_INIT_RF76P8G_F19P2G)  # 19.2GHz
    time.sleep(0.5)
    CMD_batch_w_Query(CONFIG_REG_SOFT_FSM_RESET)
    time.sleep(0.5)

    ps_value = PS_E36311A_read_volt_curr()
    data_list.append(float(ps_value[0]))
    data_list.append(float(ps_value[1]))

    if 0:  # 1:读取频率和幅度，0：不读频率和幅度，加快测试
        Max_Freq_Value = KsInstr_Freq_Test()
        time.sleep(0.5)
        data_list.append(float(Max_Freq_Value[0]) / 1000000000)
        data_list.append(float(Max_Freq_Value[1]))
    else:  # 0：不读频率和幅度，加快测试
        Max_Freq_Value = ['NO TEST', 'NO TEST']
        data_list.append(Max_Freq_Value[0])
        data_list.append(Max_Freq_Value[1])

    # 往Sheet中写入数据（不能覆盖之前的数据），传参：excel地址、sheet名、表头、数据
    xlsx_Handle(excel_full_path, PLL_DC_PROCESS_NAME, PLL_DC_SHEET_TITLE, data_list)

    # gpadc_in_data = gpadc_dc_test(data_list[1])
    gpadc_in_data = gpadc_dc_test()
    # gpadc_in_data = [0, '0x19', '0x09', 1, '0x85', '0x09', 2, '0x64', '0x08', 3, 4, 5, 6, 7, 8, 9, 10, 11]
    # GPADC 读取数据写入函数，传参：excel地址、sheet名、表头、数据
    GPADC_xlsx_Handle(excel_full_path, PLL_DC_PROCESS_NAME, PLL_DC_SHEET_TITLE, gpadc_in_data)
    # print('data_list:', data_list)

    # CMD_batch_w_Query(PLL_RESET_CONFIG)  # config PLL
    # time.sleep(0.1)
    # CMD_batch_w_Query(CONFIG_REG_SOFT_FSM_RESET)
    # time.sleep(0.5)

    # PS_E3632A_off()
    # PS_E36311A_off()
    # print('PLL test is finished')
    # return data_list


def fn_pll_dc_test():
    # chip_num_cnt = 0  # default
    global glob_chip_num_cnt
    while True:
        InputNum = input("Please enter your test chip number:  ")
        print("The input data received is : ", InputNum)
        if InputNum.isalpha():
            if InputNum.upper() == 'ESC':
                print("Quit 'PLL_Test', Back to Test")
                break
            elif InputNum.upper() == 'N':  # 用于验证测试数据写入Excel是否成功
                glob_chip_num_cnt += 1
                print('It is only used to verify that the function of Excel is normal.')
                print('ChipNum Increases automatically. ChipNum: ', glob_chip_num_cnt)
                useful_data_list = ['Test', 'test1', 3, 'n', 'PLL DC测试']
                data_list = [glob_chip_num_cnt] + useful_data_list
                # 往Sheet中写入数据（不能覆盖之前的数据），传参：excel地址、sheet名、表头、数据
                xlsx_Handle(excel_full_path, PLL_DC_PROCESS_NAME, PLL_DC_SHEET_TITLE, data_list)
            else:
                print("illegal input")
                continue
        elif InputNum.isdigit():  # 手动输入测试编号
            glob_chip_num_cnt = int(InputNum)
            print('input ChipNum: ', glob_chip_num_cnt)
            # useful_data_list = pll_dc_test_flow()  # PLL频响范围测试
            pll_dc_test_flow()  # PLL频响范围测试
        elif InputNum == '':  # 回车用于累加 测试编号
            glob_chip_num_cnt += 1
            print('ChipNum increase: ', glob_chip_num_cnt)
            # useful_data_list = pll_dc_test_flow()  # PLL频响范围测试
            pll_dc_test_flow()  # PLL频响范围测试
        else:
            print("illegal input")
            continue
        print('chip', glob_chip_num_cnt, 'PLL test is finished')


# 5
IF_PROCESS_NAME = r"IF_Test"
IF_SHEET_TITLE = ['芯片编号', 'Voltage(V)', 'Current(A)', 'IF Freq(MHz)', 'IF Power(dBm)', '备注']


def IF_test_flow():
    RX_Test_config = ([0x13, 0x07, 0x00])
    # IF_data_list = []
    data_list = [glob_chip_num_cnt]
    # PS_E3632A_on()
    PS_E36311A_on()
    CMD_batch_w_Query(CONFIG_REG_INIT_RF80P0G_F20P0G)  # SYNC_out:20G    RF:80GHz
    time.sleep(1)
    CMD_batch_w_Query(CONFIG_REG_SOFT_FSM_RESET)
    time.sleep(0.5)
    CMD_batch_w_Query(RX_Test_config)
    time.sleep(0.5)

    ps_value = PS_E36311A_read_volt_curr()
    data_list.append(float(ps_value[0]))
    data_list.append(float(ps_value[1]))

    IF_value = KsInstr_IF_Test()  # IF测试
    data_list.append(float(IF_value[0]) / 1000000)
    data_list.append(float(IF_value[1]))

    # PS_E3632A_off()
    PS_E36311A_off()

    # 往Sheet中写入数据（不能覆盖之前的数据），传参：excel地址、sheet名、表头、数据
    xlsx_Handle(excel_full_path, IF_PROCESS_NAME, IF_SHEET_TITLE, data_list)

    # return IF_data_list


def fn_IF_Test():
    global glob_chip_num_cnt
    # chip_num_cnt = 0  # default
    while True:
        InputNum = input("Please enter your test chip number:  ")
        print("The input data received is : ", InputNum)
        if InputNum.isalpha():
            if InputNum.upper() == 'ESC':
                print("Quit 'IF_Test', Back to Test")
                break
            elif InputNum.upper() == 'N':  # 用于验证测试数据写入Excel是否成功
                glob_chip_num_cnt += 1
                print('It is only used to verify that the function of Excel is normal.')
                print('ChipNum Increases automatically. ChipNum: ', glob_chip_num_cnt)
                Useful_Data_list = ['IF', 4, 'n', 'IF Test']
                data_list = [glob_chip_num_cnt] + Useful_Data_list
                # 往Sheet中写入数据（不能覆盖之前的数据），传参：excel地址、sheet名、表头、数据
                xlsx_Handle(excel_full_path, IF_PROCESS_NAME, IF_SHEET_TITLE, data_list)
            else:
                print("illegal input")
                continue
        elif InputNum.isdigit():  # 手动输入测试编号
            glob_chip_num_cnt = int(InputNum)
            print('input ChipNum: ', glob_chip_num_cnt)
            # Useful_Data_list = IF_test_flow()
            IF_test_flow()
        elif InputNum == '':  # 回车用于累加 测试编号
            glob_chip_num_cnt += 1
            print('ChipNum increase: ', glob_chip_num_cnt)
            # Useful_Data_list = IF_test_flow()
            IF_test_flow()
        else:
            print("illegal input")
            continue
        print('chip', glob_chip_num_cnt, 'IF test is finished')


# All
def test_all_case_process():
    print('++++++++++++++++      PN_Test      ++++++++++++++++')
    pn_test_flow()

    print('++++++++++++++++      PLL_Test      ++++++++++++++++')
    pll_freq_response_range_test_flow()

    print('++++++++++++++++      PLL_DC_Test   ++++++++++++++++')
    pll_dc_test_flow()
    # uf_data_list = pll_dc_test_flow()
    # dat_list = [glob_chip_num_cnt] + uf_data_list
    # xlsx_Handle(excel_full_path, PLL_PROCESS_NAME, PLL_SHEET_TITLE, dat_list)

    # print('IF_Test')
    # uf_data_list = IF_test_flow()
    # dat_list = [glob_chip_num_cnt] + uf_data_list
    # xlsx_Handle(excel_full_path, IF_PROCESS_NAME, IF_SHEET_TITLE, dat_list)


def fn_test_all_case():
    global glob_chip_num_cnt
    while True:
        InputD = input("Please enter your test chip number:  ")
        print("The input data received is : ", InputD)
        if InputD.isalpha():
            if InputD.upper() == 'ESC':
                print("Quit 'PLL_Test', Back to Test")
                break
            else:
                print("illegal input")
                continue
        elif InputD.isdigit():  # 手动输入测试编号
            glob_chip_num_cnt = int(InputD)
            print('input ChipNum: ', glob_chip_num_cnt)
            test_all_case_process()
        elif InputD == '':  # 回车用于累加 测试编号
            glob_chip_num_cnt += 1
            print('ChipNum increase: ', glob_chip_num_cnt)
            test_all_case_process()
        else:
            print("illegal input")
            continue


# TEST_CASE_LIST = ['0',  # help
#                   '1',  # PN_test
#                   '2',  # Freq_test
#                   '3',  # PLL_test
#                   '4'  # IF_test
#                   ]
INPUT_HELP_MSG_LIST = ["\n++++++++++      Help notes           ++++++++++",
                       "----------  '0': Help                ----------",
                       "----------  '1': PN_test             ----------",
                       "----------  '2': PWR_test            ----------",
                       "----------  '3': PLL_test            ----------",
                       "----------  '4': PLL_DC_test         ----------",
                       "----------  '5': IF_test             ----------",
                       "----------                           ----------",
                       "----------  'all': case1,3,4         ----------",
                       "+++++++++++++++++++ end +++++++++++++++++++\n",
                       ]


def print_help_msg():
    for input_help_msg_cnt in range(len(INPUT_HELP_MSG_LIST)):
        print(INPUT_HELP_MSG_LIST[input_help_msg_cnt])


# fn:function

if __name__ == '__main__':
    ComConfig()  # COM口配置
    PS_E36311A_init_cfg()  # power supply E36311A Init config
    print('Signal Analyzer info: ', PXA_N9030B.query('*IDN?')[:-1])  # [:-1]去掉返回数据的最后2个字符'\n'
    print('Power Supply info:    ', PS_E36311A.query('*IDN?')[:-1])  # [:-1]去掉返回数据的最后2个字符'\n'
    # mkdir(TEST_LOG_FOLDER)  # 调用函数 创建文件夹
    mkdir(TEST_DATA_FOLDER)  # 调用函数 创建文件夹

    # try:
    #     excel_full_path = xlsx_init(Test_Data_Folder)  # 新建Excel并获取新建Excel的地址 efn：excel full name
    #     print('excel_full_path', excel_full_path)
    # except Exception as e:
    #     print("新建excel异常", e)
    excel_full_path = xlsx_init(TEST_DATA_FOLDER)  # 新建Excel并获取新建Excel的地址 efn：excel full name

    # print help message
    print_help_msg()
    glob_chip_num_cnt = 0
    # Test mode selection
    while True:
        InputData = input("Please enter your test case number:  ")
        print("The input data received is : ", InputData)
        # if InputData in TEST_CASE_LIST:
        if InputData.isdigit():  # 判断输入是否为数字
            if '0' == InputData:  # print help
                print_help_msg()
            elif '1' == InputData:  # PN_Test
                print(INPUT_HELP_MSG_LIST[int(InputData) + 1])
                fn_pn_test()
            elif '2' == InputData:  # PWR_Test
                print(INPUT_HELP_MSG_LIST[int(InputData) + 1])
                fn_pwr_test()
            elif '3' == InputData:  # PLL_Test
                print(INPUT_HELP_MSG_LIST[int(InputData) + 1])
                fn_pll_test()
            elif '4' == InputData:  # PLL_DC_Test
                print(INPUT_HELP_MSG_LIST[int(InputData) + 1])
                fn_pll_dc_test()
            elif '5' == InputData:  # IF_Test
                print(INPUT_HELP_MSG_LIST[int(InputData) + 1])
                fn_IF_Test()
            elif '9' == InputData:  # Test
                # print(INPUT_HELP_MSG_LIST[int(InputData) + 1])
                print('Test mode : 9')
                # chip_reg.reg_write(0x1342, 0x01)
                for test_val in (0x23, 0x63):
                    print('++++++++++++++++++++      test_val : ', '0x%02X' % test_val, ' Test      ++++++++++++++++++++')

            else:
                print("illegal input：", InputData)
                print_help_msg()
                continue
                # break
        elif InputData.isalpha():
            if 'ESC' == InputData.upper():
                print('Quit "Test Mode", Test End')
                break
            elif 'ALL' == InputData.upper():  # Test all cases at once
                print('Test all cases at once')
                # glob_chip_num_cnt = 0
                fn_test_all_case()
            else:
                print("illegal input：", InputData)
                print_help_msg()
                continue
                # break
        else:
            print("illegal input：", InputData)
            print_help_msg()
            continue

    # PWR_Supply_com.write([0x4F, 0x55, 0x54, 0x70, 0x75, 0x74, 0x20, 0x4F, 0x4E, 0x0A])  # OUTput ON
    # time.sleep(2)
    # PWR_Test_process()    # 功率测试
    # PN_Test_process()    # PN测试
    # PLL_Freq_Response_Range_process()  # PLL频响范围测试
    # PWR_Supply_com.write([0x4F, 0x55, 0x54, 0x70, 0x75, 0x74, 0x20, 0x4F, 0x46, 0x46, 0x0A])  # OUTput OFF电源output off
    # while True:
    #     print('Pll test ok')
    #     time.sleep(3)

    # # t1 = threading.Thread(target=receive_data)  # 创建一个线程1：不断的去请求数据
    # # t2 = threading.Thread(target=send_data)  # 创建一个线程2：不断的去发送数据
    # # t2.start()  # 开启线程2
    # # t1.start()  # 开启线程1

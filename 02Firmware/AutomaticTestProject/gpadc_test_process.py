import math
import time

from pandas import cut

from encode import CMD_batch_w_Query, CMD_batch_r_Query
# from reg import REG_W_1363
import chip_reg
from chip_reg import reg_write


# from main import CONFIG_REG_SOFT_FSM_RESET


def diff_mode_data_encode(data_list=None, gpadc_data_list=None, data_rows_cnt=None):
    data_list.append(gpadc_data_list[3 * data_rows_cnt + 0])
    data_list.append(gpadc_data_list[3 * data_rows_cnt + 1])
    data_list.append(gpadc_data_list[3 * data_rows_cnt + 2])

    reg_data_h = int(gpadc_data_list[3 * data_rows_cnt + 1], 16)
    reg_data_l = int(gpadc_data_list[3 * data_rows_cnt + 2], 16)
    data_list.append(((reg_data_h << 8) | reg_data_l))
    data_list.append(float(((reg_data_h << 8) | reg_data_l) - 2048) / 2048 * 2.7)


def single_mode_data_encode(data_list=None, gpadc_data_list=None, data_rows_cnt=None):
    data_list.append(gpadc_data_list[3 * data_rows_cnt + 0])
    data_list.append(gpadc_data_list[3 * data_rows_cnt + 1])
    data_list.append(gpadc_data_list[3 * data_rows_cnt + 2])

    reg_data_h = int(gpadc_data_list[3 * data_rows_cnt + 1], 16)
    reg_data_l = int(gpadc_data_list[3 * data_rows_cnt + 2], 16)
    data_list.append(((reg_data_h << 8) | reg_data_l))
    data_list.append(float(((reg_data_h << 8) | reg_data_l)) / 4096 * 2.7)


# def gpadc_dc_test(reg_1345_init_value):
def gpadc_dc_test():
    # REG_1341_INIT = [0x13, 0x41, 0x00  # FMCW
    #                  ]
    # REG_1342_INIT = [0x13, 0x42, 0x00  # FMCW
    #                  ]

    # REG_W_1341_CFG1 = [0x13, 0x41, 0xC0  # FMCW
    #                  ]
    # REG_W_1342_CFG1 = [0x13, 0x42, 0xC0  # FMCW
    #                  ]
    # #######################################################################################
    PLL_TEST_READ_REG_ADDR = [0x13, 0x45,  # FMCW
                              0x13, 0x72  # SYSPLL
                              ]
    REG_W_12F0_MUX_DIFF = [0x12, 0xF0, 0xB8  # CASMODE0
                           ]
    REG_W_12F0_MUX_SINGLE = [0x12, 0xF0, 0xA8  # CASMODE0
                             ]
    REG_W_12F5_INIT = [0x12, 0xF5, 0x01  # FLAG
                       ]
    REG_W_12F7_INIT = [0x12, 0xF7, 0x16  # RX
                       ]
    REG_W_12F4_INIT = [0x12, 0xF4, 0x08  # FLAG
                       ]

    REG_R_GPADC_IN = [0x13, 0x5D,  # FMCW
                      0x13, 0x5C  # FMCW
                      ]
    CONFIG_REG_SOFT_FSM_RESET = [0x00, 0x01, 0x02  # SPI_CTRL SOFT_FSM_RESET
                                 ]
    # ############################## mux_sel：0-2 ##########################
    R_1345_1372_VALUE = CMD_batch_r_Query(PLL_TEST_READ_REG_ADDR)
    # print('READ_REG_LODIST_ADDR : ', R_1345_1372_VALUE)
    time.sleep(0.5)
    REG_W_1345_CFG = [0x13, 0x45, int(R_1345_1372_VALUE[1], 16)]

    REG_W_12F5_CFG1 = [0x12, 0xF5, 0x41  # FLAG
                       ]
    REG_W_1341_1342_CFG1 = [0x13, 0x41, 0xC0,  # FMCW
                            0x13, 0x42, 0xC0  # FMCW
                            ]
    REG_W_1341_1342_INIT = [0x13, 0x41, 0x00,  # FMCW
                            0x13, 0x42, 0x00  # FMCW
                            ]
    # ############################## mux_sel：3-5 ##########################
    REG_W_GPADC_LO_FLAG_CONFIG = [0x12, 0xF3, 0x23,  #
                                  0x12, 0xF4, 0x88  #
                                  ]
    REG_W_1383_CFG = [0x13, 0x83, 0x00  # FLAG
                      ]
    REG_W_1383_INIT = [0x13, 0x83, 0x38  # FLAG
                       ]
    READ_REG_W138C_F_ADDR = [0x13, 0x8C,  # LODIST
                             0x13, 0x8D,  # LODIST
                             0x13, 0x8E,  # LODIST
                             0x13, 0x8F  # LODIST
                             ]
    REG_W138C_F_VALUE = CMD_batch_r_Query(READ_REG_W138C_F_ADDR)
    # print('READ_REG_LODIST_ADDR : ', REG_W138C_F_VALUE)
    time.sleep(0.5)
    REG_W_138C_138F_CFG = [0x13, 0x8C, int(REG_W138C_F_VALUE[1], 16),
                           0x13, 0x8D, int(REG_W138C_F_VALUE[3], 16),
                           0x13, 0x8E, int(REG_W138C_F_VALUE[5], 16),
                           0x13, 0x8F, int(REG_W138C_F_VALUE[7], 16),
                           ]

    REG_W_GPADC_LO_FLAG_INIT = [0x12, 0xF4, 0x08,  #
                                0x12, 0xF3, 0x20  #
                                ]
    # ############################## mux_sel：6-9 ##########################
    REG_W_1327_CFG = [0x13, 0x27, 0x10  # FLAG
                      ]
    REG_W_1327_INIT = [0x13, 0x27, 0x1F  # FLAG
                       ]
    REG_W_12F4_CFG = [0x12, 0xF4, 0x78  # FLAG
                      ]
    READ_REG_W132C_30_ADDR = [0x13, 0x2C,  # TX
                              0x13, 0x2D,  # TX
                              0x13, 0x2E,  # TX
                              0x13, 0x2F,  # TX
                              0x13, 0x30  # TX
                              ]
    R_132C_1330_VALUE = CMD_batch_r_Query(READ_REG_W132C_30_ADDR)
    time.sleep(0.5)

    REG_W_132C_1330_CFG = [0x13, 0x2C, int(R_132C_1330_VALUE[1], 16),
                           0x13, 0x2D, int(R_132C_1330_VALUE[3], 16),
                           0x13, 0x2E, int(R_132C_1330_VALUE[5], 16),
                           0x13, 0x2F, int(R_132C_1330_VALUE[7], 16),
                           0x13, 0x30, int(R_132C_1330_VALUE[9], 16),
                           ]
    # ############################## mux_sel：10 ##########################
    REG_W_12F3_CFG = [0x12, 0xF3, 0x24  #
                      ]
    REG_W_12F3_INIT = [0x12, 0xF3, 0x20  #
                       ]
    REG_W_1309_CFG = [0x13, 0x09, 0x01  #
                      ]
    REG_W_1309_INIT = [0x13, 0x09, 0x03  #
                       ]
    READ_REG_W130F_10_ADDR = [0x13, 0x0F,  #
                              0x13, 0x10  #
                              ]
    R_130F_1310_VALUE = CMD_batch_r_Query(READ_REG_W130F_10_ADDR)
    time.sleep(0.5)
    REG_W_130F_1310_CFG = [0x13, 0x2C, int(R_130F_1310_VALUE[1], 16),
                           0x13, 0x2D, int(R_130F_1310_VALUE[3], 16),
                           ]
    # ############################## mux_sel：11 ##########################
    REG_W_1363_CFG = [0x13, 0x63, 0x08  #
                      ]
    REG_W_1363_INIT = [0x13, 0x63, 0x00  #
                       ]
    # #######################################################################################
    data_list = []
    gpadc_data_list = []
    # #######################################################################################
    # CMD_batch_w_Query([0x12, 0xF5, 0x01])
    CMD_batch_w_Query(REG_W_12F5_INIT)
    CMD_batch_w_Query(REG_W_12F7_INIT)
    CMD_batch_w_Query(REG_W_12F4_INIT)
    # 把0x1345初始值写进来
    CMD_batch_w_Query(REG_W_1345_CFG)
    time.sleep(0.5)
    data_rows_cnt = 0
    # ########################## mux_sel：0-2 ##########################
    print('++++++++++++++++++++      MUX_SEL : 0-2 Test      ++++++++++++++++++++')
    CMD_batch_w_Query(REG_W_12F0_MUX_DIFF)
    CMD_batch_w_Query(REG_W_12F5_CFG1)  # 会改变reg 0x1345的初始值
    CMD_batch_w_Query(REG_W_1341_1342_CFG1)
    for reg_135B_cfg in range(0, 3):
        print('++++++++++++++++++++      MUX_SEL(0x135B) : ', reg_135B_cfg, ' Test      ++++++++++++++++++++')
        gpadc_data_list.append(reg_135B_cfg)
        CMD_batch_w_Query(chip_reg.reg_write(0x135B, reg_135B_cfg))
        time.sleep(0.2)
        read_data = CMD_batch_r_Query(REG_R_GPADC_IN)
        time.sleep(0.5)
        read_data_len = len(read_data)
        for cnt in range(math.trunc(read_data_len / 2)):
            gpadc_data_list.append(read_data[2 * cnt + 1])
        # 在此处将读出的GPADC数据计算为十进制数，放在每个序列的第四个，计算电压放在每个序列的第五个，后面有新增序列的话，前面表头要修改
        # print('data_list : ', data_list)
        # print('gpadc_data_list : ', gpadc_data_list)
        # print('data_rows_cnt : ', data_rows_cnt)
        diff_mode_data_encode(data_list, gpadc_data_list, data_rows_cnt)
        data_rows_cnt += 1
    CMD_batch_w_Query(REG_W_1341_1342_INIT)
    CMD_batch_w_Query(REG_W_12F5_INIT)
    # CMD_batch_w_Query(REG_W_12F4_INIT)
    CMD_batch_w_Query(CONFIG_REG_SOFT_FSM_RESET)
    time.sleep(0.5)

    # ########################## mux_sel：3-5 ##########################
    print('++++++++++++++++++++      MUX_SEL : 3-5 Test      ++++++++++++++++++++')
    CMD_batch_w_Query(REG_W_GPADC_LO_FLAG_CONFIG)
    time.sleep(0.5)
    CMD_batch_w_Query(REG_W_1383_CFG)
    # CMD_batch_r_Query(READ_REG_W138C_F_ADDR)
    CMD_batch_w_Query(REG_W_138C_138F_CFG)
    time.sleep(0.2)
    for reg_135B_cfg in range(3, 6):
        print('++++++++++++++++++++      MUX_SEL(0x135B) : ', reg_135B_cfg, ' Test      ++++++++++++++++++++')
        gpadc_data_list.append(reg_135B_cfg)
        CMD_batch_w_Query(chip_reg.reg_write(0x135B, reg_135B_cfg))
        time.sleep(0.2)
        # CMD_batch_r_Query(READ_REG_W138C_F_ADDR)
        read_data = CMD_batch_r_Query(REG_R_GPADC_IN)
        time.sleep(0.5)
        read_data_len = len(read_data)
        for cnt in range(math.trunc(read_data_len / 2)):
            gpadc_data_list.append(read_data[2 * cnt + 1])
        # 在此处将读出的GPADC数据计算为十进制数，放在每个序列的第四个，计算电压放在每个序列的第五个，后面有新增序列的话，前面表头要修改
        diff_mode_data_encode(data_list, gpadc_data_list, data_rows_cnt)
        data_rows_cnt += 1
    CMD_batch_w_Query(REG_W_GPADC_LO_FLAG_INIT)
    CMD_batch_w_Query(REG_W_1383_INIT)
    CMD_batch_w_Query(CONFIG_REG_SOFT_FSM_RESET)
    time.sleep(0.5)

    # ########################## mux_sel：6-9 ##########################
    print('++++++++++++++++++++      MUX_SEL : 6-9 Test      ++++++++++++++++++++')
    CMD_batch_w_Query(REG_W_1327_CFG)
    CMD_batch_w_Query(REG_W_12F4_CFG)
    CMD_batch_w_Query(REG_W_132C_1330_CFG)
    time.sleep(0.5)
    for reg_135B_cfg in range(6, 10):
        print('++++++++++++++++++++      MUX_SEL(0x135B) : ', reg_135B_cfg, ' Test      ++++++++++++++++++++')
        gpadc_data_list.append(reg_135B_cfg)
        CMD_batch_w_Query(chip_reg.reg_write(0x135B, reg_135B_cfg))
        time.sleep(0.2)
        read_data = CMD_batch_r_Query(REG_R_GPADC_IN)
        time.sleep(0.5)
        read_data_len = len(read_data)
        for cnt in range(math.trunc(read_data_len / 2)):
            gpadc_data_list.append(read_data[2 * cnt + 1])
        # 在此处将读出的GPADC数据计算为十进制数，放在每个序列的第四个，计算电压放在每个序列的第五个，后面有新增序列的话，前面表头要修改
        diff_mode_data_encode(data_list, gpadc_data_list, data_rows_cnt)
        data_rows_cnt += 1
    CMD_batch_w_Query(REG_W_1327_INIT)
    CMD_batch_w_Query(REG_W_12F4_INIT)
    CMD_batch_w_Query(CONFIG_REG_SOFT_FSM_RESET)
    time.sleep(0.5)

    # ########################## mux_sel：10 ##########################
    print('++++++++++++++++++++      MUX_SEL : 10 Test      ++++++++++++++++++++')
    CMD_batch_w_Query(REG_W_12F3_CFG)
    CMD_batch_w_Query(REG_W_1309_CFG)
    CMD_batch_w_Query(REG_W_130F_1310_CFG)
    time.sleep(0.5)
    for reg_135B_cfg in range(10, 11):
        print('++++++++++++++++++++      MUX_SEL(0x135B) : ', reg_135B_cfg, ' Test      ++++++++++++++++++++')
        gpadc_data_list.append(reg_135B_cfg)
        # gpadc_data_list.append('0x%02X' % reg_135B_cfg)
        CMD_batch_w_Query(chip_reg.reg_write(0x135B, reg_135B_cfg))
        time.sleep(0.2)
        read_data = CMD_batch_r_Query(REG_R_GPADC_IN)
        time.sleep(0.5)
        read_data_len = len(read_data)
        for cnt in range(math.trunc(read_data_len / 2)):
            gpadc_data_list.append(read_data[2 * cnt + 1])
        # 在此处将读出的GPADC数据计算为十进制数，放在每个序列的第四个，计算电压放在每个序列的第五个，后面有新增序列的话，前面表头要修改
        diff_mode_data_encode(data_list, gpadc_data_list, data_rows_cnt)
        data_rows_cnt += 1
    CMD_batch_w_Query(REG_W_1309_INIT)
    CMD_batch_w_Query(REG_W_12F3_INIT)
    CMD_batch_w_Query(CONFIG_REG_SOFT_FSM_RESET)
    time.sleep(0.5)

    # ########################## mux_sel：11 ##########################
    print('++++++++++++++++++++      MUX_SEL : 11 Test      ++++++++++++++++++++')
    CMD_batch_w_Query(REG_W_12F0_MUX_SINGLE)
    CMD_batch_w_Query(REG_W_1363_CFG)
    time.sleep(0.2)
    for reg_135B_cfg in range(11, 12):
        print('++++++++++++++++++++      MUX_SEL(0x135B) : ', reg_135B_cfg, ' Test      ++++++++++++++++++++')
        gpadc_data_list.append(reg_135B_cfg)
        # gpadc_data_list.append('0x%02X' % reg_135B_cfg)
        CMD_batch_w_Query(chip_reg.reg_write(0x135B, reg_135B_cfg))
        time.sleep(0.2)
        read_data = CMD_batch_r_Query(REG_R_GPADC_IN)
        time.sleep(0.1)
        read_data_len = len(read_data)
        for cnt in range(math.trunc(read_data_len / 2)):
            gpadc_data_list.append(read_data[2 * cnt + 1])
        # 在此处将读出的GPADC数据计算为十进制数，放在每个序列的第四个，计算电压放在每个序列的第五个，后面有新增序列的话，前面表头要修改
        single_mode_data_encode(data_list, gpadc_data_list, data_rows_cnt)
        data_rows_cnt += 1
    CMD_batch_w_Query(REG_W_1363_INIT)
    CMD_batch_w_Query(CONFIG_REG_SOFT_FSM_RESET)
    time.sleep(0.2)

    # ########################## mux_sel：12-32 ##########################
    CMD_batch_w_Query(REG_W_12F0_MUX_SINGLE)
    for reg_135B_cfg in range(12, 33):
        print('++++++++++++++++++++      MUX_SEL(0x135B) : ', reg_135B_cfg, ' Test      ++++++++++++++++++++')
        gpadc_data_list.append(reg_135B_cfg)
        # gpadc_data_list.append('0x%02X' % reg_135B_cfg)
        CMD_batch_w_Query(chip_reg.reg_write(0x135B, reg_135B_cfg))
        time.sleep(0.2)
        if reg_135B_cfg == 12:
            CMD_batch_w_Query(chip_reg.reg_write(0x1363, 0x01))
        elif reg_135B_cfg == 13:
            CMD_batch_w_Query(chip_reg.reg_write(0x1363, 0x02))
        elif reg_135B_cfg == 14:
            CMD_batch_w_Query(chip_reg.reg_write(0x1342, 0x10))
        elif reg_135B_cfg == 15:
            CMD_batch_w_Query(chip_reg.reg_write(0x1342, 0x04))
        elif reg_135B_cfg == 16:
            CMD_batch_w_Query(chip_reg.reg_write(0x1385, 0x01))
        elif reg_135B_cfg == 17:
            CMD_batch_w_Query(chip_reg.reg_write(0x1384, 0x01))
        elif reg_135B_cfg == 18:
            CMD_batch_w_Query(chip_reg.reg_write(0x1328, 0x01))
        elif reg_135B_cfg == 19:
            CMD_batch_w_Query(chip_reg.reg_write(0x132A, 0x01))
        elif reg_135B_cfg == 20:
            CMD_batch_w_Query(chip_reg.reg_write(0x1328, 0x02))
        elif reg_135B_cfg == 21:
            CMD_batch_w_Query(chip_reg.reg_write(0x132A, 0x02))
        elif reg_135B_cfg == 22:
            CMD_batch_w_Query(chip_reg.reg_write(0x1328, 0x04))
        elif reg_135B_cfg == 23:
            CMD_batch_w_Query(chip_reg.reg_write(0x132A, 0x04))
        elif reg_135B_cfg == 24:
            CMD_batch_w_Query(chip_reg.reg_write(0x130A, 0x01))
        elif reg_135B_cfg == 25:
            CMD_batch_w_Query(chip_reg.reg_write(0x130B, 0x01))
        elif reg_135B_cfg == 26:
            CMD_batch_w_Query(chip_reg.reg_write(0x130A, 0x02))
        elif reg_135B_cfg == 27:
            CMD_batch_w_Query(chip_reg.reg_write(0x130B, 0x02))
        elif reg_135B_cfg == 28:
            CMD_batch_w_Query(chip_reg.reg_write(0x130A, 0x04))
        elif reg_135B_cfg == 29:
            CMD_batch_w_Query(chip_reg.reg_write(0x130B, 0x04))
        elif reg_135B_cfg == 30:
            CMD_batch_w_Query(chip_reg.reg_write(0x130A, 0x08))
        elif reg_135B_cfg == 31:
            CMD_batch_w_Query(chip_reg.reg_write(0x130B, 0x08))
        elif reg_135B_cfg == 32:
            CMD_batch_w_Query(chip_reg.reg_write(0x133A, 0x01))

        CMD_batch_w_Query(chip_reg.reg_write(0x135B, reg_135B_cfg))
        time.sleep(0.2)
        read_data = CMD_batch_r_Query(REG_R_GPADC_IN)
        time.sleep(0.1)
        read_data_len = len(read_data)
        for cnt in range(math.trunc(read_data_len / 2)):
            gpadc_data_list.append(read_data[2 * cnt + 1])
        # 在此处将读出的GPADC数据计算为十进制数，放在每个序列的第四个，计算电压放在每个序列的第五个，后面有新增序列的话，前面表头要修改
        single_mode_data_encode(data_list, gpadc_data_list, data_rows_cnt)
        data_rows_cnt += 1

        if reg_135B_cfg == 12:
            CMD_batch_w_Query(chip_reg.reg_write(0x1363, 0x00))
        elif reg_135B_cfg == 13:
            CMD_batch_w_Query(chip_reg.reg_write(0x1363, 0x00))
        elif reg_135B_cfg == 14:
            CMD_batch_w_Query(chip_reg.reg_write(0x1342, 0x00))
        elif reg_135B_cfg == 15:
            CMD_batch_w_Query(chip_reg.reg_write(0x1342, 0x00))
        elif reg_135B_cfg == 16:
            CMD_batch_w_Query(chip_reg.reg_write(0x1385, 0x00))
        elif reg_135B_cfg == 17:
            CMD_batch_w_Query(chip_reg.reg_write(0x1384, 0x00))
        elif reg_135B_cfg == 18:
            CMD_batch_w_Query(chip_reg.reg_write(0x1328, 0x00))
        elif reg_135B_cfg == 19:
            CMD_batch_w_Query(chip_reg.reg_write(0x132A, 0x00))
        elif reg_135B_cfg == 20:
            CMD_batch_w_Query(chip_reg.reg_write(0x1328, 0x00))
        elif reg_135B_cfg == 21:
            CMD_batch_w_Query(chip_reg.reg_write(0x132A, 0x00))
        elif reg_135B_cfg == 22:
            CMD_batch_w_Query(chip_reg.reg_write(0x1328, 0x00))
        elif reg_135B_cfg == 23:
            CMD_batch_w_Query(chip_reg.reg_write(0x132A, 0x00))
        elif reg_135B_cfg == 24:
            CMD_batch_w_Query(chip_reg.reg_write(0x130A, 0x00))
        elif reg_135B_cfg == 25:
            CMD_batch_w_Query(chip_reg.reg_write(0x130B, 0x00))
        elif reg_135B_cfg == 26:
            CMD_batch_w_Query(chip_reg.reg_write(0x130A, 0x00))
        elif reg_135B_cfg == 27:
            CMD_batch_w_Query(chip_reg.reg_write(0x130B, 0x00))
        elif reg_135B_cfg == 28:
            CMD_batch_w_Query(chip_reg.reg_write(0x130A, 0x00))
        elif reg_135B_cfg == 29:
            CMD_batch_w_Query(chip_reg.reg_write(0x130B, 0x00))
        elif reg_135B_cfg == 30:
            CMD_batch_w_Query(chip_reg.reg_write(0x130A, 0x00))
        elif reg_135B_cfg == 31:
            CMD_batch_w_Query(chip_reg.reg_write(0x130B, 0x00))
        elif reg_135B_cfg == 32:
            CMD_batch_w_Query(chip_reg.reg_write(0x133A, 0x00))

        CMD_batch_w_Query(CONFIG_REG_SOFT_FSM_RESET)
        time.sleep(0.2)

    # ########################## mux_sel：15 遍历0x1344 ##########################
    # 测试 LFLDO 遍历0x1344：(0x20->0x27)
    data_title = ['0x1344(0x135B=15(LFLDO))', '0x00', '0x00']
    gpadc_data_list.append(data_title[0])
    gpadc_data_list.append(data_title[1])
    gpadc_data_list.append(data_title[2])
    # print('data_list : ', data_list)
    # print('gpadc_data_list : ', gpadc_data_list)
    # print('data_rows_cnt : ', data_rows_cnt)
    single_mode_data_encode(data_list, gpadc_data_list, data_rows_cnt)
    data_rows_cnt += 1
    CMD_batch_w_Query(REG_W_12F0_MUX_SINGLE)
    CMD_batch_w_Query(chip_reg.reg_write(0x1342, 0x04))
    CMD_batch_w_Query(chip_reg.reg_write(0x135B, 0x0F))
    for reg_1344_sel_cfg in range(8):
        print('++++++++++++++++++++      MUX_SEL(0x135B) : ', reg_135B_cfg, ' , 0x1302 : ',
              '0x%02X' % (0x20 | reg_1344_sel_cfg),
              ' Test      ++++++++++++++++++++')
        # print('++++++++++++++++++++      0x1344 : ', (0x20 | reg_1344_sel_cfg), ' Test      ++++++++++++++++++++')
        gpadc_data_list.append('0x%02X' % (0x20 | reg_1344_sel_cfg))
        CMD_batch_w_Query(chip_reg.reg_write(0x1344, (0x20 | reg_1344_sel_cfg)))
        time.sleep(0.2)
        read_data = CMD_batch_r_Query(REG_R_GPADC_IN)
        time.sleep(0.1)
        read_data_len = len(read_data)
        for cnt in range(math.trunc(read_data_len / 2)):
            gpadc_data_list.append(read_data[2 * cnt + 1])
        # 在此处将读出的GPADC数据计算为十进制数，放在每个序列的第四个，计算电压放在每个序列的第五个，后面有新增序列的话，前面表头要修改
        # print('gpadc_data_list:', gpadc_data_list)
        single_mode_data_encode(data_list, gpadc_data_list, data_rows_cnt)
        data_rows_cnt += 1
    CMD_batch_w_Query(chip_reg.reg_write(0x1342, 0x00))
    CMD_batch_w_Query(chip_reg.reg_write(0x1344, 0x23))
    CMD_batch_w_Query(CONFIG_REG_SOFT_FSM_RESET)
    time.sleep(0.2)
    data_title = ['0x1344 test end', '0x00', '0x00']
    gpadc_data_list.append(data_title[0])
    gpadc_data_list.append(data_title[1])
    gpadc_data_list.append(data_title[2])
    single_mode_data_encode(data_list, gpadc_data_list, data_rows_cnt)
    data_rows_cnt += 1

    # ########################## mux_sel：32 遍历0x133B ##########################
    # 测试 BIST 遍历0x133B：(0x00->0x07)
    data_title = ['0x133B(0x135B=32(BIST))', '0x00', '0x00']
    gpadc_data_list.append(data_title[0])
    gpadc_data_list.append(data_title[1])
    gpadc_data_list.append(data_title[2])
    single_mode_data_encode(data_list, gpadc_data_list, data_rows_cnt)
    data_rows_cnt += 1

    reg_135B_cfg = 0x20
    CMD_batch_w_Query(REG_W_12F0_MUX_SINGLE)
    CMD_batch_w_Query(chip_reg.reg_write(0x133A, 0x01))
    CMD_batch_w_Query(chip_reg.reg_write(0x135B, reg_135B_cfg))
    for reg_133B_sel_cfg in range(8):
        print('++++++++++++++++++++      MUX_SEL(0x135B) : ', reg_135B_cfg, ' , 0x1302 : ', '0x%02X' % reg_133B_sel_cfg,
              ' Test      ++++++++++++++++++++')
        # print('++++++++++++++++++++      0x133B : ', reg_133B_sel_cfg, ' Test      ++++++++++++++++++++')
        gpadc_data_list.append('0x%02X' % reg_133B_sel_cfg)
        CMD_batch_w_Query(chip_reg.reg_write(0x133B, reg_133B_sel_cfg))
        time.sleep(0.2)
        read_data = CMD_batch_r_Query(REG_R_GPADC_IN)
        time.sleep(0.1)
        read_data_len = len(read_data)
        for cnt in range(math.trunc(read_data_len / 2)):
            gpadc_data_list.append(read_data[2 * cnt + 1])
        # 在此处将读出的GPADC数据计算为十进制数，放在每个序列的第四个，计算电压放在每个序列的第五个，后面有新增序列的话，前面表头要修改
        # print('gpadc_data_list:', gpadc_data_list)
        single_mode_data_encode(data_list, gpadc_data_list, data_rows_cnt)
        data_rows_cnt += 1
    CMD_batch_w_Query(chip_reg.reg_write(0x133A, 0x00))
    CMD_batch_w_Query(chip_reg.reg_write(0x133B, 0x03))
    CMD_batch_w_Query(CONFIG_REG_SOFT_FSM_RESET)
    time.sleep(0.2)
    data_title = ['0x133B test end', '0x00', '0x00']
    gpadc_data_list.append(data_title[0])
    gpadc_data_list.append(data_title[1])
    gpadc_data_list.append(data_title[2])
    single_mode_data_encode(data_list, gpadc_data_list, data_rows_cnt)
    data_rows_cnt += 1

    # ########################## mux_sel：34-36 ##########################
    print('++++++++++++++++++++      MUX_SEL : 34-36 Test      ++++++++++++++++++++')
    CMD_batch_w_Query(REG_W_12F0_MUX_DIFF)
    CMD_batch_w_Query(REG_W_1327_CFG)
    CMD_batch_w_Query(REG_W_12F4_CFG)
    CMD_batch_w_Query(REG_W_132C_1330_CFG)
    time.sleep(0.5)
    for reg_135B_cfg in range(34, 37):
        print('++++++++++++++++++++      MUX_SEL(0x135B) : ', reg_135B_cfg, ' Test      ++++++++++++++++++++')
        gpadc_data_list.append(reg_135B_cfg)
        # gpadc_data_list.append('0x%02X' % reg_135B_cfg)
        CMD_batch_w_Query(chip_reg.reg_write(0x135B, reg_135B_cfg))
        time.sleep(0.2)
        read_data = CMD_batch_r_Query(REG_R_GPADC_IN)
        time.sleep(0.5)
        read_data_len = len(read_data)
        for cnt in range(math.trunc(read_data_len / 2)):
            gpadc_data_list.append(read_data[2 * cnt + 1])
        # 在此处将读出的GPADC数据计算为十进制数，放在每个序列的第四个，计算电压放在每个序列的第五个，后面有新增序列的话，前面表头要修改
        diff_mode_data_encode(data_list, gpadc_data_list, data_rows_cnt)
        data_rows_cnt += 1
    CMD_batch_w_Query(REG_W_1327_INIT)
    CMD_batch_w_Query(REG_W_12F4_INIT)
    CMD_batch_w_Query(CONFIG_REG_SOFT_FSM_RESET)
    time.sleep(0.5)

    # ########################## mux_sel：37-38 ##########################
    print('++++++++++++++++++++      MUX_SEL : 37-38 Test      ++++++++++++++++++++')
    CMD_batch_w_Query(REG_W_12F0_MUX_SINGLE)
    for reg_135B_cfg in range(37, 39):
        print('++++++++++++++++++++      MUX_SEL(0x135B) : ', reg_135B_cfg, ' Test      ++++++++++++++++++++')
        gpadc_data_list.append(reg_135B_cfg)
        # gpadc_data_list.append('0x%02X' % reg_135B_cfg)
        CMD_batch_w_Query(chip_reg.reg_write(0x135B, reg_135B_cfg))
        time.sleep(0.2)
        if reg_135B_cfg == 37:
            CMD_batch_w_Query(chip_reg.reg_write(0x2001, 0x95))
        elif reg_135B_cfg == 38:
            CMD_batch_w_Query(chip_reg.reg_write(0x1344, 0x63))
        time.sleep(0.2)
        read_data = CMD_batch_r_Query(REG_R_GPADC_IN)
        time.sleep(0.1)
        read_data_len = len(read_data)
        for cnt in range(math.trunc(read_data_len / 2)):
            gpadc_data_list.append(read_data[2 * cnt + 1])
        # 在此处将读出的GPADC数据计算为十进制数，放在每个序列的第四个，计算电压放在每个序列的第五个，后面有新增序列的话，前面表头要修改
        # print('gpadc_data_list:', gpadc_data_list)
        single_mode_data_encode(data_list, gpadc_data_list, data_rows_cnt)
        data_rows_cnt += 1

        if reg_135B_cfg == 37:
            CMD_batch_w_Query(chip_reg.reg_write(0x2001, 0x15))
        elif reg_135B_cfg == 38:
            CMD_batch_w_Query(chip_reg.reg_write(0x1344, 0x23))
        CMD_batch_w_Query(CONFIG_REG_SOFT_FSM_RESET)
        time.sleep(0.2)

    # ########################## mux_sel：39 遍历0x1302 ##########################
    # 测试 Rx_adc_atbout<1> 遍历0x1302：(0x01, 0x03, 0x05, 0x07)
    data_title = ['0x1302(0x135B=39(Rx_adc_atbout<1>))', '0x00', '0x00']
    gpadc_data_list.append(data_title[0])
    gpadc_data_list.append(data_title[1])
    gpadc_data_list.append(data_title[2])
    single_mode_data_encode(data_list, gpadc_data_list, data_rows_cnt)
    data_rows_cnt += 1
    CMD_batch_w_Query(REG_W_12F0_MUX_SINGLE)
    for reg_135B_cfg in range(39, 40):
        CMD_batch_w_Query(chip_reg.reg_write(0x135B, reg_135B_cfg))
        for reg_1302_cfg_value in (0x01, 0x03, 0x05, 0x07):
            print('++++++++++++++++++++      MUX_SEL(0x135B) : ', reg_135B_cfg, ' , 0x1302 : ', reg_1302_cfg_value,
                  ' Test      ++++++++++++++++++++')
            gpadc_data_list.append('0x%02X' % reg_1302_cfg_value)
            CMD_batch_w_Query(chip_reg.reg_write(0x1302, reg_1302_cfg_value))
            time.sleep(0.2)
            read_data = CMD_batch_r_Query(REG_R_GPADC_IN)
            time.sleep(0.1)
            read_data_len = len(read_data)
            for cnt in range(math.trunc(read_data_len / 2)):
                gpadc_data_list.append(read_data[2 * cnt + 1])
            # 在此处将读出的GPADC数据计算为十进制数，放在每个序列的第四个，计算电压放在每个序列的第五个，后面有新增序列的话，前面表头要修改
            # print('gpadc_data_list:', gpadc_data_list)
            single_mode_data_encode(data_list, gpadc_data_list, data_rows_cnt)
            data_rows_cnt += 1
        CMD_batch_w_Query(chip_reg.reg_write(0x1302, 0x00))
        CMD_batch_w_Query(CONFIG_REG_SOFT_FSM_RESET)
        time.sleep(0.2)

    # ########################## mux_sel：40-47 ##########################
    CMD_batch_w_Query(REG_W_12F0_MUX_SINGLE)
    for reg_135B_cfg in range(40, 48):
        print('++++++++++++++++++++      MUX_SEL(0x135B) : ', reg_135B_cfg, ' Test      ++++++++++++++++++++')
        gpadc_data_list.append(reg_135B_cfg)
        # gpadc_data_list.append('0x%02X' % reg_135B_cfg)
        CMD_batch_w_Query(chip_reg.reg_write(0x135B, reg_135B_cfg))
        time.sleep(0.2)
        if reg_135B_cfg == 40:
            CMD_batch_w_Query(chip_reg.reg_write(0x1384, 0x02))
        elif reg_135B_cfg == 41:
            CMD_batch_w_Query(chip_reg.reg_write(0x1385, 0x02))
        elif reg_135B_cfg == 42:
            CMD_batch_w_Query(chip_reg.reg_write(0x1342, 0x20))
        elif reg_135B_cfg == 43:
            CMD_batch_w_Query(chip_reg.reg_write(0x1342, 0x01))
        elif reg_135B_cfg == 44:
            CMD_batch_w_Query(chip_reg.reg_write(0x130A, 0x20))
        elif reg_135B_cfg == 45:
            CMD_batch_w_Query(chip_reg.reg_write(0x132A, 0x10))
        elif reg_135B_cfg == 46:
            CMD_batch_w_Query(chip_reg.reg_write(0x1328, 0x10))
        elif reg_135B_cfg == 47:
            CMD_batch_w_Query(chip_reg.reg_write(0x1342, 0x08))

        CMD_batch_w_Query(chip_reg.reg_write(0x135B, reg_135B_cfg))
        time.sleep(0.2)
        read_data = CMD_batch_r_Query(REG_R_GPADC_IN)
        time.sleep(0.1)
        read_data_len = len(read_data)
        for cnt in range(math.trunc(read_data_len / 2)):
            gpadc_data_list.append(read_data[2 * cnt + 1])
        # 在此处将读出的GPADC数据计算为十进制数，放在每个序列的第四个，计算电压放在每个序列的第五个，后面有新增序列的话，前面表头要修改
        single_mode_data_encode(data_list, gpadc_data_list, data_rows_cnt)
        data_rows_cnt += 1

        if reg_135B_cfg == 40:
            CMD_batch_w_Query(chip_reg.reg_write(0x1384, 0x00))
        elif reg_135B_cfg == 41:
            CMD_batch_w_Query(chip_reg.reg_write(0x1385, 0x00))
        elif reg_135B_cfg == 42:
            CMD_batch_w_Query(chip_reg.reg_write(0x1342, 0x00))
        elif reg_135B_cfg == 43:
            CMD_batch_w_Query(chip_reg.reg_write(0x1342, 0x00))
        elif reg_135B_cfg == 44:
            CMD_batch_w_Query(chip_reg.reg_write(0x130A, 0x00))
        elif reg_135B_cfg == 45:
            CMD_batch_w_Query(chip_reg.reg_write(0x132A, 0x00))
        elif reg_135B_cfg == 46:
            CMD_batch_w_Query(chip_reg.reg_write(0x1328, 0x00))
        elif reg_135B_cfg == 47:
            CMD_batch_w_Query(chip_reg.reg_write(0x1342, 0x00))

        CMD_batch_w_Query(CONFIG_REG_SOFT_FSM_RESET)
        time.sleep(0.2)

    # ########################## mux_sel：48-51 ##########################
    CMD_batch_w_Query(REG_W_12F0_MUX_DIFF)
    for reg_135B_cfg in range(48, 52):
        print('++++++++++++++++++++      MUX_SEL(0x135B) : ', reg_135B_cfg, ' Test      ++++++++++++++++++++')
        gpadc_data_list.append(reg_135B_cfg)
        # gpadc_data_list.append('0x%02X' % reg_135B_cfg)
        CMD_batch_w_Query(chip_reg.reg_write(0x135B, reg_135B_cfg))
        time.sleep(0.2)
        if reg_135B_cfg == 48:
            CMD_batch_w_Query(chip_reg.reg_write(0x1380, 0x20))
        elif reg_135B_cfg == 49:
            CMD_batch_w_Query(chip_reg.reg_write(0x1380, 0x40))
        elif reg_135B_cfg == 50:
            CMD_batch_w_Query(chip_reg.reg_write(0x1327, 0x0F))
        elif reg_135B_cfg == 51:
            # CMD_batch_w_Query(REG_W_1327_CFG)
            # CMD_batch_w_Query(REG_W_12F4_CFG)
            CMD_batch_w_Query(chip_reg.reg_write(0x1327, 0x10))
            CMD_batch_w_Query(chip_reg.reg_write(0x12F4, 0x78))
            CMD_batch_w_Query(REG_W_132C_1330_CFG)
            time.sleep(0.2)

        CMD_batch_w_Query(chip_reg.reg_write(0x135B, reg_135B_cfg))
        time.sleep(0.2)
        read_data = CMD_batch_r_Query(REG_R_GPADC_IN)
        time.sleep(0.1)
        read_data_len = len(read_data)
        for cnt in range(math.trunc(read_data_len / 2)):
            gpadc_data_list.append(read_data[2 * cnt + 1])
        # 在此处将读出的GPADC数据计算为十进制数，放在每个序列的第四个，计算电压放在每个序列的第五个，后面有新增序列的话，前面表头要修改
        diff_mode_data_encode(data_list, gpadc_data_list, data_rows_cnt)
        data_rows_cnt += 1

        if reg_135B_cfg == 48:
            CMD_batch_w_Query(chip_reg.reg_write(0x1380, 0x20))
        elif reg_135B_cfg == 49:
            CMD_batch_w_Query(chip_reg.reg_write(0x1380, 0x40))
        elif reg_135B_cfg == 50:
            CMD_batch_w_Query(chip_reg.reg_write(0x1327, 0x0F))
        elif reg_135B_cfg == 51:
            # CMD_batch_w_Query(REG_W_1327_INIT)
            # CMD_batch_w_Query(REG_W_12F4_INIT)
            CMD_batch_w_Query(chip_reg.reg_write(0x1327, 0x1F))
            CMD_batch_w_Query(chip_reg.reg_write(0x12F4, 0x08))

        CMD_batch_w_Query(CONFIG_REG_SOFT_FSM_RESET)
        time.sleep(0.2)

    # ########################## mux_sel：53 ##########################
    CMD_batch_w_Query(REG_W_12F0_MUX_DIFF)
    for reg_135B_cfg in range(53, 54):
        print('++++++++++++++++++++      MUX_SEL(0x135B) : ', reg_135B_cfg, ' Test      ++++++++++++++++++++')
        gpadc_data_list.append(reg_135B_cfg)
        # gpadc_data_list.append('0x%02X' % reg_135B_cfg)
        CMD_batch_w_Query(chip_reg.reg_write(0x135B, reg_135B_cfg))
        time.sleep(0.2)
        if reg_135B_cfg == 53:
            CMD_batch_w_Query(chip_reg.reg_write(0x12F3, 0x24))
            CMD_batch_w_Query(chip_reg.reg_write(0x1309, 0x01))
            # CMD_batch_w_Query(REG_W_12F3_CFG)
            # CMD_batch_w_Query(REG_W_1309_CFG)
            CMD_batch_w_Query(REG_W_130F_1310_CFG)
            time.sleep(0.2)

        CMD_batch_w_Query(chip_reg.reg_write(0x135B, reg_135B_cfg))
        time.sleep(0.2)
        read_data = CMD_batch_r_Query(REG_R_GPADC_IN)
        time.sleep(0.1)
        read_data_len = len(read_data)
        for cnt in range(math.trunc(read_data_len / 2)):
            gpadc_data_list.append(read_data[2 * cnt + 1])
        # 在此处将读出的GPADC数据计算为十进制数，放在每个序列的第四个，计算电压放在每个序列的第五个，后面有新增序列的话，前面表头要修改
        diff_mode_data_encode(data_list, gpadc_data_list, data_rows_cnt)
        data_rows_cnt += 1

        if reg_135B_cfg == 53:
            # CMD_batch_w_Query(REG_W_1309_INIT)
            # CMD_batch_w_Query(REG_W_12F3_INIT)
            CMD_batch_w_Query(chip_reg.reg_write(0x12F3, 0x20))
            CMD_batch_w_Query(chip_reg.reg_write(0x1309, 0x03))

        CMD_batch_w_Query(CONFIG_REG_SOFT_FSM_RESET)
        time.sleep(0.2)

    # ########################## mux_sel：54-55 ##########################
    print('++++++++++++++++++++      MUX_SEL : 54-55 Test      ++++++++++++++++++++')
    CMD_batch_w_Query(REG_W_12F0_MUX_DIFF)
    CMD_batch_w_Query(chip_reg.reg_write(0x1327, 0x10))
    CMD_batch_w_Query(chip_reg.reg_write(0x12F4, 0x78))
    # CMD_batch_w_Query(REG_W_1327_CFG)
    # CMD_batch_w_Query(REG_W_12F4_CFG)
    CMD_batch_w_Query(REG_W_132C_1330_CFG)
    time.sleep(0.5)
    for reg_135B_cfg in range(54, 56):
        print('++++++++++++++++++++      MUX_SEL(0x135B) : ', reg_135B_cfg, ' Test      ++++++++++++++++++++')
        gpadc_data_list.append(reg_135B_cfg)
        # gpadc_data_list.append('0x%02X' % reg_135B_cfg)
        CMD_batch_w_Query(chip_reg.reg_write(0x135B, reg_135B_cfg))
        time.sleep(0.2)
        read_data = CMD_batch_r_Query(REG_R_GPADC_IN)
        time.sleep(0.5)
        read_data_len = len(read_data)
        for cnt in range(math.trunc(read_data_len / 2)):
            gpadc_data_list.append(read_data[2 * cnt + 1])
        # 在此处将读出的GPADC数据计算为十进制数，放在每个序列的第四个，计算电压放在每个序列的第五个，后面有新增序列的话，前面表头要修改
        diff_mode_data_encode(data_list, gpadc_data_list, data_rows_cnt)
        data_rows_cnt += 1

    CMD_batch_w_Query(chip_reg.reg_write(0x1327, 0x1F))
    CMD_batch_w_Query(chip_reg.reg_write(0x12F4, 0x08))
    # CMD_batch_w_Query(REG_W_1327_INIT)
    # CMD_batch_w_Query(REG_W_12F4_INIT)
    CMD_batch_w_Query(CONFIG_REG_SOFT_FSM_RESET)
    time.sleep(0.5)

    # ########################## mux_sel：56-59 ##########################
    print('++++++++++++++++++++      MUX_SEL : 56-59 Test      ++++++++++++++++++++')
    CMD_batch_w_Query(REG_W_12F0_MUX_SINGLE)
    CMD_batch_w_Query(chip_reg.reg_write(0x12F5, 0x41))  # 会改变reg 0x1345的初始值
    # CMD_batch_w_Query(REG_W_12F5_CFG1)  # 会改变reg 0x1345的初始值
    CMD_batch_w_Query(REG_W_1341_1342_CFG1)
    for reg_135B_cfg in range(56, 60):
        print('++++++++++++++++++++      MUX_SEL(0x135B) : ', reg_135B_cfg, ' Test      ++++++++++++++++++++')
        gpadc_data_list.append(reg_135B_cfg)
        CMD_batch_w_Query(chip_reg.reg_write(0x135B, reg_135B_cfg))
        time.sleep(0.2)
        read_data = CMD_batch_r_Query(REG_R_GPADC_IN)
        time.sleep(0.5)
        read_data_len = len(read_data)
        for cnt in range(math.trunc(read_data_len / 2)):
            gpadc_data_list.append(read_data[2 * cnt + 1])
        # 在此处将读出的GPADC数据计算为十进制数，放在每个序列的第四个，计算电压放在每个序列的第五个，后面有新增序列的话，前面表头要修改
        single_mode_data_encode(data_list, gpadc_data_list, data_rows_cnt)
        data_rows_cnt += 1

    CMD_batch_w_Query(REG_W_1341_1342_INIT)
    # CMD_batch_w_Query(REG_W_12F5_INIT)
    CMD_batch_w_Query(chip_reg.reg_write(0x12F5, 0x01))
    # CMD_batch_w_Query(REG_W_12F4_INIT)
    CMD_batch_w_Query(CONFIG_REG_SOFT_FSM_RESET)
    time.sleep(0.5)

    # ########################## mux_sel：60,61,63 ##########################
    print('++++++++++++++++++++      MUX_SEL : 60,61,63 Test      ++++++++++++++++++++')
    CMD_batch_w_Query(REG_W_12F0_MUX_SINGLE)
    for reg_135B_cfg in (60, 61, 63):
        print('++++++++++++++++++++      MUX_SEL(0x135B) : ', reg_135B_cfg, ' Test      ++++++++++++++++++++')
        gpadc_data_list.append(reg_135B_cfg)
        CMD_batch_w_Query(chip_reg.reg_write(0x135B, reg_135B_cfg))
        time.sleep(0.2)
        read_data = CMD_batch_r_Query(REG_R_GPADC_IN)
        time.sleep(0.5)
        read_data_len = len(read_data)
        for cnt in range(math.trunc(read_data_len / 2)):
            gpadc_data_list.append(read_data[2 * cnt + 1])
        # 在此处将读出的GPADC数据计算为十进制数，放在每个序列的第四个，计算电压放在每个序列的第五个，后面有新增序列的话，前面表头要修改
        single_mode_data_encode(data_list, gpadc_data_list, data_rows_cnt)
        data_rows_cnt += 1

        CMD_batch_w_Query(CONFIG_REG_SOFT_FSM_RESET)
        time.sleep(0.5)

    # ########################## mux_sel：62 遍历0x2050 ##########################
    data_title = ['0x2050(0x135B=62)', '0x00', '0x00']
    gpadc_data_list.append(data_title[0])
    gpadc_data_list.append(data_title[1])
    gpadc_data_list.append(data_title[2])
    single_mode_data_encode(data_list, gpadc_data_list, data_rows_cnt)
    data_rows_cnt += 1
    CMD_batch_w_Query(REG_W_12F0_MUX_SINGLE)

    for reg_135B_cfg in range(62, 63):
        CMD_batch_w_Query(chip_reg.reg_write(0x135B, reg_135B_cfg))
        for reg_2050_cfg_value in (0x9C, 0x9D, 0x9E, 0x9F):
            print('++++++++++++++++++++      MUX_SEL(0x135B) : ', reg_135B_cfg, ' , 0x1302 : ', reg_1302_cfg_value,
                  ' Test      ++++++++++++++++++++')
            gpadc_data_list.append('0x%02X' % reg_2050_cfg_value)
            CMD_batch_w_Query(chip_reg.reg_write(0x2050, reg_2050_cfg_value))
            time.sleep(0.2)
            read_data = CMD_batch_r_Query(REG_R_GPADC_IN)
            time.sleep(0.1)
            read_data_len = len(read_data)
            for cnt in range(math.trunc(read_data_len / 2)):
                gpadc_data_list.append(read_data[2 * cnt + 1])
            # 在此处将读出的GPADC数据计算为十进制数，放在每个序列的第四个，计算电压放在每个序列的第五个，后面有新增序列的话，前面表头要修改
            single_mode_data_encode(data_list, gpadc_data_list, data_rows_cnt)
            data_rows_cnt += 1
        CMD_batch_w_Query(chip_reg.reg_write(0x2050, 0x98))
        CMD_batch_w_Query(CONFIG_REG_SOFT_FSM_RESET)
        time.sleep(0.2)
    # print('gpadc_data_list : ', gpadc_data_list)
    # print('data_list : ', data_list)

    if 1:
        # 换行打印测试数据
        print('p_data_list :')
        p_data_list = data_list
        p_data_len = math.trunc(len(p_data_list))
        p_data_len_end = len(p_data_list) % 20
        for p_cnt in range(math.trunc(p_data_len / 20)):
            print(p_data_list[20 * p_cnt:20 * p_cnt + 20])
        print(p_data_list[p_data_len - p_data_len_end:p_data_len], '\n')

    # return gpadc_data_list
    # return dat_list
    return data_list

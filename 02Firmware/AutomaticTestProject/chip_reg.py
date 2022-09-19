"""

#寄存器初始配置

"""


# class Reg:
#     """
#     # 重新校准
#     """
#
#     reg_SPI_CTRL_addr = ([0x00, 0x01])
#     reg_SPI_CTRL_value = ([0x02])
#     reg_SPI_CTRL = (reg_SPI_CTRL_addr + reg_SPI_CTRL_value)
#     # reg_SPI_CTRL = ([0x00, 0x01, 0x02])
#
#     """
#     # Freq config
#     """
#
#     reg_CP1_CTRL0_addr = ([0x10, 0x40])
#     reg_CP1_CTRL0_value = ([0x00])
#     reg_CP1_CTRL0 = (reg_CP1_CTRL0_addr + reg_CP1_CTRL0_value)
#     # reg_CP1_CTRL0 = ([0x10, 0x40, 0x00])
#
#     reg_CP1_CTRL1 = ([0x10, 0x41, 0x00])
#     reg_CP1_CTRL2 = ([0x10, 0x42, 0x86])
#     reg_CP1_CTRL3 = ([0x10, 0x43, 0x00])
#     reg_CP1_CTRL4 = ([0x10, 0x44, 0x00])
#
#     reg_CSAMODE0 = ([0x12, 0xF0, 0xA8])
#
#     reg_FLAG0 = ([0x12, 0xF3, 0x20])
#     reg_FLAG1 = ([0x12, 0xF5, 0x04])
#
#     """
#     # PLL BW
#     # 1:600K PLL BW 1347&1348 3F, 1349&134A 1F
#     # 2:300K PLL BW 1347&1348 67, 1349&134A 07
#     # 3:200K PLL BW 1347&1348 45, 1349&1349 05
#     # 4:150K PLL BW 1347&1348 E1, 1349&134A 01
#     """
#     reg_FMCW0 = ([0x13, 0x47, 0x67])
#     reg_FMCW1 = ([0x13, 0x48, 0x67])
#     reg_FMCW2 = ([0x13, 0x49, 0x07])
#     reg_FMCW3 = ([0x13, 0x4A, 0x07])
#
#     reg_LODIST = ([0x13, 0x82, 0x09])
#     reg_CAL = ([0x13, 0xB2, 0x00])
#
# def REG_W_CFG(addr_h=None, addr_l=None, val=None):
#     Value = [addr_h, addr_l, val]
#     return Value


def REG_W_0x1363(val=None):
    Value = [0x13, 0x63, val]
    return Value


def REG_W_0x1342(val=None):
    Value = [0x13, 0x42, val]
    return Value


# def REG_W(val=None):
#     print('val : ', val)
#     addr_h = int(str(val)[:2], 16)
#     addr_l = int(str(val)[2:4], 16)
#     # addr_l = int(val[2:4], 16)
#     Value = [0x13, 0x42, val]
#     print('addr_h : ', '0x%02X' % addr_h)
#     print('addr_l : ', '0x%02X' % addr_l)
#     print('Value : ', Value)
#     return Value


def reg_write(addr=None, val=None):
    # print('addr : ', '0x%02X' % addr)
    # print('val : ', '0x%02X' % val)
    addr_h = addr >> 8
    addr_l = addr & 0xFF
    Value = [addr_h, addr_l, val]
    # print('addr_h : ', '0x%02X' % addr_h)
    # print('addr_l : ', '0x%02X' % addr_l)
    # print('Value : ', Value)
    return Value

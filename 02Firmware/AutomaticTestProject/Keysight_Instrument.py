import time
import pyvisa
# import pandas as pd

# from com_connect import PWR_Supply_E3632A_COM_cfg, PWR_Supply_E36311A_COM_cfg

PXA_N9030B_IP = 'TCPIP0::169.254.151.186::inst0::INSTR'  # N9030B
E36311A_ADDR = 'USB0::0x2A8D::0x1002::MY61002092::0::INSTR'  # E36311A
rm = pyvisa.ResourceManager()
rm.list_resources()
PXA_N9030B = rm.open_resource(PXA_N9030B_IP)
PS_E36311A = rm.open_resource(E36311A_ADDR)
# print(rm.list_resources())
# print(PXA_N9030B.query('*IDN?'))
# print(PS_E36311A.query('*IDN?'))

# def SA_config():
#     rm = pyvisa.ResourceManager()
#     rm.list_resources()
#     PXA_N9030B = rm.open_resource(PXA_N9030B_IP)
#     print(PXA_N9030B.query('*IDN?'))

# def PXA_connect():
#     # Init_PXA_N9030B()
#     # 配置PXA_N9030B
#     rm = pyvisa.ResourceManager()
#     # rm.list_resources()
#     PXA_N9030B = rm.open_resource(PXA_N9030B_IP)
#     print(PXA_N9030B.query('*IDN?'))


def PS_E3632A_on():
    # PWR_Supply_E3632A_COM_cfg.write(
    #     [0x4F, 0x55, 0x54, 0x70, 0x75, 0x74, 0x20, 0x4F, 0x4E, 0x0A])  # OUTput ON 电源output on
    time.sleep(2)


def PS_E3632A_off():
    # PWR_Supply_E3632A_COM_cfg.write(
    #     [0x4F, 0x55, 0x54, 0x70, 0x75, 0x74, 0x20, 0x4F, 0x46, 0x46, 0x0A])  # OUTput OFF电源output off
    time.sleep(0.2)


def PS_E36311A_init_cfg():
    PS_E36311A.write('*RST')  # RST page55
    time.sleep(0.2)
    # PS_E36311A.write('INST P6V')    # 选择通道CH1 page59
    PS_E36311A.write('INST CH1')    # 选择通道CH1 page59
    PS_E36311A.write('SOUR:VOLT 5;CURR 2')  # 配置选择通道的电压电流
    time.sleep(0.1)
    PS_E36311A.write('INST P25V')    # 选择通道CH2 page59
    # PS_E36311A.write('INST CH2')    # 选择通道CH2 page59
    PS_E36311A.write('SOUR:VOLT 5;CURR 1')
    time.sleep(0.1)
    PS_E36311A.write('INST N25V')  # 选择通道CH3 page59
    # PS_E36311A.write('INST CH3')    # 选择通道CH3 page59
    PS_E36311A.write('SOUR:VOLT -5;CURR 1')
    time.sleep(0.1)
    print('Power Supply E36311A init complete')


def PS_E36311A_on():
    # PS_E36311A.write('INST:NSEL 1')  # 选择通道CH1 page
    PS_E36311A.write('INST CH1')  # 选择通道CH1 page59
    PS_E36311A.write('OUTP ON')  # CH1 ON page59
    # PS_E36311A.write('INIT:CONT ON')   # page58
    time.sleep(2)


def PS_E36311A_off():
    PS_E36311A.write('INST CH1')  # 选择通道CH1 page59
    PS_E36311A.write('OUTP OFF')  # CH1 ON page59
    # PS_E36311A.write('INIT:CONT OFF')
    time.sleep(0.5)


def PS_E36311A_read_volt_curr():
    # ps_vc_value = []
    volt_value = PS_E36311A.query('MEAS:VOLT? CH1')   # 读取输出电压 page68
    # ps_vc_value.append(volt_value)

    curr_value = PS_E36311A.query('MEAS:CURR? CH1')   # 读取输出电流 page68
    # ps_vc_value.append(curr_value)

    ps_vc_value = [volt_value[:-1], curr_value[:-1]]  # 去掉数据中的\n
    # print(PS_E36311A.query('MEAS:VOLT? CH1'))   # 读取输出电压 page68
    # print(PS_E36311A.query('MEAS:CURR? CH1'))   # 读取输出电流 page68

    print(' CH1 volt_value:', volt_value, 'CH1 curr_value:', curr_value)   # 打印输出电压电流 page68
    # print('CH1 volt_value:', volt_value)   # 打印输出电压 page68
    # print('CH1 curr_value:', curr_value)   # 打印输出电流 page68
    # print('CH1 ps_vc_value:', ps_vc_value)

    return ps_vc_value


def KsInstr_PN_Test():
    # PXA_N9030B.open()
    # 此函数中备注的page 'x' 为文件 Phase Noise Mode User's & Programmer's Reference.pdf 中的页数
    # PXA_N9030B.write(':INST:SCR:DEL:ALL')  # 删除所有窗口(Screen)
    # PXA_N9030B.write(':INST:SCR:CRE')  # 新增一个窗口(Screen) 指令1   page66
    # PXA_N9030B.write(':INSTrument:SCReen:CREate')  # 新增一个窗口(Screen) 指令2   page186
    # PXA_N9030B.write(':INST:SCR:DEL')  # 删除一个窗口(Screen)   page64

    PXA_N9030B.write(':INST:SCR:MULT OFF')  # 关闭多窗口显示   page115
    PXA_N9030B.write(':SYST:SEQ OFF')  # 只有一个窗口处于活动 ON 所有窗口顺序处于活动状态 page60

    # print(PXA_N9030B.query(':INST:SCR:CAT?'))  # 查询已打开的窗口(Screen list)  page117
    inst_screen_list = PXA_N9030B.query(':INST:SCR:CAT?')  # 查询已打开的窗口(Screen list)  page117
    # print(inst_screen_list)
    # PN_SCR_name = "PN Test1"
    # if "PN Test1" not in inst_screen_list:
    if "PN Test" not in inst_screen_list:
        print('没有名称为”PN Test“的窗口，新建”PN Test“窗口')
        PXA_N9030B.write(':INST:SCR:CRE')  # 新增一个窗口(Screen) 指令1   page66
        PXA_N9030B.write(':INST:SCR:REN "PN Test"')  # 修改窗口名称   page63
        time.sleep(1)
        PXA_N9030B.write(':INST:CONF:PNOISE:LPLot')  # 测试模式mode：Phase Noise  meas：Log Plot  page51
        PXA_N9030B.write(':FREQ:CARR 20 GHz')  # Carrier Frequency 设置为20GHz  page287

        PXA_N9030B.write(':DISP:LPL:WIND:TRAC:Y:RLEV -30')  # Ref Value    page238
        # print(PXA_N9030B.query(':DISP:LPL:WIND:TRAC:Y:RLEV?'))  # Ref Value    page238
        PXA_N9030B.write(':DISP:LPL:WIND:TRAC:Y:PDIV 10')  # Scale/Div    page238

        PXA_N9030B.write(':POW:ATT 6')  # Mech Atten  Mechanical attenuator    page243

        PXA_N9030B.write(':DISP:LPL:VIEW NORM')  # View Selection  Normal|Decade Table|Spurious Table  page279
        # PXA_N9030B.write(':DISP:LPL:VIEW DEC')  # View Selection  Normal|Decade Table|Spurious Table  page279

        PXA_N9030B.write(':DISP:ANN:SCR ON')  # 打开屏幕注释     page284
        PXA_N9030B.write(':DISP:ANN:MBAR ON')  # 打开顶部测量栏     page285

        PXA_N9030B.write(':LPL:FREQ:OFFS:STAR 1kHz')  # Freq Start offset 设置为1kHz   page288
        PXA_N9030B.write(':LPL:FREQ:OFFS:STOP 10MHz')  # Freq Stop offset 设置为10MHz  page289

        PXA_N9030B.write(':LPL:AVER ON')  # Averaging ON    page306
        PXA_N9030B.write(':LPL:AVER:COUN 5')  # Avg|Hold Num 设置为5次  page306
        PXA_N9030B.write(':LPL:AVER:TCON REP')  # Average Mode:Repeat  page307
        PXA_N9030B.write(':LPL:METH PN')  # Meas Type:Phase Noise  page309
        PXA_N9030B.write(':LPL:SMO 4')  # Smoothing:4%  page309

        PXA_N9030B.write(':INIT:CONT OFF')  # Sweep/Measure:single  page326
        time.sleep(2)
    else:
        pass

    # PXA_N9030B.write(':LPL:AVER ON')  # Averaging ON    page306
    # PXA_N9030B.write(':LPL:AVER:COUN 5')  # Avg|Hold Num 设置为5次  page306
    # PXA_N9030B.write(':CALC:LPL:DEC:TABL ON')  # Decade Table  page235

    # PXA_N9030B.write(':INST:SCR:SEL "Phase Noise 1"')  # 选择活动窗口 page116
    PXA_N9030B.write(':INST:SCR:SEL "PN Test"')  # 选择活动窗口 page116
    # PXA_N9030B.write(':INST:CONF:PNOISE:LPLot')  # 测试模式mode：Phase Noise  meas：Log Plot  page51
    # PXA_N9030B.write(':INST:SEL PNOISE')  # mode：Phase Noise   # 选择Phase Noise测试模式
    # PXA_N9030B.write(':INST PNOISE') # mode：Phase Noise   # 选择Phase Noise测试模式

    PXA_N9030B.write(':CALC:LPL:MARK1:MODE POS')  # Mark1点设置为Position 模式    page294
    PXA_N9030B.write(':CALC:LPL:MARK1:X 1000kHz')  # Mark1点设置为1MHz    page292

    time.sleep(0.1)

    # print(PXA_N9030B.query(''))
    time.sleep(0.1)
    PXA_N9030B.write(':FREQ:CARR:SEAR')  # Auto tune  自动调整  page288
    # PXA_N9030B.write(':INIT:REST')  # Restart  page328
    time.sleep(10)
    # print(PXA_N9030B.query(':FREQ:CARR?'))
    # print(PXA_N9030B.query(':CALC:LPL:MARK1:X?'))
    # print(PXA_N9030B.query(':CALC:LPL:MARK1:Y?'))
    Frequency = PXA_N9030B.query(':FREQ:CARR?')
    Amplitude = PXA_N9030B.query(':CALC:LPL:MARK1:Y?')
    PN_Mark_Freq = PXA_N9030B.query(':CALC:LPL:MARK1:X?')

    time.sleep(0.1)
    print(' Frequency(Hz):', Frequency, 'PN_Mark_Freq(Hz):', PN_Mark_Freq, 'Amplitude(dBm):', Amplitude)
    # print(Amplitude)
    # print(Frequency)
    # print(PN_Mark_Freq)

    Freq_Amp_data = [Frequency[:-1], Amplitude[:-1]]  # 去掉数据中的\n
    # print('Freq_Amp_data:', Freq_Amp_data)
    return Freq_Amp_data
    # PXA_N9030B.close()
    # time.sleep(5)
    # PXA_N9030B.write(':INST:SCR:DEL')  # 删除一个窗口(Screen)   page64


def KsInstr_Freq_Test():
    # 此函数中备注的page 'x' 为文件 Spectrum Analyzer Mode User's & Programmer's Reference.pdf 中的页数
    PXA_N9030B.write(':INST:SCR:MULT OFF')  # 关闭多窗口显示   page158
    PXA_N9030B.write(':SYST:SEQ OFF')  # 只有一个窗口处于活动 ON 所有窗口顺序处于活动状态 page96

    inst_screen_list = PXA_N9030B.query(':INST:SCR:CAT?')  # 查询已打开的窗口(Screen list)  page159
    if "Freq Test" not in inst_screen_list:
        print('没有名称为”Freq Test“的窗口，新建”Freq Test“窗口')
        PXA_N9030B.write(':INST:SCR:CRE')  # 新增一个窗口(Screen) 指令1   page102
        PXA_N9030B.write(':INST:SCR:REN "Freq Test"')  # 修改窗口名称   page100
        time.sleep(0.2)
        PXA_N9030B.write(':INST:CONF:SA:SAN')  # Mode：Spectrum Analyzer  meas：Swept SA  page87
        # PXA_N9030B.write(':CONF:SAN:NDEF')  # Mode：Spectrum Analyzer  meas：Swept SA  page182
        PXA_N9030B.write(':CONFigure:SANalyzer')  # Mode：Spectrum Analyzer  meas：Swept SA  page182

        PXA_N9030B.write(':DISP:VIEW NORM')  # View Selection  Normal|TZOom|SPECtrogram|ZSPan  page184

        # PXA_N9030B.write(':POW:ATT 20')  # Mech Atten  Mechanical attenuator    page214
        PXA_N9030B.write(':POW:ATT:AUTO ON')  # Mech Atten  Mechanical attenuator    page214
        PXA_N9030B.write(':DISP:WIND:TRAC:Y:RLEV 10')  # Ref Value    page201
        PXA_N9030B.write(':DISP:WIND:TRAC:Y:PDIV 10')  # Scale/Div    page203
        PXA_N9030B.write(':DISP:WIND:TRAC:Y:SPAC LOG')  # Display Scale ： LOG    page203
        PXA_N9030B.write(':UNIT:POW DBM')  # Y Axis Unit : dBm    page203

        # PXA_N9030B.write(':DISP:WIND:TRAC:Y:RLEV:OFFS:STAT ON')  # Reference Level Offset : ON    page209
        # PXA_N9030B.write(':DISP:WIND:TRAC:Y:RLEV:OFFS 0')  # Reference Level Offset : 0dBm    page209
        # PXA_N9030B.write(':DISP:WIND:TRAC:Y:NDIV 10')  # Number of Divisions : 6-20 对应(6-20)*PDIV的功率范围    page210
        PXA_N9030B.write(':BWID:AUTO ON')  # Res BW    page244
        PXA_N9030B.write(':BWID:VID:AUTO ON')  # Video BW    page247
        PXA_N9030B.write(':BAND:VID:RAT:AUTO ON')  # VBW:3dB RBW   page248
        PXA_N9030B.write(':FREQ:SPAN:BAND:RAT:AUTO ON')  # Span:3dB RBW   page249

        PXA_N9030B.write(':DISP:ANN:SCR ON')  # 打开屏幕注释  default：ON     page272
        PXA_N9030B.write(':DISP:ANN:MBAR ON')  # 打开顶部测量栏    default：ON     page273

        # PXA_N9030B.write(':FREQ:CENT 19 GHz')  # Center Frequency 设置为18GHz  page280
        # # PXA_N9030B.write(':FREQ:RF:CENT 20 GHz')  # Center Frequency 设置为20GHz  page280
        # PXA_N9030B.write(':FREQ:SPAN 6GHz')  # Span 设置为5GHz  page280
        PXA_N9030B.write(':FREQ:STAR 16GHz')  # Freq Start 设置为16GHz   page290
        PXA_N9030B.write(':FREQ:STOP 22GHz')  # Freq Stop 设置为22GHz  page292
        time.sleep(0.2)

    else:
        pass
    PXA_N9030B.write(':INST:SCR:SEL "Freq Test"')  # 选择活动窗口 page158
    # PXA_N9030B.write(':INST:CONF:SA:SAN')  # Mode：Spectrum Analyzer  meas：Swept SA  page87
    # PXA_N9030B.write(':CONF:SAN:NDEF')  # Mode：Spectrum Analyzer  meas：Swept SA  page182 X
    # PXA_N9030B.write(':CONFigure:SANalyzer')  # Mode：Spectrum Analyzer  meas：Swept SA  page182
    time.sleep(0.1)
    PXA_N9030B.write(':DISP:WIND:TRAC:Y:RLEV 0')  # Ref Value    page201
    PXA_N9030B.write(':FREQ:STAR 16GHz')  # Freq Start 设置为16GHz   page290
    PXA_N9030B.write(':FREQ:STOP 22GHz')  # Freq Stop 设置为22GHz  page292
    time.sleep(0.1)
    PXA_N9030B.write(':CALC:MARK1:MODE POS')  # Mark1点设置为Position   default：POS page313
    # PXA_N9030B.write(':CALC:MARK1:X 20GHz')  # Mark1点设置为20GHz    page308
    PXA_N9030B.write(':CALC:MARK:TABL OFF')  # Marker Table         default：OFF page316
    time.sleep(0.1)
    PXA_N9030B.write(':FREQ:TUNE:IMM')  # Auto Tune  page294
    time.sleep(6)  # 等待仪器调整结束
    PXA_N9030B.write(':DISP:WIND:TRAC:Y:RLEV 0')  # Ref Value    page201
    PXA_N9030B.write(':FREQ:SPAN 100MHz')  # Span 设置为100MHz  page280
    time.sleep(0.1)
    # PXA_N9030B.write(':INIT:CONT OFF')  # Sweep/Measure:single    default：ON  page485
    PXA_N9030B.write(':INIT:CONT ON')  # Sweep/Measure:continuous   default：ON  page485
    PXA_N9030B.write(':AVER:COUN 100')  # Avg|Hold Num 设置为100次   default：100  page384
    PXA_N9030B.write(':TRAC:TYPE AVER')  # Trace Type ： Average page513
    time.sleep(2)
    PXA_N9030B.write(':CALC:MARK:PEAK:THR -50 dBm')  # Peak Threshold  page325
    PXA_N9030B.write(':CALC:MARK:PEAK:SEAR:MODE MAX')  # Peak Search Mode  page329
    # PXA_N9030B.write(':CALC:MARK1:MAX')  # Peak Search  page319
    PXA_N9030B.write(':CALC:MARK:CPS ON')  # Continuous Peak Search  page372
    time.sleep(0.1)
    PXA_N9030B.write(':CALC:MARK1:CENT')  # Mkr->CF  page319

    # PXA_N9030B.write(':AVER:CLE')  # page384
    # PXA_N9030B.write(':TRAC:TYPE WRIT')  # page384
    # PXA_N9030B.write(':TRAC:TYPE AVER')  # page384

    time.sleep(2)
    time.sleep(0.1)

    Amplitude = PXA_N9030B.query(':CALC:MARK1:Y?')  # Marker Amplitude page310
    Frequency = PXA_N9030B.query(':CALC:MARK1:X?')  # Marker Frequency page308/319
    print(' Amplitude(dBm):', Amplitude, 'Frequency(Hz):', Frequency)
    # print(Amplitude)
    # print(Frequency)
    Freq_Amp_data = [Frequency[:-1], Amplitude[:-1]]  # 去掉数据中的\n
    # print('Amp_Freq_list:', Amp_Freq_data)

    # x = [float(Amplitude[:-1]), float(Frequency[:-1])]    # string 变成 float型，并去掉数据中的\n
    # print('x:', x)
    # print(PXA_N9030B.query(':CALC:MARK1:Y?'))  # Marker Amplitude page310
    # print(PXA_N9030B.query(':CALC:MARK1:X?'))  # Marker Frequency page308/319
    # print(PXA_N9030B.query(':SYST:ERR?'))  # 打印系统错误信息  page124
    # time.sleep(0.1)
    return Freq_Amp_data
    # time.sleep(2)
    # PXA_N9030B.write(':INIT:REST')  # Restart  page489 比IMM重启范围广
    # PXA_N9030B.write(':INIT:IMM')  # Restart  page489

    # time.sleep(10000)
    # PXA_N9030B.close()
    # time.sleep(5)
    # PXA_N9030B.write(':INST:SCR:DEL')  # 删除一个窗口(Screen)   page64


def KsInstr_Power_Test():
    PXA_N9030B.open()
    # 此函数中备注的page 'x' 为文件 Spectrum Analyzer Mode User's & Programmer's Reference.pdf 中的页数
    PXA_N9030B.write(':INST:SCR:MULT OFF')  # 关闭多窗口显示   page158
    PXA_N9030B.write(':SYST:SEQ OFF')  # 只有一个窗口处于活动 ON 所有窗口顺序处于活动状态 page96

    inst_screen_list = PXA_N9030B.query(':INST:SCR:CAT?')  # 查询已打开的窗口(Screen list)  page159
    if "Power Test" not in inst_screen_list:
        print('没有名称为”Power Test“的窗口，新建”Power Test“窗口')
        PXA_N9030B.write(':INST:SCR:CRE')  # 新增一个窗口(Screen) 指令1   page102
        PXA_N9030B.write(':INST:SCR:REN "Power Test"')  # 修改窗口名称   page100
        time.sleep(1)
        PXA_N9030B.write(':INST:CONF:SA:SAN')  # Mode：Spectrum Analyzer  meas：Swept SA  page87
        # PXA_N9030B.write(':CONF:SAN:NDEF')  # Mode：Spectrum Analyzer  meas：Swept SA  page182
        PXA_N9030B.write(':CONFigure:SANalyzer')  # Mode：Spectrum Analyzer  meas：Swept SA  page182

        PXA_N9030B.write(':DISP:VIEW NORM')  # View Selection  Normal|TZOom|SPECtrogram|ZSPan  page184

        # PXA_N9030B.write(':POW:ATT 20')  # Mech Atten  Mechanical attenuator    page214
        PXA_N9030B.write(':POW:ATT:AUTO ON')  # Mech Atten  Mechanical attenuator    page214
        PXA_N9030B.write(':DISP:WIND:TRAC:Y:RLEV 10')  # Ref Value    page201
        PXA_N9030B.write(':DISP:WIND:TRAC:Y:PDIV 10')  # Scale/Div    page203
        PXA_N9030B.write(':DISP:WIND:TRAC:Y:SPAC LOG')  # Display Scale ： LOG    page203
        PXA_N9030B.write(':UNIT:POW DBM')  # Y Axis Unit : dBm    page203

        # PXA_N9030B.write(':DISP:WIND:TRAC:Y:RLEV:OFFS:STAT ON')  # Reference Level Offset : ON    page209
        # PXA_N9030B.write(':DISP:WIND:TRAC:Y:RLEV:OFFS 0')  # Reference Level Offset : 0dBm    page209
        # PXA_N9030B.write(':DISP:WIND:TRAC:Y:NDIV 10')  # Number of Divisions : 6-20 对应(6-20)*PDIV的功率范围    page210
        PXA_N9030B.write(':BWID:AUTO ON')  # Res BW    page244
        PXA_N9030B.write(':BWID:VID:AUTO ON')  # Video BW    page247
        PXA_N9030B.write(':BAND:VID:RAT:AUTO ON')  # VBW:3dB RBW   page248
        PXA_N9030B.write(':FREQ:SPAN:BAND:RAT:AUTO ON')  # Span:3dB RBW   page249

        PXA_N9030B.write(':DISP:ANN:SCR ON')  # 打开屏幕注释  default：ON     page272
        PXA_N9030B.write(':DISP:ANN:MBAR ON')  # 打开顶部测量栏    default：ON     page273

        # PXA_N9030B.write(':FREQ:CENT 19 GHz')  # Center Frequency 设置为18GHz  page280
        # # PXA_N9030B.write(':FREQ:RF:CENT 20 GHz')  # Center Frequency 设置为20GHz  page280
        # PXA_N9030B.write(':FREQ:SPAN 6GHz')  # Span 设置为5GHz  page280
        PXA_N9030B.write(':FREQ:STAR 72GHz')  # Freq Start  page290
        PXA_N9030B.write(':FREQ:STOP 82GHz')  # Freq Stop   page292

        PXA_N9030B.write(':FEED EMIX')  # Select Input   page2277
        PXA_N9030B.write(':ROSC:SOUR:TYPE SENS')  # Freq Ref Input  page2395

        PXA_N9030B.write(':FEED EMIX')  # Select Input   page2277
        PXA_N9030B.write(':ROSC:SOUR:TYPE SENS')  # Freq Ref Input  page2395

        PXA_N9030B.write(':INST:SCR:SEL "Power Test"')  # 选择活动窗口 page158
        # PXA_N9030B.write(':INST:CONF:SA:SAN')  # Mode：Spectrum Analyzer  meas：Swept SA  page87
        # PXA_N9030B.write(':CONF:SAN:NDEF')  # Mode：Spectrum Analyzer  meas：Swept SA  page182 X
        # PXA_N9030B.write(':CONFigure:SANalyzer')  # Mode：Spectrum Analyzer  meas：Swept SA  page182
        time.sleep(0.1)
        PXA_N9030B.write(':DISP:WIND:TRAC:Y:RLEV 0')  # Ref Value    page201
        PXA_N9030B.write(':FREQ:STAR 72GHz')  # Freq Start  page290
        PXA_N9030B.write(':FREQ:STOP 82GHz')  # Freq Stop   page292
        time.sleep(0.1)
        PXA_N9030B.write(':CALC:MARK1:MODE POS')  # Mark1点设置为Position   default：POS page313
        # PXA_N9030B.write(':CALC:MARK1:X 20GHz')  # Mark1点设置为20GHz    page308
        PXA_N9030B.write(':CALC:MARK:TABL OFF')  # Marker Table         default：OFF page316
        time.sleep(0.1)
        PXA_N9030B.write(':FREQ:TUNE:IMM')  # Auto Tune  page294
        time.sleep(6)  # 等待仪器调整结束
        PXA_N9030B.write(':FREQ:SPAN 100MHz')  # Span 设置为100MHz  page280
        time.sleep(0.1)
        # PXA_N9030B.write(':INIT:CONT OFF')  # Sweep/Measure:single    default：ON  page485
        PXA_N9030B.write(':INIT:CONT ON')  # Sweep/Measure:continuous   default：ON  page485
        PXA_N9030B.write(':AVER:COUN 100')  # Avg|Hold Num 设置为100次   default：100  page384
        PXA_N9030B.write(':TRAC:TYPE AVER')  # Trace Type ： Average page513
        time.sleep(2)
        PXA_N9030B.write(':CALC:MARK:PEAK:THR -60 dBm')  # Peak Threshold  page325
        PXA_N9030B.write(':CALC:MARK:PEAK:SEAR:MODE MAX')  # Peak Search Mode  page329
        # PXA_N9030B.write(':CALC:MARK1:MAX')  # Peak Search  page319
        PXA_N9030B.write(':CALC:MARK:CPS ON')  # Continuous Peak Search  page372
        time.sleep(1)
        #
        if 1:
            PXA_N9030B.write(':FEED EMIX')  # Select Input   page2277
            PXA_N9030B.write(':ROSC:SOUR:TYPE SENS')  # Freq Ref Input  page2395

            PXA_N9030B.write(':INST:SCR:SEL "Power Test"')  # 选择活动窗口 page158
            # PXA_N9030B.write(':INST:CONF:SA:SAN')  # Mode：Spectrum Analyzer  meas：Swept SA  page87
            # PXA_N9030B.write(':CONF:SAN:NDEF')  # Mode：Spectrum Analyzer  meas：Swept SA  page182 X
            # PXA_N9030B.write(':CONFigure:SANalyzer')  # Mode：Spectrum Analyzer  meas：Swept SA  page182
            time.sleep(0.1)
            PXA_N9030B.write(':DISP:WIND:TRAC:Y:RLEV 0')  # Ref Value    page201
            PXA_N9030B.write(':FREQ:STAR 72GHz')  # Freq Start  page290
            PXA_N9030B.write(':FREQ:STOP 82GHz')  # Freq Stop   page292
            time.sleep(0.1)
            PXA_N9030B.write(':CALC:MARK1:MODE POS')  # Mark1点设置为Position   default：POS page313
            # PXA_N9030B.write(':CALC:MARK1:X 20GHz')  # Mark1点设置为20GHz    page308
            PXA_N9030B.write(':CALC:MARK:TABL OFF')  # Marker Table         default：OFF page316
            time.sleep(0.1)
            PXA_N9030B.write(':FREQ:TUNE:IMM')  # Auto Tune  page294
            time.sleep(6)  # 等待仪器调整结束
            PXA_N9030B.write(':FREQ:SPAN 100MHz')  # Span 设置为100MHz  page280
            time.sleep(0.1)
            # PXA_N9030B.write(':INIT:CONT OFF')  # Sweep/Measure:single    default：ON  page485
            PXA_N9030B.write(':INIT:CONT ON')  # Sweep/Measure:continuous   default：ON  page485
            PXA_N9030B.write(':AVER:COUN 100')  # Avg|Hold Num 设置为100次   default：100  page384
            PXA_N9030B.write(':TRAC:TYPE AVER')  # Trace Type ： Average page513
            time.sleep(2)
            PXA_N9030B.write(':CALC:MARK:PEAK:THR -60 dBm')  # Peak Threshold  page325
            PXA_N9030B.write(':CALC:MARK:PEAK:SEAR:MODE MAX')  # Peak Search Mode  page329
            # PXA_N9030B.write(':CALC:MARK1:MAX')  # Peak Search  page319
            PXA_N9030B.write(':CALC:MARK:CPS ON')  # Continuous Peak Search  page372

    else:
        pass
    # s = PXA_N9030B.query(':FEED?')  # Select Input  page319
    # f = PXA_N9030B.query(':CALC:MARK1:X?')  # Marker Frequency page308/319
    # print(s)
    # if "EMIX" not in s:  # 判断是否多次执行Auto Tune 目前使用是否已选中EXIT做判断依据，没有考虑频率，不可靠，需优化
    if 1:
        PXA_N9030B.write(':FEED EMIX')  # Select Input   page2277
        PXA_N9030B.write(':ROSC:SOUR:TYPE SENS')  # Freq Ref Input  page2395

        PXA_N9030B.write(':INST:SCR:SEL "Power Test"')  # 选择活动窗口 page158
        # PXA_N9030B.write(':INST:CONF:SA:SAN')  # Mode：Spectrum Analyzer  meas：Swept SA  page87
        # PXA_N9030B.write(':CONF:SAN:NDEF')  # Mode：Spectrum Analyzer  meas：Swept SA  page182 X
        # PXA_N9030B.write(':CONFigure:SANalyzer')  # Mode：Spectrum Analyzer  meas：Swept SA  page182
        time.sleep(0.1)
        PXA_N9030B.write(':DISP:WIND:TRAC:Y:RLEV 0')  # Ref Value    page201
        PXA_N9030B.write(':FREQ:STAR 72GHz')  # Freq Start  page290
        PXA_N9030B.write(':FREQ:STOP 82GHz')  # Freq Stop   page292
        time.sleep(0.1)
        PXA_N9030B.write(':CALC:MARK1:MODE POS')  # Mark1点设置为Position   default：POS page313
        # PXA_N9030B.write(':CALC:MARK1:X 20GHz')  # Mark1点设置为20GHz    page308
        PXA_N9030B.write(':CALC:MARK:TABL OFF')  # Marker Table         default：OFF page316
        time.sleep(0.1)
        PXA_N9030B.write(':FREQ:TUNE:IMM')  # Auto Tune  page294
        time.sleep(6)  # 等待仪器调整结束
        PXA_N9030B.write(':FREQ:SPAN 100MHz')  # Span 设置为100MHz  page280
        time.sleep(0.1)
        # PXA_N9030B.write(':INIT:CONT OFF')  # Sweep/Measure:single    default：ON  page485
        PXA_N9030B.write(':INIT:CONT ON')  # Sweep/Measure:continuous   default：ON  page485
        PXA_N9030B.write(':AVER:COUN 100')  # Avg|Hold Num 设置为100次   default：100  page384
        PXA_N9030B.write(':TRAC:TYPE AVER')  # Trace Type ： Average page513
        time.sleep(2)
        PXA_N9030B.write(':CALC:MARK:PEAK:THR -60 dBm')  # Peak Threshold  page325
        PXA_N9030B.write(':CALC:MARK:PEAK:SEAR:MODE MAX')  # Peak Search Mode  page329
        # PXA_N9030B.write(':CALC:MARK1:MAX')  # Peak Search  page319
        PXA_N9030B.write(':CALC:MARK:CPS ON')  # Continuous Peak Search  page372
    time.sleep(1)
    PXA_N9030B.write(':CALC:MARK1:CENT')  # Mkr->CF  page319
    PXA_N9030B.write(':INIT:REST')  # Restart  page489 比IMM重启范围广
    # PXA_N9030B.write(':INIT:IMM')  # Restart  page489

    # PXA_N9030B.write(':DISP:WIND:TRAC:Y:RLEV:OFFS 34')  # Reference Level Offset:34dB 功率补偿  page209
    # PXA_N9030B.write(':DISP:WIND:TRAC:Y:RLEV:OFFS:STAT OFF')  # Reference Level Offset:OFF  page209

    # PXA_N9030B.write(':AVER:CLE')  # page384
    # PXA_N9030B.write(':TRAC:TYPE WRIT')  # page384
    # PXA_N9030B.write(':TRAC:TYPE AVER')  # page384

    time.sleep(4)

    # print(PXA_N9030B.query(':CALC:MARK1:X?'))  # Marker Frequency page308/319
    # print(PXA_N9030B.query(':CALC:MARK1:Y?'))  # Marker Amplitude page310
    Frequency = PXA_N9030B.query(':CALC:MARK1:X?')  # Marker Frequency page308/319
    Amplitude = PXA_N9030B.query(':CALC:MARK1:Y?')  # Marker Amplitude page310
    # print(Amplitude)  # Marker Amplitude page310
    # print(Frequency)  # Marker Frequency page308/319
    # print(PXA_N9030B.query(':SYST:ERR?'))  # 打印系统错误信息  page124
    # time.sleep(0.1)

    time.sleep(0.2)
    # PXA_N9030B.write(':INIT:REST')  # Restart  page489 比IMM重启范围广
    # PXA_N9030B.write(':INIT:IMM')  # Restart  page489

    # time.sleep(10000)
    # PXA_N9030B.close()
    # time.sleep(5)
    # PXA_N9030B.write(':INST:SCR:DEL')  # 删除一个窗口(Screen)   page64

    Freq_Power_data = [Frequency[:-1], Amplitude[:-1]]  # 去掉数据中的\n
    print('Freq_Power_data:', Freq_Power_data)
    # x = [float(Amplitude[:-1]), float(Frequency[:-1])]    # 去掉数据中的\n
    # print('x:', x)
    # print(PXA_N9030B.query(':CALC:MARK1:Y?'))  # Marker Amplitude page310
    # print(PXA_N9030B.query(':CALC:MARK1:X?'))  # Marker Frequency page308/319
    # print(PXA_N9030B.query(':SYST:ERR?'))  # 打印系统错误信息  page124
    # time.sleep(0.1)
    PXA_N9030B.close()
    return Freq_Power_data


def KsInstr_IF_Test():
    # 此函数中备注的page 'x' 为文件 Spectrum Analyzer Mode User's & Programmer's Reference.pdf 中的页数
    PXA_N9030B.write(':INST:SCR:MULT OFF')  # 关闭多窗口显示   page158
    PXA_N9030B.write(':SYST:SEQ OFF')  # 只有一个窗口处于活动 ON 所有窗口顺序处于活动状态 page96

    inst_screen_list = PXA_N9030B.query(':INST:SCR:CAT?')  # 查询已打开的窗口(Screen list)  page159
    if "IF Test" not in inst_screen_list:
        print('没有名称为”IF Test“的窗口，新建”IF Test“窗口')
        PXA_N9030B.write(':INST:SCR:CRE')  # 新增一个窗口(Screen) 指令1   page102
        PXA_N9030B.write(':INST:SCR:REN "IF Test"')  # 修改窗口名称   page100

        PXA_N9030B.write(':INST:CONF:SA:SAN')  # Mode：Spectrum Analyzer  meas：Swept SA  page87
        # PXA_N9030B.write(':CONF:SAN:NDEF')  # Mode：Spectrum Analyzer  meas：Swept SA  page182
        PXA_N9030B.write(':CONFigure:SANalyzer')  # Mode：Spectrum Analyzer  meas：Swept SA  page182

        PXA_N9030B.write(':DISP:VIEW NORM')  # View Selection  Normal|TZOom|SPECtrogram|ZSPan  page184

        # PXA_N9030B.write(':POW:ATT 20')  # Mech Atten  Mechanical attenuator    page214
        PXA_N9030B.write(':POW:ATT:AUTO ON')  # Mech Atten  Mechanical attenuator    page214
        PXA_N9030B.write(':DISP:WIND:TRAC:Y:RLEV 10')  # Ref Value    page201
        PXA_N9030B.write(':DISP:WIND:TRAC:Y:PDIV 10')  # Scale/Div    page203
        PXA_N9030B.write(':DISP:WIND:TRAC:Y:SPAC LOG')  # Display Scale ： LOG    page203
        PXA_N9030B.write(':UNIT:POW DBM')  # Y Axis Unit : dBm    page203

        # PXA_N9030B.write(':DISP:WIND:TRAC:Y:RLEV:OFFS:STAT ON')  # Reference Level Offset : ON    page209
        # PXA_N9030B.write(':DISP:WIND:TRAC:Y:RLEV:OFFS 0')  # Reference Level Offset : 0dBm    page209
        # PXA_N9030B.write(':DISP:WIND:TRAC:Y:NDIV 10')  # Number of Divisions : 6-20 对应(6-20)*PDIV的功率范围    page210
        PXA_N9030B.write(':BWID:AUTO ON')  # Res BW    page244
        PXA_N9030B.write(':BWID:VID:AUTO ON')  # Video BW    page247
        PXA_N9030B.write(':BAND:VID:RAT:AUTO ON')  # VBW:3dB RBW   page248
        PXA_N9030B.write(':FREQ:SPAN:BAND:RAT:AUTO ON')  # Span:3dB RBW   page249

        PXA_N9030B.write(':DISP:ANN:SCR ON')  # 打开屏幕注释  default：ON     page272
        PXA_N9030B.write(':DISP:ANN:MBAR ON')  # 打开顶部测量栏    default：ON     page273

        # PXA_N9030B.write(':FREQ:CENT 19 GHz')  # Center Frequency 设置为18GHz  page280
        # # PXA_N9030B.write(':FREQ:RF:CENT 20 GHz')  # Center Frequency 设置为20GHz  page280
        # PXA_N9030B.write(':FREQ:SPAN 6GHz')  # Span 设置为5GHz  page280
        PXA_N9030B.write(':FREQ:STAR 1KHz')  # Freq Start 设置为16GHz   page290
        PXA_N9030B.write(':FREQ:STOP 10MHz')  # Freq Stop 设置为22GHz  page292

    else:
        pass
    PXA_N9030B.write(':INST:SCR:SEL "IF Test"')  # 选择活动窗口 page158
    # PXA_N9030B.write(':INST:CONF:SA:SAN')  # Mode：Spectrum Analyzer  meas：Swept SA  page87
    # PXA_N9030B.write(':CONF:SAN:NDEF')  # Mode：Spectrum Analyzer  meas：Swept SA  page182 X
    # PXA_N9030B.write(':CONFigure:SANalyzer')  # Mode：Spectrum Analyzer  meas：Swept SA  page182
    time.sleep(0.1)
    PXA_N9030B.write(':DISP:WIND:TRAC:Y:RLEV 0')  # Ref Value    page201
    PXA_N9030B.write(':FREQ:STAR 1KHz')  # Freq Start 设置为16GHz   page290
    PXA_N9030B.write(':FREQ:STOP 10MHz')  # Freq Stop 设置为22GHz  page292
    time.sleep(0.1)
    PXA_N9030B.write(':CALC:MARK1:MODE POS')  # Mark1点设置为Position   default：POS page313
    # PXA_N9030B.write(':CALC:MARK1:X 20GHz')  # Mark1点设置为20GHz    page308
    PXA_N9030B.write(':CALC:MARK:TABL OFF')  # Marker Table         default：OFF page316
    time.sleep(0.1)
    PXA_N9030B.write(':FREQ:TUNE:IMM')  # Auto Tune  page294
    time.sleep(6)  # 等待仪器调整结束
    PXA_N9030B.write(':DISP:WIND:TRAC:Y:RLEV -10')  # Ref Value    page201
    PXA_N9030B.write(':FREQ:SPAN 10MHz')  # Span 设置为100MHz  page280
    time.sleep(0.1)
    # PXA_N9030B.write(':INIT:CONT OFF')  # Sweep/Measure:single    default：ON  page485
    PXA_N9030B.write(':INIT:CONT ON')  # Sweep/Measure:continuous   default：ON  page485
    PXA_N9030B.write(':AVER:COUN 100')  # Avg|Hold Num 设置为100次   default：100  page384
    PXA_N9030B.write(':TRAC:TYPE AVER')  # Trace Type ： Average page513
    time.sleep(2)
    PXA_N9030B.write(':CALC:MARK:PEAK:THR -50 dBm')  # Peak Threshold  page325
    PXA_N9030B.write(':CALC:MARK:PEAK:SEAR:MODE MAX')  # Peak Search Mode  page329
    # PXA_N9030B.write(':CALC:MARK1:MAX')  # Peak Search  page319
    PXA_N9030B.write(':CALC:MARK:CPS ON')  # Continuous Peak Search  page372
    time.sleep(0.1)
    PXA_N9030B.write(':CALC:MARK1:CENT')  # Mkr->CF  page319

    # PXA_N9030B.write(':AVER:CLE')  # page384
    # PXA_N9030B.write(':TRAC:TYPE WRIT')  # page384
    # PXA_N9030B.write(':TRAC:TYPE AVER')  # page384

    time.sleep(2)
    time.sleep(0.1)

    Amplitude = PXA_N9030B.query(':CALC:MARK1:Y?')  # Marker Amplitude page310
    Frequency = PXA_N9030B.query(':CALC:MARK1:X?')  # Marker Frequency page308/319
    print(' Frequency(Hz):', Frequency, 'Amplitude(dBm):', Amplitude)
    # print(Amplitude)
    # print(Frequency)

    Freq_Amp_data = [Frequency[:-1], Amplitude[:-1]]  # 去掉数据中的\n
    # print('Amp_Freq_list:', Amp_Freq_data)

    return Freq_Amp_data

import math

from com_connect import STM32_com

from mylog import print_2bytes_hex


# def send_data(data):
#     while True:
#         time.sleep(3)
#         # data = comPackData()
#         # print(data)
#         print_2bytes_hex(data)
#         st.write(data)  # 串口发送成功，要验证ST接受数据是否正确


# def receive_data():  # 接收函数
#     while True:
#         if st.inWaiting() > 0:  # 当接收缓冲区中的数据不为零时，执行下面的代码
#             rx_data = st.read(st.inWaiting())
#             print('Receive_data : ')
#             print_2bytes_hex(rx_data)


def receive_data_manual():  # 接收函数
    while STM32_com.inWaiting() > 0:  # 当接收缓冲区中的数据不为零时，执行下面的代码
        rx_data = STM32_com.read(STM32_com.inWaiting())
        # print('Receive_data : ')
        if rx_data[0] == 0x54:
            # print('receive ACK success')
            if rx_data[6] == 0x00:
                # print('寄存器配置正确')
                print('Receive_data_manual : ')
                print_2bytes_hex(rx_data)
            else:
                print('寄存器配置错误')
        # print('Receive_data_manual : ')
        # print_2bytes_hex(rx_data)


def receive_reg_data_handle():  # 接收函数
    while STM32_com.inWaiting() > 0:  # 当接收缓冲区中的数据不为零时，执行下面的代码
        rx_data = STM32_com.read(STM32_com.inWaiting())
        print('Receive_data : ')
        print_2bytes_hex(rx_data)

        data_len = len(rx_data)
        parsed_data_len = (data_len - 10)
        # reg_number = parsed_data_len / 3
        # print('len(rx_data) : ', data_len)
        # print('parsed_data_len : ', parsed_data_len)
        # print('reg_number : ', parsed_data_len / 3)

        # format(255, '#x'), format(255, 'x'), format(255, 'X')

        # print('reg_addr_h, reg_addr_l, reg_value :')
        print('reg_addr, reg_value :')
        reg_addr_value = []
        for index in range(math.trunc(parsed_data_len / 3)):
            reg_addr_h = rx_data[9+index*3]
            reg_addr_l = rx_data[10+index*3]
            reg_addr = ((reg_addr_h << 8) | reg_addr_l)
            reg_value = rx_data[11+index*3]
            reg_addr_value.append('0x%02X' % reg_addr)
            reg_addr_value.append('0x%02X' % reg_value)
            print('0x%02X' % reg_addr, '0x%02X' % reg_value)

            # print(hex(rx_data[9+index*3]), hex(rx_data[10+index*3]), hex(rx_data[11+index*3]))
            # 补全
            # print('0x%02X' % (rx_data[9+index*3]), '0x%02X' % (rx_data[10+index*3]), '0x%02X' % (rx_data[11+index*3]))
            # print('0x%02X' % (((rx_data[9+index*3]) << 8) | (rx_data[10+index*3])), '0x%02X' % (rx_data[11+index*3]))
        # print('read_reg_data:', reg_addr_data)
        return reg_addr_value


def send_data(data):
    print_2bytes_hex(data)
    STM32_com.write(data)  # 串口发送数据
    #
    #
    # def receive_data():  # 接收函数
    #     while st.inWaiting() > 0:  # 当接收缓冲区中的数据不为零时，执行下面的代码
    #         rx_data = st.read(10)
    #         print_2bytes_hex(rx_data)

    # def saveSql(a):  # 保存接收的数据
    #     # time.time返回当前时间的时间戳,即1234892919.655932这种类型
    #     sql = "INSERT INTO VOC_DATA(value,create_time) VALUES (" + str(a) + "," + str(int(time.time())) + ")"
    #     cursor.execute(sql)
    #     db.commit()
    #     st.flushInput()

import math
import time
# import xlwt
# import xlrd
# import openpyxl
import xlwings as xw
# import xlsxwriter

"""
xlrd/xlwt：Python2和3都支持的库；xlrd库仅支持读取xls和xlsx；xlwt库仅支持读写xls格式的文件，不支持读写xlsx文件。

openpyxl：支持读写xlsx文件，功能较广泛，可以设置单元格格式等；但是不支持读写xls文件。

xlwings：支持读写xls和xlsx文件；也可以设置单元格格式等操作。

xlsxwriter：用于创建xlsx/xls文件；支持图片/表格/图表/格式等；缺点是不能打开/修改已有的文件。
"""


def xlsx_init(test_data_folder):
    file_folder = test_data_folder
    app = xw.App(visible=False, add_book=False)  # 创建一个进程 App,不可见，不自动创建Book
    app.display_alerts = False  # 不显示Excel 消息框
    app.screen_updating = False  # 是否实时刷新excel程序的显示内容
    # # file_name1 = Test_process_name1 + time.strftime('%Y.%m.%d.%H.%M.%S',
    # #                                                time.localtime(time.time())).replace(".", "") + ".xlsx"
    file_name = '\\' + "Test" + "_" + time.strftime('%Y%m%d%H%M%S', time.localtime())

    # 新建Excel
    wb = app.books.add()
    # wbs = wb.sheets
    # ws.add('new')
    # wbs[0].name = "test"    # 更改第一个sheet名字
    # wbs['Sheet1'].delete()  # 删除工作表
    wb.save(file_folder + file_name + ".xlsx")
    file_full_path = wb.fullname

    # Pll_Test_Title = ['芯片编号', '0x1345', '0x1372', 'Sync_out_Freq MIN(GHz)', 'Sync_out_Freq MAX(GHz)', '备注']
    # # ws.range('B1').value = Pll_Test_Title  # 写入行数据
    # # ws.range('A2').options(transpose=True).value = Pll_Test_Title   # 写入列数据
    wb.save()
    wb.close()
    # app.kill()
    app.quit()

    print('New Excel Complete', '"', file_name[1:] + '.xlsx', '"')
    return file_full_path


def xlsx_Handle(excel_full_name, sheet_name, test_title, data):
    # df = pd.read_excel(r'C:\Users\DELL\PycharmProjects\AutomaticTestProject\Test.xlsx', sheet_name=None)  # 读取所有sheet
    # print(df)
    # df = pd.read_excel(r'C:\Users\DELL\PycharmProjects\AutomaticTestProject\Test.xlsx', sheet_name='Sheet1', header=0)
    # print(df)
    # df = pd.read_excel(r'C:\Users\DELL\PycharmProjects\AutomaticTestProject\Test.xlsx', sheet_name='Sheet2',
    #                    header=0, usecols="B:F")
    # print(df)

    # df = pd.ExcelFile(r'C:\Users\DELL\PycharmProjects\AutomaticTestProject\Test.xlsx')  # 读取所有sheet
    # print(df.sheet_names)
    # print(df.parse(sheet_name='Sheet1'))
    # print(df.parse(sheet_name='Sheet2'))
    # # print(df.parse(sheet_name='Sheet1', header=1))

    # wb = xlsxwriter.Workbook(r'C:\Users\DELL\PycharmProjects\AutomaticTestProject\Test.xlsx')
    # # wb.add_worksheet('input2')
    # ws = wb.add_worksheet('input')
    # ws.write(0, 0, 1)  # 将值1写入单元格A1
    # ws.write(1, 0, 2)  # 将值2写入单元格A2
    # ws.write(2, 0, 3)  # 将值3写入单元格A3
    # ws.write(3, 0, "=SUM(A1:A3)")  # 将值3写入单元格A3

    File_Full_Folder = excel_full_name
    Test_Sheet_Name = sheet_name
    Pll_Test_Title = test_title
    W_data = data

    app = xw.App(visible=False, add_book=False)  # 创建一个进程 App,不可见，不自动创建Book
    app.display_alerts = False  # 不显示Excel 消息框
    app.screen_updating = False  # 是否实时刷新excel程序的显示内容

    wb = app.books.open(File_Full_Folder)
    wbs = wb.sheets

    # Pll_Test_Title = ['芯片编号', '0x1345', '0x1372', 'Sync_out_Freq MIN(GHz)', 'Sync_out_Freq MAX(GHz)', '备注']
    # ws.range('B1').value = Pll_Test_Title  # 写入行数据
    # ws.range('A2：A7').options(transpose=True).value = Pll_Test_Title   # 写入列数据

    # Pll_Test_Title1 = [['芯片编号'], ['0x1345'], ['0x1372'], ['Sync_out_Freq MIN'], ['Sync_out_Freq MAX'], ['备注']]
    # ws.range('A2').options(transpose=True).value = Pll_Test_Title1   # 写入行数据

    # 获取excel中的sheet名
    Sheet_Num = len(wbs)
    Sheet_Name_List = []
    for i in range(0, Sheet_Num):
        if i >= 0:
            sht = wb.sheets[i]
            Sheet_Name_List.append(sht.name)
            i += 1  # 计数数量自加1
        else:
            pass
    # print(Sheet_Name_List)
    # 判断是否新建Sheet，传参：excel地址、sheet名、Title
    if Test_Sheet_Name not in Sheet_Name_List:
        # print(Test_process_name, '不存在')
        print('New Sheet ：', Test_Sheet_Name)
        ws_add = wb.sheets.add(Test_Sheet_Name)
        ws_add.range('A1').value = Pll_Test_Title  # 写入行数据
        # ws.autofit(axis='r')    # 自动调整行
        # ws.autofit(axis='c')    # 自动调整列
        ws_add.autofit()  # 自动调整
        # print(ws_add)
    else:
        # # ws = wb.sheets.open(Test_process_name)
        # print(Test_Sheet_Name, '已存在')
        pass
    if ('Sheet1' in Sheet_Name_List) and (len(wbs) > 1):
        print("Delete Sheet ：", 'Sheet1')
        wbs['Sheet1'].delete()  # 删除工作表

    # if "Sheet1" not in Sheet_Name_List:
    #     print("Sheet1", '不存在')
    #     print('新建', "Sheet1")
    #     ws_add = wb.sheets.add("Sheet1")
    # else:
    #     print("Sheet1", '已存在')

    # ws = wb.sheets.open(Test_process_name)

    # for i, row in enumerate(Title_Data):
    #     for j, col in enumerate(row):
    #         # wb.sheets.active.write(i, j, col)
    #         # ws.range(i, j).value = col
    #
    #         # print(col)
    #         # print(ws_add.range(1, j).value)
    # ws = wb.sheets[0]
    ws = wbs(Test_Sheet_Name)
    # ws = wbs("Sheet1")
    # ws = wb.sheets(Sheet_Name_List[0])

    # ws.range('A' + str(1)).value = Pll_Test_Title   # 写入行数据
    # print(ws.range('A1:E' + str(1)).value)
    # print(ws.range('A1:E1').value)
    # print(ws.range('A1').value)

    # wsa = app.books.active.sheets.active
    wsa = ws
    used_range_last = wsa.used_range.last_cell

    # used_range_last = ws.used_range.last_cell
    # print('used_range_last: ', used_range_last)
    rows = used_range_last.row
    columns = used_range_last.column
    # print('used_range: ', wsa.used_range)
    # print('used_range_last: ', used_range_last)
    # print('rows: ', rows)
    # print('columns: ', columns)
    # print('W_data: ', W_data)

    wsa.range('A' + str(rows + 1)).value = W_data  # 写入行数据

    # dat_len = len(W_data)
    # print('dat_len: ', dat_len)
    # for row in range(1, 2):
    # for col in range(0, dat_len):
    #     # ws[row, col].value = W_data[col]
    #     wsa.range(2, col + 1).value = W_data[col]
    #     # wsa.range((2, 1), (1, col+1)).value = W_data[col]
    #     # print(ws[row, col])
    #     # print(ws[row, col].value)
    # print(ws[:3, :3].value)
    # ws.range('A1').value = Pll_Test_Title   # 写入行数据
    wsa.autofit()  # 自动调整
    wsa.range((1, 1), (rows + 1, columns)).api.HorizontalAlignment = -4108  # -4108 水平居中。 -4131 靠左，-4152 靠右。
    wsa.range((1, 1),
              (rows + 1, columns)).api.VerticalAlignment = -4108  # -4108 垂直居中（默认）。 -4160 靠上，-4107 靠下， -4130 自动换行对齐。
    # wsa.range((3, 1)).api.HorizontalAlignment = -4108  # -4108 水平居中。 -4131 靠左，-4152 靠右。
    # wsa.range((3, 1)).api.VerticalAlignment = -4108  # -4108 垂直居中（默认）。 -4160 靠上，-4107 靠下， -4130 自动换行对齐。

    wb.save()
    wb.close()
    print('Excel saved')
    app.kill()
    # app.quit()  # 结束进程


def xlsx_new_Sheet(excel_full_name, sheet_name, test_title):
    File_Full_Folder = excel_full_name
    Test_Sheet_Name = sheet_name
    Pll_Test_Title = test_title

    app = xw.App(visible=False, add_book=False)  # 创建一个进程 App,不可见，不自动创建Book
    app.display_alerts = False  # 不显示Excel 消息框
    app.screen_updating = False  # 是否实时刷新excel程序的显示内容

    wb = app.books.open(File_Full_Folder)
    wbs = wb.sheets

    # 获取excel中的sheet名
    Sheet_Num = len(wbs)
    Sheet_Name_List = []
    for i in range(0, Sheet_Num):
        if i >= 0:
            sht = wb.sheets[i]
            Sheet_Name_List.append(sht.name)
            i += 1  # 计数数量自加1
        else:
            pass
    # print(Sheet_Name_List)
    # 判断是否新建Sheet，传参：excel地址、sheet名、Title
    if Test_Sheet_Name not in Sheet_Name_List:
        # print(Test_process_name, '不存在')
        print('New Sheet ：', Test_Sheet_Name)
        ws_add = wb.sheets.add(Test_Sheet_Name)
        ws_add.range('A1').value = Pll_Test_Title  # 写入行数据
        # ws.autofit(axis='r')    # 自动调整行
        # ws.autofit(axis='c')    # 自动调整列
        ws_add.autofit()  # 自动调整
        # print(ws_add)
        if ('Sheet1' in Sheet_Name_List) and (len(wbs) > 1):
            print("Delete Sheet ：", 'Sheet1')
            wbs['Sheet1'].delete()  # 删除工作表
    else:
        # # ws = wb.sheets.open(Test_process_name)
        # print(Test_Sheet_Name, '已存在')
        pass

    wb.save()
    wb.close()
    print('Excel saved')
    app.kill()
    # app.quit()  # 结束进程


def GPADC_xlsx_Handle(excel_full_name, sheet_name, test_title, data):
    File_Full_Folder = excel_full_name
    Test_Sheet_Name = sheet_name
    Pll_Test_Title = test_title
    W_data = data
    print('Waiting...')
    app = xw.App(visible=False, add_book=False)  # 创建一个进程 App,不可见，不自动创建Book
    app.display_alerts = False  # 不显示Excel 消息框
    app.screen_updating = False  # 是否实时刷新excel程序的显示内容

    wb = app.books.open(File_Full_Folder)
    wbs = wb.sheets

    # 获取excel中的sheet名
    Sheet_Num = len(wbs)
    Sheet_Name_List = []
    for i in range(0, Sheet_Num):
        if i >= 0:
            sht = wb.sheets[i]
            Sheet_Name_List.append(sht.name)
            i += 1  # 计数数量自加1
        else:
            pass
    # print(Sheet_Name_List)
    # 判断是否新建Sheet，传参：excel地址、sheet名、Title
    if Test_Sheet_Name not in Sheet_Name_List:
        # print(Test_process_name, '不存在')
        print('New Sheet ：', Test_Sheet_Name)
        ws_add = wb.sheets.add(Test_Sheet_Name)
        ws_add.range('A1').value = Pll_Test_Title  # 写入行数据
        # ws.autofit(axis='r')    # 自动调整行
        # ws.autofit(axis='c')    # 自动调整列
        ws_add.autofit()  # 自动调整
        # print(ws_add)
    else:
        # # ws = wb.sheets.open(Test_process_name)
        # print(Test_Sheet_Name, '已存在')
        pass
    if ('Sheet1' in Sheet_Name_List) and (len(wbs) > 1):
        print("Delete Sheet ：", 'Sheet1')
        wbs['Sheet1'].delete()  # 删除工作表

    ws = wbs(Test_Sheet_Name)
    wsa = ws
    used_range_last = wsa.used_range.last_cell

    rows = used_range_last.row
    # columns = used_range_last.column
    # print('rows:', rows)
    # print('columns:', columns)

    gpadc_in_data_len = len(W_data)
    # print('gpadc_in_data:', gpadc_in_data)
    # print('gpadc_in_data_len:', gpadc_in_data_len)
    gpadc_data = []
    # for cnt in range(math.trunc(gpadc_in_data_len / 3)):
    #     gpadc_data.append([W_data[3 * cnt], W_data[3 * cnt + 1], W_data[3 * cnt + 2]])
    for cnt in range(math.trunc(gpadc_in_data_len / 5)):
        gpadc_data.append([W_data[5 * cnt], W_data[5 * cnt + 1],
                           W_data[5 * cnt + 2], W_data[5 * cnt + 3], W_data[5 * cnt + 4]])
    for i, row in enumerate(gpadc_data):
        for j, col in enumerate(row):
            wsa.range(i + rows, j+1+7).value = col  # 写入行数据
            wsa.autofit()  # 自动调整
            # HorizontalAlignment -4108 水平居中。 -4131 靠左，-4152 靠右。
            wsa.range((1, 1), (i + rows, j + 1 + 7)).api.HorizontalAlignment = -4108
            # VerticalAlignment -4108 垂直居中（默认）。 -4160 靠上，-4107 靠下， -4130 自动换行对齐。
            wsa.range((1, 1), (i + rows, j + 1 + 7)).api.VerticalAlignment = -4108
    # wb.save()

    # wsa.range('A' + str(rows + 1)).value = W_data  # 写入行数据

    # wsa.autofit()  # 自动调整
    # # HorizontalAlignment -4108 水平居中。 -4131 靠左，-4152 靠右。
    # wsa.range((1, 1), (rows + 1, columns)).api.HorizontalAlignment = -4108
    # # VerticalAlignment -4108 垂直居中（默认）。 -4160 靠上，-4107 靠下， -4130 自动换行对齐。
    # wsa.range((1, 1), (rows + 1, columns)).api.VerticalAlignment = -4108

    wb.save()
    wb.close()
    print('Excel saved')
    app.kill()
    # app.quit()  # 结束进程

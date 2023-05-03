import xlwt
import xlrd
import time
import json
import requests

book = xlwt.Workbook(encoding='utf-8', style_compression=0)
sheet_ID = book.add_sheet('ID', cell_overwrite_ok=True)
sheet_NAME = book.add_sheet('NAME', cell_overwrite_ok=True)
sheet_ID.write(0, 0, '查找用户ID')
sheet_NAME.write(0, 0, '查找用户名')

data_excel = xlrd.open_workbook('../search_UPuser/Pop&Samp.xls')
table = data_excel.sheets()[2]
uids = table.col_values(4, start_rowx=1, end_rowx=None)

n = 1
c = 1


def search_ins(uid):
    global n
    global c
    c = 0
    url = "https://api.bilibili.com/x/relation/followings?vmid=%d&pn=%d&ps=50&order=desc&order_type=attention&jsonp=jsonp"  # % (UID, Page Number)
    for i in range(1, 6):
        time.sleep(1)
        html = requests.get(url % (uid, i))
        if html.status_code != 200:
            print("GET ERROR!")
            return []
        text = html.text
        dic = json.loads(text)
        if dic['code'] == -400:
            return []
        try:
            list = dic['data']['list']
        except:
            return []
        for usr in list:
            c = c + 1
            print(usr['uname'])
            sheet_ID.write(n, c, usr['mid'])
            sheet_NAME.write(n, c, usr['uname'])


if __name__ == '__main__':
    for uid in uids:
        sheet_ID.write(n, 0, uid)
        sheet_NAME.write(n, 0, uid)
        print(f'正在爬取ID：{uid}')
        search_ins(uid)
        n = n + 1

book.save('InsList3.xls')
print('爬取完成')

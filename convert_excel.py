import win32com.client
import os

src = r"C:\Users\Administrator\Desktop\ceshi\temp.xls"
dst = r"C:\Users\Administrator\Desktop\ceshi\temp_converted.xlsx"

print("打开Excel并另存为xlsx...")
excel = win32com.client.Dispatch("Excel.Application")
excel.Visible = False
excel.DisplayAlerts = False

wb = excel.Workbooks.Open(src)
wb.SaveAs(dst, FileFormat=51)  # 51 = xlsx
wb.Close()
excel.Quit()

print(f"已保存到: {dst}")

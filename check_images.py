import openpyxl
import os

f = r"C:\Users\Administrator\Desktop\ceshi\temp.xls"

# xls doesn't support images directly, need to check
print("检查文件中的图片/媒体内容...")

# Try with xlrd for xls
try:
    import xlrd
    wb = xlrd.open_workbook(f)
    print(f"Sheets: {wb.sheet_names()}")
    sh = wb.sheet_by_index(0)
    print(f"Rows: {sh.nrows}, Cols: {sh.ncols}")
    
    # Check for embedded images
    print(f"\n媒体对象数量: {len(wb._src__images) if hasattr(wb, '_src__images') else 'N/A'}")
except ImportError:
    print("xlrd not available")

# Try with openpyxl on a copied file converted to xlsx
try:
    import xlrd
    wb = xlrd.open_workbook(f)
    print("\n使用xlrd读取成功")
    print(f"总行数: {wb.sheet_by_index(0).nrows}")
except Exception as e:
    print(f"xlrd error: {e}")

# Check if there are image files embedded
print("\n检查文件内容中是否有图片...")
print("提示: .xls格式的图片需要特殊处理")
print("建议: 1) 把xls另存为xlsx格式再处理图片")
print("      2) 或者告诉我图片在哪里，我来单独处理")

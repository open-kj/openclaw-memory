$excel = New-Object -ComObject Excel.Application
$excel.Visible = $false
$excel.DisplayAlerts = $false
$src = "C:\Users\Administrator\Desktop\ceshi\temp.xls"
$dst = "C:\Users\Administrator\Desktop\ceshi\temp_converted.xlsx"
$wb = $excel.Workbooks.Open($src)
$wb.SaveAs($dst, 51)
$wb.Close()
$excel.Quit()
Write-Host "Done: $dst"

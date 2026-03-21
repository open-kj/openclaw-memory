$r = Invoke-WebRequest -Uri 'https://qt.gtimg.cn/q=sz300394,sz300223,sz300548,sh688521' -UseBasicParsing
$enc = [System.Text.Encoding]::GetEncoding('GBK')
$enc.GetString($r.Content)

$API_DATA = @"
v_sz300394="51~天孚通信~300394~317.40~307.99~335.00~311417~159319~152086~317.49~1~317.42~1~317.40~5~317.39~35~317.36~17~317.60~1~317.73~2~317.74~2~317.75~2~317.77~1~~20260320134503~9.41~3.06~336.63~315.21~317.40/311417/10051359324~311417~1005136~4.01~134.66~~336.63~315.21~6.95~2462.56~2467.52~50.58~369.59~246.39~1.19~51~322.76~126.29~183.66~~~2.82~1005135.9324~0.0000~0~ A~GP-A-CYB~56.33~-2.34~0.27~37.56~31.31~388.94~39.94~-1.70~-3.82~59.26~775852386~777415891~76.12~348.31~775852386~~~400.40~-0.01~~CNY~0~~317.31~18~";
v_sz300223="51~炬芯科技~300223~122.15~121.92~122.12~240081~126326~113738~122.15~1~122.14~50~122.13~33~122.12~70~122.11~14~122.17~1~122.18~7~122.19~2~122.20~14~122.21~4~~20260320134503~0.23~0.19~126.50~118.22~122.15/240081/2942367435~240081~294237~5.71~185.63~~126.50~118.22~6.79~513.73~589.42~4.75~146.30~97.54~1.01~140~122.56~172.86~160.96~~~2.56~294236.7435~0.0000~0~ A~GP-A-CYB~15.19~2.52~0.08~2.56~2.33~151.98~56.85~-1.91~-1.05~34.16~420570410~482540723~71.43~86.40~420570410~~~58.74~-0.12~~CNY~0~~122.08~24~";
v_sz300548="51~博创科技~300548~147.81~143.56~148.90~247637~142486~105109~147.81~1~147.76~1~147.75~1~147.74~11~147.73~2~147.82~1~147.85~18~147.86~40~147.87~13~147.88~5~~20260320134503~4.25~2.96~156.50~147.58~147.81/247637/3758259938~247637~375826~9.20~151.46~~156.50~147.58~6.21~398.02~430.97~22.99~172.27~114.85~1.73~-61~151.76~129.31~597.99~~~2.51~375825.9938~0.0000~0~ A~GP-A-CYB~4.09~-6.95~0.05~15.20~14.01~177.77~26.46~-1.36~-16.16~17.64~269278878~291571378~-65.59~126.60~269278878~~~252.26~0.01~~CNY~0~~147.68~18~";
v_sh688521="1~源杰股份~688521~204.60~199.52~203.31~14912672~7551607~7353631~204.60~10~204.53~2~204.52~2~204.51~12~204.50~42~204.62~8~204.63~12~204.77~5~204.78~203~204.86~14~~20260320134504~5.08~2.55~209.88~198.60~204.60/14912672/3037376890~14912672~303738~2.84~-203.86~~209.88~198.60~5.65~1076.02~1076.02~31.48~239.42~159.62~1.41~-174~203.68~-203.86~-203.86~~~2.29~303737.6890~0.0000~0~A R~GP-A-KCB~49.38~-1.88~0.00~-15.54~-8.52~288.00~80.01~-15.05~-23.79~58.75~525915273~525915273~-56.13~140.14~525915273~~~109.76~-0.49~~CNY~0~___D__F__NY~204.94~-21~100";
"@

$lines = $API_DATA -split "`n"

$p_tianfu = [double]($lines[0].Split('~')[3])
$p_juxin = [double]($lines[1].Split('~')[3])
$p_bochuang = [double]($lines[2].Split('~')[3])
$p_yuanjie = [double]($lines[3].Split('~')[3])

$v_tianfu = $p_tianfu * 618
$v_juxin = $p_juxin * 1530
$v_bochuang = $p_bochuang * 1000
$v_yuanjie = $p_yuanjie * 1000
$cash = 294992

$total_market = $v_tianfu + $v_juxin + $v_bochuang + $v_yuanjie
$total_assets = $total_market + $cash
$total_pnl = $total_assets - 1000000

$stop_tianfu = [math]::Round(306.99 * 0.95, 2)
$stop_juxin = [math]::Round(122.34 * 0.95, 2)
$stop_bochuang = [math]::Round(148.57 * 0.95, 2)
$stop_yuanjie = [math]::Round(198.88 * 0.95, 2)

$pnl_tianfu = [math]::Round($p_tianfu * 618 - 306.99 * 618, 2)
$pnl_juxin = [math]::Round($p_juxin * 1530 - 122.34 * 1530, 2)
$pnl_bochuang = [math]::Round($p_bochuang * 1000 - 148.57 * 1000, 2)
$pnl_yuanjie = [math]::Round($p_yuanjie * 1000 - 198.88 * 1000, 2)

Write-Host "TianFu=$p_tianfu"
Write-Host "JuXin=$p_juxin"
Write-Host "BoChuang=$p_bochuang"
Write-Host "YuanJie=$p_yuanjie"
Write-Host "V_TianFu=$v_tianfu"
Write-Host "V_JuXin=$v_juxin"
Write-Host "V_BoChuang=$v_bochuang"
Write-Host "V_YuanJie=$v_yuanjie"
Write-Host "Cash=$cash"
Write-Host "TotalMarket=$total_market"
Write-Host "TotalAssets=$total_assets"
Write-Host "TotalPnL=$total_pnl"
Write-Host "Stop_TianFu=$stop_tianfu"
Write-Host "Stop_JuXin=$stop_juxin"
Write-Host "Stop_BoChuang=$stop_bochuang"
Write-Host "Stop_YuanJie=$stop_yuanjie"
Write-Host "TianFu_OK=$($p_tianfu -gt $stop_tianfu)"
Write-Host "JuXin_OK=$($p_juxin -gt $stop_juxin)"
Write-Host "BoChuang_OK=$($p_bochuang -gt $stop_bochuang)"
Write-Host "YuanJie_OK=$($p_yuanjie -gt $stop_yuanjie)"
Write-Host "PnL_TianFu=$pnl_tianfu"
Write-Host "PnL_JuXin=$pnl_juxin"
Write-Host "PnL_BoChuang=$pnl_bochuang"
Write-Host "PnL_YuanJie=$pnl_yuanjie"

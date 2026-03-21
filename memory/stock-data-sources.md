# 股票分析能力汇总

## 实时数据获取（无需联网搜索）

### 1. 东方财富 API ✅
- **实时行情**: `push2.eastmoney.com/api/qt/stock/get`
- **涨跌幅榜**: `push2.eastmoney.com/api/qt/clist/get`
- **K线历史**: `push2his.eastmoney.com/api/qt/stock/kline/get`
- **资金流向**: `push2.eastmoney.com/api/qt/ulist.np/get`
- **板块资金**: `push2.eastmoney.com/api/qt/ulist.np/get`

### 2. 腾讯财经 ✅
- **实时行情**: `qt.gtimg.cn/q=sh600519`

### 3. 同花顺 ✅
- **K线数据**: `web.ifzq.gtimg.cn/appstock/app/fqkline/get`

### 4. 新浪财经 ✅
- **K线数据**: `money.finance.sina.com.cn/quotes_service/api/json_v2.php`

### 5. 财联社 ✅
- **财经日历**: `www.cls.cn`
- **新闻**: `caifuhao.eastmoney.com`

---

## 联网搜索能力

### Tavily 搜索 ✅ (已配置API Key)
- **用途**: 实时新闻、行业动态、热点事件
- **调用方式**: 
  ```bash
  node skills/liang-tavily-search/scripts/search.mjs "查询内容" -n 数量
  ```
- **示例**:
  - `A股今日热点板块`
  - `茅台最新消息`
  - `AI算力板块新闻`

---

## 选股分析流程

### 每日开盘前
1. **Tavily搜索** → 获取今日热点/政策/新闻
2. **东方财富** → 涨幅榜、资金流向
3. **分析筛选** → 符合条件股票

### 盘中监控
1. **东方财富API** → 实时涨跌幅
2. **资金流向** → 主力净流入
3. **自动提醒** → 止盈/止损

### 收盘后
1. **Tavily搜索** → 晚间新闻/公告
2. **东方财富** → 资金流向龙虎榜
3. **复盘总结** → 明日计划

---

## 数据字段说明

### 实时行情字段
| 字段 | 含义 |
|------|------|
| f2 | 最新价 |
| f3 | 涨跌幅 |
| f4 | 涨跌额 |
| f12 | 股票代码 |
| f14 | 股票名称 |
| f62 | 主力净流入 |

### K线字段
| 字段 | 含义 |
|------|------|
| open | 开盘价 |
| close | 收盘价 |
| high | 最高价 |
| low | 最低价 |
| volume | 成交量 |

---

## 调用优先级

1. **首选**: 东方财富API (最稳定、功能全)
2. **备用**: 腾讯/同花顺 (获取不到时用)
3. **搜索**: Tavily (实时新闻、热点事件)

---
更新: 2026-03-19 00:36

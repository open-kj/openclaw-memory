# TOOLS.md - Local Notes

## 数据源（2026-03-25确认）
- 腾讯财经：qt.gtimg.cn ✅ 主数据源
- 新浪财经：hq.sinajs.cn ✅ 备用数据源
- 东方财富：push2.eastmoney.com ❌ 连接被拒
- 脚本路径：D:\AI_Scripts\get_prices_v4.py

## 工作目录规范
- **Excel/文件读取/输出目录**：`D:\AI_Scripts\2026-03-23_深户团购_E公司报价清单\03_Excel数据处理\`
- **输出文件放入对应子目录的output文件夹**
- 不再在workspace里中转，直接读和写到这个路径

Skills define *how* tools work. This file is for *your* specifics — the stuff that's unique to your setup.

## What Goes Here

Things like:
- Camera names and locations
- SSH hosts and aliases  
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Examples

```markdown
### Cameras
- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH
- home-server → 192.168.1.100, user: admin

### TTS
- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

Add whatever helps you do your job. This is your cheat sheet.

---

## Windows exec 注意事项

### Git 中文 commit message 问题
- **问题**：&& 链式命令中中文 commit message 在 PowerShell 中报编码错误（ParserError）
- **解决**：用 `git -C "path"` 语法替代 `cd path && git`，commit message 用纯英文
- **示例**：
  ```
  # 错误（中文报错）
  cd "C:\path" && git commit -m "中文"

  # 正确
  git -C "C:\path" add .
  git -C "C:\path" commit -m "English message only"
  git -C "C:\path" push
  ```

### 房产/新闻平台 web_fetch 反爬策略
- **58同城/贝壳/安居客**：强制登录或验证码 → 直接抓取失败
- **替代方案**：用百度搜索 site:过滤 + 快照获取信息
- **安居客商铺写字楼**：URL 结构已变，需从首页重新导航
- **贝壳**：直接 URL 会跳转登录页，需用 m.ke.com 移动端尝试

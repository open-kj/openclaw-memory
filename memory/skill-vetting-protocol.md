# 技能安全审查协议 (Skill Vetting Protocol)

*来源: ClawHub - skill-vetter*

---

## 何时使用

- [ ] 安装任何来自 ClawHub 的技能前
- [ ] 运行来自 GitHub 仓库的技能前
- [ ] 评估其他agent分享的技能
- [ ] 被要求安装未知代码时

---

## 审查步骤

### Step 1: 来源检查

- [ ] 技能来自哪里？
- [ ] 作者是否知名/有信誉？
- [ ] 有多少下载量/星标？
- [ ] 最后更新时间是什么时候？
- [ ] 有其他agent的评价吗？

### Step 2: 代码审查 (必做)

🚨 **立即拒绝如果看到:**
─────────────────────────────────────────
- curl/wget 到未知URL
- 发送数据到外部服务器
- 请求凭证/Token/API密钥
- 读取 ~/.ssh, ~/.aws, ~/.config
- 访问 MEMORY.md, USER.md, SOUL.md, IDENTITY.md
- 使用 base64 解码
- 使用 eval() 或 exec() 处理外部输入
- 修改系统文件（workspace外）
- 安装未列出的包
- 网络请求到IP地址而非域名
- 混淆代码（压缩、编码、混淆）
- 请求提升权限/sudo
- 访问浏览器cookie/session
- 接触凭证文件
─────────────────────────────────────────

### Step 3: 权限范围评估

- [ ] 需要读取哪些文件？
- [ ] 需要写入哪些文件？
- [ ] 需要运行哪些命令？
- [ ] 需要网络访问吗？到哪里？
- [ ] 权限范围是否最小化？

### Step 4: 风险分类

| 风险等级 | 示例 | 行动 |
|----------|------|------|
| 🟢 LOW | 笔记、天气、格式化 | 基础审查，可安装 |
| 🟡 MEDIUM | 文件操作、浏览器、API | 需要完整代码审查 |
| 🔴 HIGH | 凭证、交易、系统 | **需要人类批准** |
| ⛔ EXTREME | 安全配置、root权限 | **不要安装** |

---

## 输出格式

```
SKILL VETTING REPORT
═══════════════════════════════════════
Skill: [名称]
Source: [ClawHub / GitHub / 其他]
Author: [用户名]
Version: [版本]
───────────────────────────────────────
METRICS:
• Downloads/Stars: [数量]
• Last Updated: [日期]
• Files Reviewed: [数量]
───────────────────────────────────────
RED FLAGS: [无 / 列出问题]

PERMISSIONS NEEDED:
• Files: [列表或"无"]
• Network: [列表或"无"]
• Commands: [列表或"无"]
───────────────────────────────────────
RISK LEVEL: [🟢 LOW / 🟡 MEDIUM / 🔴 HIGH / ⛔ EXTREME]

VERDICT: [✅ SAFE TO INSTALL / ⚠️ INSTALL WITH CAUTION / ❌ DO NOT INSTALL]

NOTES: [观察备注]
═══════════════════════════════════════
```

---

## 信任层级

- **官方 OpenClaw 技能** → 较低审查（仍需检查）
- **高星标仓库 (1000+)** → 中等审查
- **知名作者** → 中等审查
- **新/未知来源** → 最高审查
- **请求凭证的技能** → 始终需要人类批准

---

## 快速审查命令

```bash
# 检查仓库统计
curl -s "https://api.github.com/repos/OWNER/REPO" | jq '{stars: .stargazers_count, forks: .forks_count, updated: .updated_at}'

# 列出技能文件
curl -s "https://api.github.com/repos/OWNER/REPO/contents/skills/SKILL_NAME" | jq '.[].name'

# 获取并审查 SKILL.md
curl -s "https://raw.githubusercontent.com/OWNER/REPO/main/skills/SKILL_NAME/SKILL.md"
```

---

## 核心原则

- **没有技能值得危害安全**
- **有疑问就不安装**
- **高风险决策请求人类批准**
- **记录审查过程以供未来参考**

> ⚠️ **偏执是特色** 🔒🦀

---
*最后更新: 2026-03-19*

# 🤖 PaperSubmit AI - 桌面Agent使用指南

**本地运行 | 自动监控 | 智能推荐**

---

## 📖 什么是桌面Agent？

PaperSubmit AI 桌面Agent是一个**本地运行的智能助手**，它可以：

✅ **自动监控**指定文件夹中的PDF论文  
✅ **自动分析**论文内容并提取关键词  
✅ **自动推荐**最合适的投稿期刊  
✅ **自动生成**推荐报告和投稿记录  
✅ **本地存储**所有数据，无需上传

---

## 🚀 快速开始

### 1. 准备工作

**创建论文文件夹：**
```bash
mkdir -p ~/Documents/Papers
```

### 2. 启动Agent

**方式1: 使用默认设置**
```bash
cd ~/Desktop/论文投稿Agent/src/backend
source venv/bin/activate
python desktop_agent.py
```

**方式2: 指定文件夹**
```bash
python desktop_agent.py --folder ~/Documents/MyPapers
```

**方式3: 只运行一次（不持续监控）**
```bash
python desktop_agent.py --once
```

### 3. 使用Agent

#### 步骤1: 放入论文PDF
将你的论文PDF文件复制到监控文件夹：
```
~/Documents/Papers/
└── my_paper.pdf
```

#### 步骤2: Agent自动处理
Agent会自动：
1. 发现新论文
2. 提取关键词
3. 推荐期刊
4. 生成推荐报告

#### 步骤3: 查看推荐报告
在同一文件夹中会生成：
```
~/Documents/Papers/
├── my_paper.pdf
├── my_paper_推荐报告.txt  ← 查看这个文件
└── .papersubmit/           ← Agent数据目录
```

#### 步骤4: 创建投稿（可选）
如果要创建投稿记录，创建投稿信息文件：

**文件名：** `my_paper_投稿信息.json`

**内容：**
```json
{
  "journal_name": "arXiv",
  "username": "your_username",
  "password": "your_password",
  "notes": "第一次投稿"
}
```

#### 步骤5: Agent自动创建投稿
Agent会自动：
1. 读取投稿信息
2. 创建投稿记录
3. 生成投稿确认报告
4. 将投稿信息文件标记为"已处理"

---

## 📁 文件结构

### 监控文件夹结构
```
~/Documents/Papers/
├── paper1.pdf                      # 你的论文
├── paper1_推荐报告.txt             # Agent生成的推荐报告
├── paper1_投稿信息.json            # 你创建的投稿信息
├── paper1_投稿信息_已处理.json     # Agent处理后重命名
├── paper1_投稿确认.txt             # Agent生成的投稿确认
├── 投稿状态总览.txt                # 所有论文的状态总览
└── .papersubmit/                   # Agent数据目录（隐藏）
    ├── papers.json                 # 论文数据库
    ├── submissions.json            # 投稿数据库
    └── agent.log                   # Agent日志
```

---

## 📊 推荐报告示例

```
╔══════════════════════════════════════════════════════════════╗
║          PaperSubmit AI - 期刊推荐报告                      ║
╚══════════════════════════════════════════════════════════════╝

论文文件: deep_learning_paper.pdf
分析时间: 2026-02-05 11:00:00

【提取的关键词】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
machine learning, deep learning, neural networks, computer vision

【推荐期刊 Top 5】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. IEEE TPAMI
   综合评分: 0.383
   匹配度:   0.663
   影响因子: 24.314
   审稿时间: 120 天
   接收率:   15.0%
   投稿系统: scholarone
   网址:     https://ieeexplore.ieee.org/...

2. arXiv
   综合评分: 0.416
   匹配度:   0.310
   影响因子: 0
   审稿时间: 3 天
   接收率:   95.0%
   投稿系统: arxiv
   网址:     https://arxiv.org/

...

【下一步操作】
1. 查看推荐期刊，选择合适的目标期刊
2. 在同目录下创建 {论文名}_投稿信息.json 文件
3. Agent会自动读取并创建投稿记录
```

---

## ⚙️ 配置文件

Agent会在首次运行时创建配置文件：`agent_config.json`

```json
{
  "auto_recommend": true,
  "auto_backup": true,
  "check_interval": 300,
  "file_extensions": [".pdf"],
  "user_email": "",
  "default_authors": []
}
```

**配置说明：**
- `auto_recommend`: 是否自动推荐期刊
- `auto_backup`: 是否自动备份数据
- `check_interval`: 扫描间隔（秒）
- `file_extensions`: 监控的文件类型
- `user_email`: 用户邮箱（用于通知）
- `default_authors`: 默认作者列表

---

## 🎯 使用场景

### 场景1: 日常论文管理
```
1. 将新写好的论文PDF放入监控文件夹
2. Agent自动分析并生成推荐报告
3. 查看推荐报告，选择期刊
4. 创建投稿信息文件
5. Agent自动创建投稿记录
```

### 场景2: 批量处理论文
```
1. 将多篇论文PDF一次性放入文件夹
2. Agent逐个处理，生成推荐报告
3. 查看"投稿状态总览.txt"了解整体情况
```

### 场景3: 定期检查
```
1. Agent持续运行，每5分钟扫描一次
2. 有新论文时自动处理
3. 有投稿请求时自动创建记录
```

---

## 📝 工作流程

```
┌─────────────────┐
│  放入PDF论文    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Agent发现新文件 │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  提取关键词      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  推荐期刊        │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  生成推荐报告    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  用户查看报告    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  创建投稿信息    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Agent创建投稿   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  生成投稿确认    │
└─────────────────┘
```

---

## 🔧 高级功能

### 1. 查看Agent日志
```bash
cat ~/Documents/Papers/.papersubmit/agent.log
```

### 2. 查看论文数据库
```bash
cat ~/Documents/Papers/.papersubmit/papers.json
```

### 3. 查看投稿数据库
```bash
cat ~/Documents/Papers/.papersubmit/submissions.json
```

### 4. 手动触发扫描
```bash
python desktop_agent.py --once
```

### 5. 修改扫描间隔
编辑 `agent_config.json`，修改 `check_interval` 值（秒）

---

## 💡 使用技巧

### 技巧1: 组织论文文件夹
```
~/Documents/Papers/
├── 2024/
│   ├── paper1.pdf
│   └── paper2.pdf
├── 2025/
│   ├── paper3.pdf
│   └── paper4.pdf
└── drafts/
    └── draft1.pdf
```

### 技巧2: 使用描述性文件名
```
✅ 好的命名:
- deep_learning_image_classification.pdf
- transformer_nlp_2024.pdf

❌ 不好的命名:
- paper.pdf
- untitled.pdf
```

### 技巧3: 备份重要数据
```bash
# 备份Agent数据
cp -r ~/Documents/Papers/.papersubmit ~/Documents/Papers_backup/
```

### 技巧4: 定期查看状态总览
```bash
cat ~/Documents/Papers/投稿状态总览.txt
```

---

## 🐛 故障排除

### 问题1: Agent没有发现新论文
**检查：**
- 文件是否是PDF格式
- 文件名是否以`.`开头（隐藏文件）
- Agent是否正在运行

### 问题2: 推荐报告没有生成
**检查：**
- PDF文件是否损坏
- PDF是否包含可提取的文本
- 查看agent.log日志

### 问题3: 投稿信息没有被处理
**检查：**
- 文件名格式是否正确：`{论文名}_投稿信息.json`
- JSON格式是否正确
- 必填字段是否完整

---

## 📊 与Web版本的对比

| 特性 | 桌面Agent | Web版本 |
|------|----------|---------|
| 部署方式 | 本地运行 | 需要服务器 |
| 数据存储 | 本地文件 | 数据库 |
| 使用方式 | 文件夹操作 | 网页上传 |
| 自动化 | 自动监控 | 手动操作 |
| 适用场景 | 个人使用 | 团队协作 |
| 网络要求 | 无需联网 | 需要联网 |

---

## 🚀 启动脚本

创建一个启动脚本方便使用：

**文件：** `start_agent.sh`
```bash
#!/bin/bash
cd ~/Desktop/论文投稿Agent/src/backend
source venv/bin/activate
python desktop_agent.py --folder ~/Documents/Papers
```

**使用：**
```bash
chmod +x start_agent.sh
./start_agent.sh
```

---

## 📞 获取帮助

```bash
python desktop_agent.py --help
```

---

## 🎉 总结

**桌面Agent的优势：**
- ✅ 完全本地运行，数据安全
- ✅ 自动监控文件夹，无需手动操作
- ✅ 智能推荐期刊，节省时间
- ✅ 生成详细报告，便于决策
- ✅ 简单易用，无需复杂配置

**开始使用：**
```bash
cd ~/Desktop/论文投稿Agent/src/backend
source venv/bin/activate
python desktop_agent.py
```

**让论文投稿更简单！** 🚀

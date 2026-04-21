# 🚀 PaperSubmit AI - 论文自动投稿系统

**两种使用方式 | 智能推荐 | 自动化投稿**

---

## 📖 系统简介

PaperSubmit AI 提供两种使用方式：

### 🤖 方式1: 桌面Agent（推荐）
- **本地运行**，自动监控文件夹
- **无需上传**，直接读取本地PDF
- **自动处理**，生成推荐报告
- **适合个人**使用

### 🌐 方式2: Web界面
- **Web界面**，可视化操作
- **团队协作**，多用户支持
- **API接口**，方便集成
- **适合团队**使用

---

## 🤖 桌面Agent使用（推荐）

### 快速开始

**1. 启动Agent**
```bash
cd ~/Desktop/论文投稿Agent/src/backend
source venv/bin/activate
python desktop_agent.py
```

**2. 放入论文**
```bash
# 将PDF文件复制到监控文件夹
cp your_paper.pdf ~/Documents/Papers/
```

**3. 查看推荐**
```bash
# Agent自动生成推荐报告
cat ~/Documents/Papers/your_paper_推荐报告.txt
```

**4. 创建投稿（可选）**
```bash
# 创建投稿信息文件
cat > ~/Documents/Papers/your_paper_投稿信息.json << EOF
{
  "journal_name": "arXiv",
  "username": "your_username",
  "password": "your_password",
  "notes": "第一次投稿"
}
EOF
```

**5. 自动处理**
Agent会自动创建投稿记录并生成确认报告

### 工作流程

```
放入PDF → Agent发现 → 提取关键词 → 推荐期刊 → 生成报告
                                                    ↓
                                          查看报告 → 创建投稿信息
                                                    ↓
                                          Agent处理 → 生成投稿确认
```

### 详细文档
📖 [桌面Agent使用指南](docs/桌面Agent使用指南.md)

---

## 🌐 Web界面使用

### 快速开始

**1. 启动服务**
```bash
cd ~/Desktop/论文投稿Agent
./start.sh
```

**2. 访问系统**
- 前端: http://localhost:3001
- 后端: http://localhost:8000
- API文档: http://localhost:8000/docs

**3. 使用界面**
- 上传论文PDF
- 查看期刊推荐
- 创建投稿记录
- 查看投稿状态

### 详细文档
📖 [Web界面使用指南](docs/使用指南.md)

---

## 📊 功能对比

| 功能 | 桌面Agent | Web界面 |
|------|----------|---------|
| **部署** | 本地运行 | 需要服务器 |
| **数据** | 本地文件 | 数据库 |
| **操作** | 文件夹 | 网页 |
| **自动化** | ✅ 自动监控 | ❌ 手动上传 |
| **适用** | 个人 | 团队 |
| **网络** | 无需联网 | 需要联网 |
| **界面** | 文本报告 | 可视化 |
| **API** | ❌ 无 | ✅ 有 |

---

## 🎯 使用建议

### 选择桌面Agent，如果你：
- ✅ 个人使用
- ✅ 重视数据隐私
- ✅ 喜欢自动化
- ✅ 不需要团队协作

### 选择Web界面，如果你：
- ✅ 团队使用
- ✅ 需要可视化界面
- ✅ 需要API集成
- ✅ 需要多用户管理

---

## 📁 项目结构

```
论文投稿Agent/
├── src/
│   ├── backend/
│   │   ├── desktop_agent.py      # 🤖 桌面Agent主程序
│   │   ├── main.py                # 🌐 Web后端API
│   │   └── ...
│   ├── frontend/
│   │   └── web/
│   │       └── index.html         # 🌐 Web前端界面
│   └── ml_models/
│       ├── keyword_extractor.py   # 关键词提取
│       └── journal_recommender.py # 期刊推荐
├── docs/
│   ├── 桌面Agent使用指南.md       # 🤖 Agent文档
│   ├── 使用指南.md                # 🌐 Web文档
│   └── ...
├── start.sh                       # 🌐 Web启动脚本
└── README.md                      # 本文件
```

---

## 🚀 核心功能

### 1. 智能期刊推荐
- TF-IDF关键词提取
- 余弦相似度匹配
- 多维度综合评分
- Top K推荐

### 2. 自动化处理
- 自动监控文件夹（Agent）
- 自动提取关键词
- 自动生成报告
- 自动创建投稿记录

### 3. 数据管理
- 本地JSON数据库（Agent）
- SQLite数据库（Web）
- 数据导出功能
- 统计分析

### 4. 安全保障
- AES-256加密
- 本地数据存储
- 密码不明文保存

---

## 📖 完整文档

### 桌面Agent
- 📖 [桌面Agent使用指南](docs/桌面Agent使用指南.md)
- 📖 [系统架构设计](docs/系统架构设计文档.md)

### Web界面
- 📖 [Web使用指南](docs/使用指南.md)
- 📖 [API文档](http://localhost:8000/docs)

### 其他文档
- 📖 [商业计划书](docs/商业计划书.md)
- 📖 [开发计划](docs/2天开发计划.md)
- 📖 [项目完成报告](docs/最终功能完成报告.md)

---

## 💡 使用示例

### 桌面Agent示例

**场景：处理一篇机器学习论文**

```bash
# 1. 启动Agent
python desktop_agent.py

# 2. 放入论文
cp deep_learning_paper.pdf ~/Documents/Papers/

# 3. Agent自动处理（几秒钟后）
# 生成文件：
# - deep_learning_paper_推荐报告.txt
# - 投稿状态总览.txt

# 4. 查看推荐
cat ~/Documents/Papers/deep_learning_paper_推荐报告.txt

# 5. 创建投稿
cat > ~/Documents/Papers/deep_learning_paper_投稿信息.json << EOF
{
  "journal_name": "IEEE TPAMI",
  "username": "myuser",
  "password": "mypass",
  "notes": "投稿到顶级期刊"
}
EOF

# 6. Agent自动处理（下次扫描时）
# 生成文件：
# - deep_learning_paper_投稿确认.txt
# - deep_learning_paper_投稿信息_已处理.json
```

### Web界面示例

**场景：团队协作投稿**

```bash
# 1. 启动服务
./start.sh

# 2. 打开浏览器
# http://localhost:3001

# 3. 上传论文
# - 选择PDF文件
# - 填写标题、作者、摘要
# - 点击"上传并获取推荐"

# 4. 查看推荐
# - 系统显示Top 5期刊
# - 查看匹配度、影响因子等

# 5. 创建投稿
# - 选择目标期刊
# - 输入账号密码
# - 点击"投稿"

# 6. 跟踪进度
# - 切换到"投稿仪表盘"
# - 查看所有投稿状态
```

---

## 🛠️ 技术栈

### 后端
- Python 3.9+
- FastAPI (Web API)
- SQLAlchemy (数据库)
- scikit-learn (机器学习)
- Selenium (自动化)

### 前端
- HTML/CSS/JavaScript
- 响应式设计

### 算法
- TF-IDF (关键词提取)
- 余弦相似度 (期刊匹配)
- 多维度评分 (综合推荐)

---

## 📞 获取帮助

### 桌面Agent
```bash
python desktop_agent.py --help
```

### Web界面
访问 API 文档: http://localhost:8000/docs

### 文档
查看 `docs/` 目录下的详细文档

---

## 🎉 开始使用

### 桌面Agent（推荐个人使用）
```bash
cd ~/Desktop/论文投稿Agent/src/backend
source venv/bin/activate
python desktop_agent.py
```

### Web界面（推荐团队使用）
```bash
cd ~/Desktop/论文投稿Agent
./start.sh
```

**让学术发表更简单！** 🚀

---

**项目地址:** ~/Desktop/论文投稿Agent  
**版本:** v1.0 Final  
**更新日期:** 2026-02-05

## 📐 理论基础

> **Harness理论**：在AI领域，Harness（环境设计）比模型本身更重要。
> **红杉论点**：从卖工具到卖结果。

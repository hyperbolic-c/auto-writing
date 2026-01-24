---
name: academic-write
description: "Integrates brainstorming workflow for academic writing inspiration, then executes section-by-section writing with reference management and semantic matching."
---

# Academic Write Command

## 使用方式

`/academic-write <path_to_requirement_file>`

## 执行流程

### Step 0: 集成 Superpowers 工作流（灵感来源）

本命令集成了 `superpowers:brainstorming`、`superpowers:writing-plans`、`superpowers:executing-plans` 工作流，为学术写作提供系统化的探索、规划和执行框架。

---

### Step 1: 读取需求文件

1. 读取用户提供的文件路径
2. 验证文件存在
3. 解析文档结构：
   - 论文题目
   - 章节结构（一级/二级标题）
   - 内容要点
   - 参考文献标注

---

### Step 2: Brainstorming 工作流（灵感探索）

**核心原则：每轮只问一个问题，优先使用选择题**

#### 理解阶段

**提问示例：**

- "这篇论文的研究目的是什么？"
- "目标期刊或会议是什么？"
- "预计篇幅是多少？"
- "有哪些必须包含的关键内容？"

#### 探索备选方案

提出 2-3 种写作方案供选择：

| 方案 | 结构特点 | 适用场景 |
|------|----------|----------|
| **方案 A: 经典 IMRAD** | Introduction → Methods → Results → Discussion | 实验类论文 |
| **方案 B: 问题驱动** | Problem → Analysis → Solution → Evaluation | 方法创新类 |
| **方案 C: 对比结构** | Background → Related Work → Proposed Method → Experiments | 改进类研究 |

**推荐：** 方案 A（经典 IMRAD），因为结构清晰、符合学术规范

#### 设计验证

分段展示设计方案（每段 200-300 字），逐段确认：

1. **论文结构设计** - 章节划分逻辑
2. **每章节重点** - 各章节核心内容
3. **引用策略** - 参考文献分布
4. **写作风格** - 语言风格、术语规范

**每次确认后提问：**
- "这部分设计是否符合预期？需要调整吗？"

---

### Step 3: 生成写作计划

基于 brainstorming 结果，调用 `superpowers:writing-plans` 生成详细写作计划：

```markdown
## 写作计划

### 任务分解
1. [ ] 解析需求文档，提取章节和参考文献
2. [ ] 获取参考文献全文（zotero_get_item_fulltext）
3. [ ] 语义匹配内容要点与文献段落
4. [ ] 撰写第1章 绪论
5. [ ] 撰写第2章 ...
6. [ ] ...

### 验收标准
- 每章节 500-800 字
- 引用 2-3 篇参考文献
- 使用学术语言，避免口语化
```

---

### Step 4: 执行写作计划

调用 `superpowers:executing-plans` 逐章节执行：

#### 4.1 需求文档解析（reference-manager）

调用 `reference-manager` 技能：
- 输入：需求文档内容
- 输出：章节结构 + 参考文献列表（JSON格式）

#### 4.2 参考文献全文获取

对于每章节的参考文献：
- 调用 `zotero_get_item_fulltext` 获取全文
- 记录获取状态

#### 4.3 语义匹配与仿写（paper-writer）

调用 `paper-writer` 技能：
- 输入：章节内容要点 + 参考文献 key
- 处理：匹配段落 → 以第一篇为主要模板仿写
- 输出：完整段落内容

#### 4.4 章节审核

每章节完成后：
- **检查项：**
  - [ ] 内容覆盖所有要点
  - [ ] 引用正确匹配
  - [ ] 语言流畅、学术规范
  - [ ] 与前后章节连贯

- **如需调整：** 返回对应步骤重新处理

---

### Step 5: 整合与输出

1. 整合所有章节
2. 生成摘要（中文/英文）
3. 生成关键词
4. 格式化参考文献
5. 输出完整论文

---

## 完整流程图

```
需求文件
    ↓
读取 → 解析结构
    ↓
Brainstorming（灵感探索）
    ├── 理解研究目的、目标期刊
    ├── 探索写作方案
    └── 分段验证设计
    ↓
生成写作计划
    ↓
执行计划（逐章节）
    ├── 解析需求 → reference-manager
    ├── 获取全文 → zotero_get_item_fulltext
    ├── 语义匹配 → paper-writer
    └── 章节审核
    ↓
整合输出 → 完整论文
```

---

## 工作流集成说明

### Brainstorming 集成

| 阶段 | 集成内容 |
|------|----------|
| 理解需求 | 提问澄清研究目的、目标、约束 |
| 探索方案 | 2-3 种写作结构供选择 |
| 设计验证 | 分段确认，200-300 字/段 |

### Writing Plans 集成

- 生成任务分解（TODO 列表）
- 定义验收标准
- 跟踪进度

### Executing Plans 集成

- 逐章节执行
- 审核点检查
- 循环调整

---

## 示例

```
/academic-write ./research-requirements.md
```

**输出：**

```
**Step 1: 需求文件解析**

论文题目：p-MQWs-n型AlGaN日盲紫外探测器研究
章节数：5 章
参考文献：12 篇

---

**Step 2: Brainstorming**

Q1: 这篇论文的主要创新点是什么？
A) 新结构设计
B) 新材料体系
C) 新工艺方法
D) 性能突破

[用户选择 A]

Q2: 目标期刊是？
A) IEEE Photonics
B) Applied Physics Letters
C) Journal of Applied Physics

[用户选择 B]

（继续提问...）

---

**Step 3: 写作计划生成**

[生成详细 TODO 列表]

---

**Step 4: 执行写作**

[逐章节写作，每章审核]
```

---

## 响应示例

```
**Academic Write 执行结果**

论文标题：p-MQWs-n型AlGaN日盲紫外探测器研究
输出文件：./output/p-MQWs-n-AlGaN-UV-detector.md

**写作统计：**
- 章节数：5 章
- 总字数：~8000 字
- 引用文献：12 篇

**各章节字数：**
- 第1章 绪论：~1200 字
- 第2章 器件研究：~2000 字
- 第3章 实验结果：~2500 字
- 第4章 讨论：~1500 字
- 第5章 结论：~800 字

**参考文献分布：**
- 第1章：3 篇
- 第2章：4 篇
- 第3章：3 篇
- 第4章：2 篇
```

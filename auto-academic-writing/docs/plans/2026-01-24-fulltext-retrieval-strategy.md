# 分层全文获取策略设计

## 1. 背景与问题

当前 `reference-manager` 技能的 SKILL.md 描述中提及"步骤6: Fetch fulltext"，但 LLM 在执行时可能跳过这步，只调用 `zotero_get_item_metadata` 获取摘要。

日志证据：
```
zotero_get_item_metadata → 返回摘要
zotero_get_item_fulltext → 从未调用
```

## 2. 设计目标

- 区分用户提供的精确匹配文献 vs LLM 自主检索的文献
- 按写作章节分配全文获取优先级
- 无 PDF 时自动 fallback 到摘要

## 3. 整体架构

```
┌─────────────────────────────────────────────────────────────┐
│                    文献检索流程                              │
├─────────────────────────────────────────────────────────────┤
│  Phase 1: 用户输入的精确匹配文献                              │
│  └─→ 强制获取全文（无PDF则摘要）                              │
├─────────────────────────────────────────────────────────────┤
│  Phase 2: LLM 语义检索 + 扩展文献                            │
│  ├─→ Methods/Results 章节引用 → 强制全文                      │
│  ├─→ Related Work 高相关度 → 可选全文（LLM判断）              │
│  └─→ 其他 → 摘要即可                                         │
└─────────────────────────────────────────────────────────────┘
```

## 4. Reference Manager 改造

### 4.1 新增输入字段

```markdown
{
  "topic": "Research topic description",
  "reference_titles": ["Title 1", "Title 2"],  // 用户提供的精确引用
  "additional_references": 5,
  "expand_from_references": true,
  "sections_for_fulltext": ["Methods", "Results"]  // 需要全文的章节
}
```

### 4.2 Phase 1 - 精确匹配文献

```
输入: ["Attention Is All You Need", "BERT: Pre-training"]
      ↓
逐条精确搜索 → 匹配最佳结果
      ↓
强制调用 zotero_get_item_fulltext
      ↓
zotero_get_item_fulltext 内部逻辑：
├─ Zotero 全文索引 → 返回内容
├─ 无索引 → 下载 PDF → markitdown 转换
└─ 无 PDF → 返回 "No attachment" 提示
      ↓
如返回 "No attachment" → 调用 zotero_get_item_metadata（摘要）
      ↓
输出: {key: fulltext, key: abstract}
```

### 4.3 Phase 2 - 语义检索文献

```
语义搜索 → 按相似度排序
      ↓
按 sections_for_fulltext 分类：
├─ Methods/Results → required_fulltext_keys
├─ Related Work (top 3) → optional_fulltext_keys
└─ 其他 → 仅元数据
      ↓
先获取 required → 再获取 optional（如token允许）
```

### 4.4 新增输出格式

```markdown
**文献检索结果:**

- **MCP Provider:** {provider}
- **精确匹配:** {n} 篇 (强制全文: {nf} 篇, 摘要: {na} 篇)
- **语义检索:** {m} 篇 (强制全文: {mf} 篇, 可选全文: {mo} 篇, 摘要: {ms} 篇)
- **扩展检索:** {k} 篇 (摘要)

---

**已解析文献:**

### 1. {title} [强制全文]
- **Key:** {key}
**全文内容:**
{fulltext_markdown}

### 2. {title} [可选全文]
- **Key:** {key}
**内容摘要:**
{abstract}
（全文: {fulltext_markdown_preview}）

### 3. {title} [摘要]
- **Key:** {key}
**内容摘要:**
{abstract}
```

## 5. Paper Writer 全文获取触发

### 5.1 输入格式扩展

```markdown
{
  "requirement": {...},
  "outline": {...},
  "references": [
    {
      "title": "Reference Title",
      "key": "ZoteroKey",
      "fulltext_status": "required" | "optional" | "abstract",  // 新增
      "content": "Parsed content",
      "sections_cited": ["Methods"]  // 新增：哪些章节会引用这篇
    }
  ],
  "output_path": "./output/paper.md"
}
```

### 5.2 写作时全文获取策略

```
当 LLM 撰写特定 section 时：

Methods / Results section:
  └─→ 查找 references 中 fulltext_status=required 的文献
      └─→ 如果 content 不完整 → 主动调用 zotero_get_item_fulltext

Related Work section:
  └─→ 查找 references 中 fulltext_status=optional 的文献
      └─→ 评估相关度后决定是否调用 fulltext

其他 section:
  └─→ 使用已有摘要/元数据
```

### 5.3 触发规则

| 触发点 | 动作 | 调用工具 |
|--------|------|----------|
| LLM 需要具体参数值 | 获取 Methods 引用全文 | `zotero_get_item_fulltext` |
| LLM 需要具体数据/图表 | 获取 Results 引用全文 | `zotero_get_item_fulltext` |
| LLM 需要详细对比 | 获取 Related Work 高相关文献全文 | `zotero_get_item_fulltext` (按需) |
| 常规引用 | 使用摘要 | `zotero_get_item_metadata` |

## 6. 错误处理与 Fallback

| 场景 | 处理方式 |
|------|----------|
| zotero_get_item_fulltext 返回 "No attachment" | 调用 `zotero_get_item_metadata` 获取摘要 |
| zotero_get_item_fulltext 返回空内容 | 调用 `zotero_get_item_metadata` 获取摘要，记录警告 |
| Token 限制 | 优先保留 required fulltext，optional 可延迟 |

> 注：PDF 下载和转换由 zotero-mcp 的 `get_item_fulltext` 工具内部处理。

## 7. 日志示例

```
[reference-manager] 精确匹配: 3 篇
  - ASDQ9VBA: 强制全文 ✓ (zotero_get_item_fulltext 成功)
  - BQRT8XCK: 强制全文 ⚠ (无PDF，回退到摘要)
  - XY789LMN: 强制全文 ⚠ (zotero_get_item_fulltext 返回空，回退到摘要)

[reference-manager] 语义检索: 10 篇
  - 强制全文 (Methods引用): 2 篇 ✓
  - 可选全文 (Related Work): 5 篇
  - 摘要: 3 篇

[paper-writer] Methods 撰写
  - 调用 zotero_get_item_fulltext: 2 篇
  - token 充足，额外获取 optional: 2 篇
```

## 8. 待实现功能

- [ ] 修改 `reference-manager/SKILL.md` 实现分层获取策略
- [ ] 修改 `paper-writer/SKILL.md` 添加全文触发逻辑
- [ ] 添加日志记录 fulltext 获取状态
- [ ] 后续版本：按问题2/3 的多方法综合策略

## 9. 后续版本规划

问题2选项（后续综合考虑）：
- A) 精确匹配
- B) 包含匹配
- C) DOI 匹配

问题3选项（后续综合考虑）：
- A) 固定阈值
- B) LLM 自主判断
- C) 按章节分配（当前实现）

# Changelog

## [v2.1.0] - 2026-01-24

### Added
- **分层全文获取策略**: reference-manager 技能现在区分精确匹配文献（强制获取全文）和语义检索文献（按章节分配优先级）
- **章节级全文触发**: paper-writer 技能根据写作章节（Methods/Results/Related Work）决定是否需要调用 `zotero_get_item_fulltext`
- **新增输入字段**: `sections_for_fulltext`, `fulltext_status`, `sections_cited`

### Changed
- **Processing Steps**: 明确要求 LLM 始终调用 fulltext 工具获取精确匹配文献的全文
- **Output Format**: 添加 fulltext_status 标签（强制全文/可选全文/摘要）
- **Fulltext Trigger Rules**: 新增章节级全文获取规则表格

### Fixed
- 修复 LLM 跳过 `zotero_get_item_fulltext` 调用的问题

### Technical
- PDF 下载和转换逻辑由 zotero-mcp 的 `get_item_fulltext` 工具内部处理
- 无 PDF 时自动 fallback 到摘要

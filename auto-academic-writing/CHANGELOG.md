# Changelog

## v2.2.2 (2026-01-24)

### Features

- **academic-write command**: Integrated superpowers workflow for academic writing
  - **brainstorming**: Explore requirements, propose 2-3 writing approaches, validate design section-by-section
  - **writing-plans**: Generate detailed TODO list with acceptance criteria
  - **executing-plans**: Execute chapter-by-chapter with review checkpoints
- **Enhanced workflow**: Chapter review checkpoints, content coverage checks, citation matching verification

### Changes

- **academic-write.md**: Complete rewrite with integrated superpowers workflow
  - Step 0: Superpowers integration
  - Step 1: Read requirements file
  - Step 2: Brainstorming (understanding, approach exploration, design validation)
  - Step 3: Generate writing plan
  - Step 4: Execute plan (reference-manager → fulltext fetch → paper-writer → review)
  - Step 5: Compile and output

### Breaking Changes

- New workflow: Questions before writing, not after
- Chapter-by-chapter review checkpoints

---

## v2.2.1 (2026-01-24)

### Features

- **paper-writer**: Restored full scientific writing capabilities
  - IMRAD structure with Chinese paper support (摘要/关键词/第X章)
  - Citation styles: APA/AMA/Vancouver/IEEE/Chicago
  - Reporting guidelines: CONSORT/STROBE/PRISMA/STARD/TRIPOD/ARRIVE/CARE/SPIRIT
  - Figures/tables guidelines and best practices
  - Field-specific terminology (biomedical, molecular biology, chemistry, physics)
  - Journal-specific formatting support
  - Two-stage writing process detailed
  - Error handling for missing fulltext

### Documentation

- Added `CHANGELOG.md` for version tracking

---

## v2.2.0 (2026-01-24)

### New Features

- **Section-based fulltext retrieval workflow**: Parse requirements document, extract references by section, and fetch fulltext for semantic matching
- **Semantic paragraph matching**: Match content points with reference paragraphs (not headings) using semantic similarity
- **Primary template selection**: First reference in each section used as primary template for writing
- **Dual format support**: Support both structured template and inline reference formats

### Changes

- **reference-manager**: Completely rewritten for section-based document parsing
  - New input format: `requirements_doc` field with full markdown content
  - New output format: Section structure + reference table (no fulltext content)
  - Added reference extraction from both template format (`### 参考文献`) and inline format (`参考文献：...`)
  - Added JSON output for downstream paper-writer consumption

- **paper-writer**: Refocused on section-by-section writing with semantic matching
  - New input format: Structured JSON with `paper_title`, `sections[]`, `content_points[]`, `references[]`
  - Workflow: Fetch fulltext → Parse paragraphs → Semantic match → Write prose
  - Removed fulltext content from input (fetch on-demand per section)
  - Simplified to core academic writing capabilities

### Documentation

- Added `2026-01-24-section-based-fulltext-retrieval-design.md` design document
- Added requirements document template

### Bug Fixes

- Fixed fulltext retrieval enforcement (now mandatory for all referenced papers)
- Fixed citation format consistency

### Breaking Changes

- Input format changed from `requirement + outline + references` to `requirements_doc`
- Output format changed from full paper to section-by-section JSON
- Reference fulltext no longer included in output (fetched by paper-writer on-demand)

---

## v2.1.0 (2026-01-23)

### Features

- Added tiered fulltext retrieval strategy
- Fulltext required for exact-matched references
- Optional fulltext for semantic-matched references by section priority

### Changes

- Updated reference-manager SKILL.md with fulltext status tags
- Updated paper-writer SKILL.md with fulltext trigger logic

---

## v2.0.0 (2026-01-22)

### Features

- Initial release with Zotero MCP integration
- Reference search and management
- Basic academic writing workflow

---
name: academic-write
description: 根据需求文件启动学术写作流程
---

# Academic Write Command

## 使用方式

`/academic-write <path_to_requirement_file>`

## 执行流程

### Step 1: 确认需求文件

1. 读取用户提供的文件路径
2. 验证文件存在
3. 调用 `requirement-parser` 技能解析
4. 返回解析结果摘要

### Step 2: 用户确认

- 显示解析结果摘要
- 等待用户确认或修改
- 用户确认后继续

### Step 3: 执行写作流程

调用 `academic-writing-workflow` 技能，传递解析后的需求数据

### Step 4: 返回结果

- 输出文件路径
- 显示摘要统计

## 示例

```
/academic-write ./research-requirements.md
```

## 响应示例

```
**需求文件确认**

文件路径: ./research-requirements.md

**已解析需求:**

- 标题: Deep Learning for Image Classification
- 主题: CNN architectures for image recognition
- 字数: ~2000
- 风格: academic
- 参考文献: 3 篇

**建议行动:**
- [确认] 开始生成写作大纲
- [修改] 返回修改需求
```

# Example Queries

## 1) 概念型综述
```bash
./scripts/run_lookup.sh "Find papers on causal representation learning for healthcare time-series" 5
```

## 2) 方法核查
```bash
./scripts/run_lookup.sh "What methods are used for uncertainty estimation in clinical ML models?" 6
```

## 3) 争议分析
```bash
./scripts/run_lookup.sh "Evidence for and against scaling laws in small-domain scientific corpora" 5
```

## 4) 带过滤器
```bash
./scripts/run_lookup.sh \
"Transformer-based recommendation methods" \
5 '{"item_type":"journalArticle"}'
```

## 5) 快速模式（节省上下文）
```bash
./scripts/run_lookup.sh "Diffusion models for inverse problems" 3
```

## 6) 深挖模式（覆盖更多文献）
```bash
./scripts/run_lookup.sh "Benchmark design flaws in LLM evaluation" 8
```

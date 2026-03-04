# 🎡 环球影城年卡回本追踪

追踪北京环球影城悠享年卡（¥1688）的回本进度。

## 架构

纯静态站，数据在构建时从 Notion 拉取并写入 HTML。部署到 Cloudflare Pages。

- `src/index.html` — 模板（含 `__DATA__` 占位符）
- `build.py` — 从 Notion 拉数据，替换占位符，输出到 `dist/`
- `dist/index.html` — 构建产物（自动生成，不要手动编辑）

## 构建

```bash
python3 build.py
```

需要 `~/clawd/secrets/notion.json` 里有 Notion API key。

## 部署

Cloudflare Pages：Build output directory = `dist`，Build command = `python3 build.py`

## 回本计算

净回本 = 门票节省金额 − 园内额外花费（餐饮/停车/商品等）

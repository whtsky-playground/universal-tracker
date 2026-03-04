# 🎡 环球影城年卡回本追踪

追踪北京环球影城悠享年卡（¥1688）的回本进度。

## 架构

- `src/index.html` — 前端（纯 HTML/CSS/JS）
- `functions/api/data.js` — Cloudflare Pages Function（代理 Notion API）

## 部署

1. Cloudflare Pages 连接此 repo
2. 构建设置：Build output directory = `src`
3. 环境变量：`NOTION_KEY` = Notion Integration API Key

## 回本计算

净回本 = 门票节省金额 − 园内额外花费（餐饮/停车/商品等）

# 调研执行手册

## 来源优先级

1. 官方文档、规范、架构白皮书
2. 大厂工程博客与生产实践（Google、Meta、Netflix、Uber、字节、阿里、腾讯、蚂蚁、华为、CNCF 项目博客）
3. GitHub 仓库本身（star、贡献者、发布节奏、issue 响应、license、生产案例）
4. 基准测试、论文、会议分享（含 QCon 等工程会议）
5. 第三方分析报告（只作背景，不作为技术证据）

## 检索式模板

- `<topic> architecture` / `<topic> 架构设计`
- `<topic> vs <alternative>`
- `<topic> production case study` / `<topic> 生产实践`
- `<topic> benchmark` / `<topic> 性能测试`
- `site:github.com <topic>` + 按 star 排序
- `site:engineering.<company>.com <topic>`
- `site:qcon.infoq.cn <topic>`
- `QCon <topic> 架构` / `QCon <topic> 生产实践`
- `<topic> 选型 踩坑` / `<topic> 迁移`

## QCon（InfoQ）探索

QCon 是 InfoQ 主办的技术大会，议程、Track 与演讲页可作为中文工程实践与生产案例来源，适合智能研发、平台中间件、可观测、架构演进等主题。

**入口与 URL 规律**：

- 官网首页：https://qcon.infoq.cn/
- 届次日程：`https://qcon.infoq.cn/<year>/<city>/schedule`
  - 例：2026 上海 https://qcon.infoq.cn/2026/shanghai/schedule
  - 往届同样适用：2025 北京/上海、2024 上海等
- Track：`https://qcon.infoq.cn/<year>/<city>/track/<id>`
- 演讲详情：`https://qcon.infoq.cn/<year>/<city>/presentation/<id>`

**探索步骤**：

1. 先看目标届次的 schedule，按主题/关键词筛选候选 session，记录标题、讲者、公司、Track、年份与城市。
2. 打开 presentation 页，提取摘要、关键架构、量化指标、落地规模与踩坑；如有 PPT/视频，记录链接。
3. 优先采用大厂生产实践与有量化数据的 session；厂商软文式分享只作线索，不作技术证据。
4. 关键结论至少与官方文档或第二个独立来源交叉验证。
5. 引用时写明 session 标题、讲者/公司、届次（年/城市）与访问日期。

**限制**：QCon 演讲以经验分享为主，版本与时效性需核对；部分内容需登录或仅现场可见。不要把议程标题当作已证实的技术结论。

## GitHub 评估清单

| 维度 | 看什么 |
|---|---|
| 活跃度 | 近 6 个月提交、release 节奏、issue/PR 响应时间 |
| 社区 | star、fork、贡献者数量与集中度（是否一人维护） |
| 成熟度 | 版本号、breaking change 频率、生产案例 |
| 生态 | 插件、SDK、集成、文档质量 |
| 治理 | license、基金会归属（CNCF/ASF）、商业支持 |
| 风险 | 单点维护、license 变更史、与现有栈的耦合 |

## 证据表（边查边填）

| 结论 | 证据 | 来源 | 日期 | 置信度 |
|---|---|---|---|---|
| 例：方案 A 支持多租户 | 官方文档"Multi-tenancy"章节 | URL | 2026-10 | 高 |

## 对比维度（中间件 / 可观测 / 智能研发通用）

功能覆盖、架构与扩展性、性能与容量、稳定性与多租户、可运维性、生态与集成、总拥有成本、安全与合规、厂商锁定风险、团队适配度。

评分建议：每个维度 1-5 分并写权重；分数必须能回溯到证据，不要只给结论。

## 图片获取

- 优先官方文档中的 architecture diagram、comparison matrix
- 下载后确认文件可打开、分辨率足够、图中文字可读
- 记录：原图 URL、获取日期、license/使用条款
- 下载失败：保留外链 + 图注（说明"原图见链接"）
- 不摆放来源不明的图；不用生成图冒充官方架构图；自绘图必须标注"自绘"
- **图注格式**：每张图统一为 `图 <章节号>-<序号>：<标题>`；章节号取图所在最小小节编号（如 2.1.2），序号在该小节内从 1 递增
- **Markdown 呈现**：除 Mermaid 外，图片默认用 `[图注](本地相对路径)` 链接放入正文，相对路径优先按工作区根目录书写（如 `docs/research/images/<topic>/xxx.png`）；若用户要求预览可见，则用内嵌图片 `![图注](images/<topic>/xxx.png)`。两者都不使用绝对路径；只有下载失败时才使用远程外链并标注“原图链接”。Mermaid 用 `mermaid` 代码块直接渲染

## 参考链接整理

- 正文保留内联引用，所有来源统一汇总到第五章“参考链接”。
- 按来源类型分组（内部材料、各产品官方文档、图片与版权）。
- 每条来源保留标题、URL、访问日期；图片注明路径、来源、获取日期和版权/许可。
- 不在前四章末尾重复列“本章来源”或其他分散来源清单。

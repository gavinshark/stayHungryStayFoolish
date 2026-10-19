# 调研执行手册

## 来源优先级

1. 官方文档、规范、架构白皮书
2. 大厂工程博客与生产实践（Google、Meta、Netflix、Uber、字节、阿里、腾讯、蚂蚁、华为、CNCF 项目博客）
3. GitHub 仓库本身（star、贡献者、发布节奏、issue 响应、license、生产案例）
4. 基准测试、论文、会议分享
5. 第三方分析报告（只作背景，不作为技术证据）

## 检索式模板

- `<topic> architecture` / `<topic> 架构设计`
- `<topic> vs <alternative>`
- `<topic> production case study` / `<topic> 生产实践`
- `<topic> benchmark` / `<topic> 性能测试`
- `site:github.com <topic>` + 按 star 排序
- `site:engineering.<company>.com <topic>`
- `<topic> 选型 踩坑` / `<topic> 迁移`

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
- **Markdown 呈现**：除 Mermaid 外，图片默认用 `[图注](本地相对路径)` 链接放入正文，相对路径优先按工作区根目录书写（如 `docs/research/images/<topic>/xxx.png`）；若用户要求预览可见，则用内嵌图片 `![图注](images/<topic>/xxx.png)`。两者都不使用绝对路径；只有下载失败时才使用远程外链并标注“原图链接”。Mermaid 用 `mermaid` 代码块直接渲染

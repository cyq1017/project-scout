# 商机发现 Skill Prior-Art Map

生成时间：2026-05-28T10:44:13+08:00

## 执行摘要

本次围绕“商机发现 / business opportunity discovery skill”做了一轮 formal gate 样例调研，共纳入 15 个候选。候选覆盖三类：

- 已有 agent skill：创业想法验证、产品发现、Reddit 机会研究、机会树。
- 开源项目：startup idea validator、business idea validator、Xiaohongshu 商机分析工具。
- 产品形态：从 GitHub、社区、RSS、Twitter/X 等信号中发现产品机会的商业化产品。

当前结论是：**可以自研，但不应该从空白开始自研**。

更准确的建议是：**Write New + Borrow**。已有候选已经覆盖“创业想法验证”“市场调研”“竞品分析”“社区信号挖掘”的局部能力，但没有看到一个同时覆盖以下目标的开源 skill：

- prior-art / competitive map
- 多源搜索覆盖度记录
- 明确 blind spots
- 中国平台信号，例如小红书、公众号、中文社区
- build / adopt / borrow / fork / plugin 类型决策
- 可被 Codex、Claude、Hermes 等不同 agent 复用的 search adapter 协议

决策置信度：**Low**。原因是本地 `npx skills find` 在本次环境里挂起/失败，虽然用 web 和 GitHub fallback 补了候选，但 skills registry 不能算完整覆盖。

覆盖置信度：**Low**。这份报告适合作为公开样例和方向判断，不适合作为“已经搜尽”的最终结论。

## 搜索摘要

| 来源 | 查询 | 结果数 | 纳入数 | 状态 | 备注 |
| --- | --- | ---: | ---: | --- | --- |
| skills | `npx skills find "business opportunity discovery"` | 0 | 0 | failed | 本地 npm/npx skills registry 命令挂起或失败；改用 web fallback 补充 skill 候选。 |
| web | `business opportunity discovery AI agent skill startup idea validation GitHub; site:skills.sh opportunity discovery skill; startup idea validation skill` | 30 | 8 | ok | 用公开 web 结果补充 skill、产品和项目候选。 |
| github | `startup idea validation` | 10 | 4 | ok | 找到多个人工智能创业想法验证项目。 |
| github | `market research agent` | 10 | 1 | ok | 找到市场调研 agent 方向候选。 |
| github | `business idea validation` | 10 | 3 | ok | 找到 business idea validator 方向候选。 |
| github | `opportunity discovery agent` | 1 | 1 | ok | 找到 name-level match 的 Opportunity Discovery Agent。 |
| manual | 已知候选与上一轮 quick scan 结果 | 4 | 4 | ok | 纳入用户讨论中已出现的候选。 |

## 覆盖矩阵

| 来源 | 状态 | 纳入数 | 说明 |
| --- | --- | ---: | --- |
| Skills registry | failed | 0 | `npx skills find` 未成功完成；这会降低覆盖置信度。 |
| Web / 产品页 / skill 索引页 | ok | 8 | 覆盖到 EliteAI.tools、skills.sh、learn-skills.dev、Fulcrum、OSSIdeas 等。 |
| GitHub | ok | 9 | 覆盖 startup validator、business validator、XHS 商机分析、ODA 等项目。 |
| Manual candidates | ok | 4 | 纳入已知候选，避免重复搜索遗漏。 |

未覆盖或未充分覆盖：

- Product Hunt
- Hacker News 深度讨论
- Reddit 原帖与评论
- V2EX
- 小红书真实内容检索
- 微信公众号
- 电商评论
- 招聘站和岗位需求
- 论文数据库

## 相似候选

| 候选 | Stars | 更新时间 | License | 语言 | Score | 建议 |
| --- | ---: | --- | --- | --- | ---: | --- |
| [startup-idea-validation](https://eliteai.tools/agent-skills/startup-idea-validation) | 163 | 2026-05-28 | MIT | Markdown | 0.432 | Write New |
| [Fulcrum](https://www.fulcrum.host/) | 0 | 2026-05-28 | unknown | unknown | 0.410 | Write New |
| [ferdinandobons/startup-skill](https://github.com/ferdinandobons/startup-skill) | 319 | 2026-05-26T14:42:28Z | MIT | unknown | 0.393 | Write New |
| [ailabs-393/ai-labs-claude-skills@startup-validator](https://agent-skills.md/skills/ailabs-393/ai-labs-claude-skills/startup-validator) | 0 | 2026-05-28 | unknown | Markdown | 0.392 | Write New |
| [onvoyage-ai/gtm-engineer-skills@reddit-opportunity-research](https://skills.sh/onvoyage-ai/gtm-engineer-skills/reddit-opportunity-research) | 0 | 2026-05-28 | unknown | Markdown | 0.392 | Write New |
| [igr290/XHS_Business_Idea_Validator](https://github.com/igr290/XHS_Business_Idea_Validator) | 5 | 2026-05-28T02:21:33Z | unknown | Python | 0.375 | Write New |
| [Nirikshan95/VettIQ](https://github.com/Nirikshan95/VettIQ) | 14 | 2026-05-17T07:45:41Z | MIT | Python | 0.357 | Write New |
| [OSSIdeas](https://ossideas.ai/) | 0 | 2026-05-28 | unknown | unknown | 0.355 | Write New |
| [nweii/agent-stuff@validating-startup-ideas](https://www.learn-skills.dev/en/skills/nweii/agent-stuff/validating-startup-ideas) | 0 | 2026-05-28 | unknown | Markdown | 0.338 | Monitor |
| [majiayu000/claude-arsenal@product-discovery](https://skills.sh/majiayu000/claude-arsenal/product-discovery) | 0 | 2026-05-28 | unknown | Markdown | 0.336 | Monitor |
| [mxvsh/prove](https://github.com/mxvsh/prove) | 3 | 2026-03-15T17:44:16Z | unknown | TypeScript | 0.318 | Monitor |
| [codechan-dev/ai-business-validator](https://github.com/codechan-dev/ai-business-validator) | 1 | 2026-04-26T06:45:41Z | unknown | Python | 0.318 | Monitor |
| [thim81/ost-builder@opportunity-solution-tree-builder](https://skills.sh/thim81/ost-builder/opportunity-solution-tree-builder) | 3 | 2026-05-28 | unknown | Markdown | 0.317 | Monitor |
| [bhagwadG/oda](https://github.com/bhagwadG/oda) | 1 | 2026-03-02T01:58:10Z | unknown | Python | 0.282 | Monitor |
| [Pranavharshans/ThinkTank-AI](https://github.com/Pranavharshans/ThinkTank-AI) | 8 | 2026-04-12T16:12:48Z | unknown | Python | 0.262 | Monitor |

说明：这里的 `Write New` 不是“完全从零写”，而是表示当前最高相似候选仍不足以直接 adopt/fork/integrate。更实际的执行策略是：**自研主协议，借鉴多个候选的局部能力**。

## 重叠矩阵

| 候选 | 关键词 | 技术/生态 | 用户 | 排除项 | Score |
| --- | ---: | ---: | ---: | ---: | ---: |
| startup-idea-validation | 5 | 0 | 2 | 0 | 0.432 |
| Fulcrum | 2 | 3 | 1 | 0 | 0.410 |
| ferdinandobons/startup-skill | 3 | 1 | 1 | 0 | 0.393 |
| ailabs-393/ai-labs-claude-skills@startup-validator | 4 | 1 | 0 | 0 | 0.392 |
| onvoyage-ai/gtm-engineer-skills@reddit-opportunity-research | 4 | 1 | 0 | 0 | 0.392 |
| igr290/XHS_Business_Idea_Validator | 2 | 1 | 1 | 0 | 0.375 |
| Nirikshan95/VettIQ | 2 | 0 | 1 | 0 | 0.357 |
| OSSIdeas | 2 | 1 | 0 | 0 | 0.355 |
| nweii/agent-stuff@validating-startup-ideas | 1 | 0 | 1 | 0 | 0.338 |
| majiayu000/claude-arsenal@product-discovery | 1 | 1 | 0 | 0 | 0.336 |
| mxvsh/prove | 1 | 0 | 0 | 0 | 0.318 |
| codechan-dev/ai-business-validator | 1 | 0 | 0 | 0 | 0.318 |
| thim81/ost-builder@opportunity-solution-tree-builder | 1 | 2 | 0 | 0 | 0.317 |
| bhagwadG/oda | 1 | 0 | 1 | 0 | 0.282 |
| Pranavharshans/ThinkTank-AI | 1 | 0 | 0 | 0 | 0.262 |

## 值得借鉴

- [startup-idea-validation](https://eliteai.tools/agent-skills/startup-idea-validation)：借鉴 9 维验证框架、证据质量分层、GO/NO-GO 阈值、风险假设优先验证。
- [Fulcrum](https://www.fulcrum.host/)：借鉴“从噪音到机会”的定位，以及 Reddit、HN、GitHub Issues、RSS、Twitter/X 多源信号扫描和反证审查。
- [ferdinandobons/startup-skill](https://github.com/ferdinandobons/startup-skill)：借鉴 startup validation、competitive intelligence、pricing analysis 等模块拆分方式。
- [onvoyage-ai/gtm-engineer-skills@reddit-opportunity-research](https://skills.sh/onvoyage-ai/gtm-engineer-skills/reddit-opportunity-research)：借鉴 Reddit 作为单一社区信号源的专门 adapter 思路。
- [igr290/XHS_Business_Idea_Validator](https://github.com/igr290/XHS_Business_Idea_Validator)：借鉴小红书数据用于发现用户需求和市场机会的中文平台方向。
- [OSSIdeas](https://ossideas.ai/)：借鉴从开源仓库趋势反推创业机会、商业化路径和竞品洞察的产品思路。
- [majiayu000/claude-arsenal@product-discovery](https://skills.sh/majiayu000/claude-arsenal/product-discovery)：借鉴 problem-first、outcome-driven、assumption testing 的产品发现原则。
- [thim81/ost-builder@opportunity-solution-tree-builder](https://skills.sh/thim81/ost-builder/opportunity-solution-tree-builder)：借鉴 Opportunity Solution Tree 作为输出结构，但不把它当作搜索层。

## 需要避免

- 不要只做“创业想法打分器”。这类 skill 已经很多。
- 不要只做“idea validator”。我们的差异应该在发现机会之前的搜索覆盖、prior-art、盲点声明和证据链。
- 不要把它做成爬虫平台。默认 local-first，不存 token，不保存 cookie，不自动操作账号。
- 不要把社交平台登录态当作默认能力。小红书、公众号、Reddit 等都应该是可选 adapter，并明确平台风险。
- 不要让 LLM 直接拍板。LLM 可以辅助摘要，但评分、覆盖记录和推荐理由要尽量结构化。
- 不要把“有差异化”当作结论。真正有用的是：这个差异是否对应明确用户、明确场景、明确证据源。

## 建议与置信度

建议：**Write New + Borrow**。

具体含义：

- 自研一个新的商机发现 skill 主协议。
- 借鉴已有 skill 的验证框架、机会树、社区信号、竞品分析模块。
- 不直接 fork 单一候选，因为没有一个候选同时覆盖 prior-art map、搜索覆盖度、blind spots、中国平台信号和跨 agent search adapter。

决策置信度：**Low**。

置信度低不是因为方向弱，而是因为本轮 skills registry adapter 失败，且多个高价值来源还没正式覆盖。更稳妥的下一步是做第二轮 formal gate，重点补：

- skills registry 成功查询
- Reddit / HN 原帖
- V2EX / 小红书 / 公众号
- Product Hunt
- 招聘站需求信号
- 电商评论和 SaaS review sites

## 覆盖置信度与盲点

覆盖置信度：**Low**。

停止原因：本轮已经比较可用候选，并记录了来源状态；但不是 exhaustive search。

已知盲点：

- `npx skills find "business opportunity discovery"` 本地执行失败，skills registry 不能算完整覆盖。
- 社区来源没有进入原帖和评论级别分析。
- 中文平台仅通过 GitHub/XHS 项目间接覆盖，没有直接检索小红书或公众号内容。
- 商业产品候选只覆盖公开搜索结果，没有覆盖 Product Hunt、G2、Capterra、AppSumo 等产品目录。
- 没有做论文和市场研究文献检索。

## 有用定位

不要把新 skill 定位成：

> AI 帮你判断创业想法好不好。

这个定位已经拥挤，而且容易滑向主观打分。

更有用的定位是：

> 在开始做产品、skill、plugin 或 roadmap 前，系统性发现已有实现、社区痛点、竞品、中文平台信号和需求代理指标，并输出带覆盖置信度的商机地图。

建议命名方向：

- `opportunity-scout`
- `market-signal-scout`
- `business-opportunity-scout`
- `opportunity-prior-art-scout`

核心差异：

- 先发现机会，再验证想法。
- 先记录搜索覆盖，再给建议。
- 先列出 blind spots，再谈信心。
- 面向 agent skill，可被 Codex、Claude、Hermes 等复用。

## 风险与未知

- 直接使用小红书、公众号、Reddit 等平台可能涉及登录态、风控、平台条款和数据合规问题。
- 多源信号容易引入噪音，需要定义证据等级和反证搜索。
- 商机发现很容易变成“确认偏误机器”，必须默认寻找反证。
- 如果没有明确目标用户，报告会变成泛泛的市场研究。
- 如果不做 source profile，agent 每次都会临时决定搜哪里，结果不稳定。
- 当前候选元数据仍需人工复核 license、维护状态和实际 skill 结构。

## 建议 ADR / Backlog / Skill 更新

- ADR：记录为什么不直接 adopt/fork 单一候选，而是自研主协议并借鉴 `startup-idea-validation`、`Fulcrum`、`startup-skill`、`XHS_Business_Idea_Validator` 等候选。
- Backlog：新增 `market_opportunity` source profile。
- Backlog：新增社区信号 adapter 设计，覆盖 Reddit、HN、V2EX、小红书、公众号。
- Backlog：新增“证据等级 + 反证搜索” rubric。
- Backlog：新增公开样例：用该 skill 分析一个真实商机方向。
- Backlog：把 machine JSON 和中文 Markdown 的关系写进 report contract，避免以后生成样例时语言不一致。

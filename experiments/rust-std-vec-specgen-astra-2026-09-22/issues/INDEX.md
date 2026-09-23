# Vec 转换的当前问题

| 记录 | 范围 | 当前情况 |
|---|---|---|
| [vec-index-source-correspondence](vec-index-source-correspondence.md) | 泛型 Vec Index、继承的 index_req/caller 属性及关联输出 | 当前源入口新编译通过 1 个义务，默认聚合通过 4 个义务，实际委托为 Vec Deref 和切片 Index；新原生程序 8 项及客户端 8 个义务通过。真实单目标 analyze/reexecute 均在关联返回观察处报告 observation_gap，没有比较、查询或完整性义务，正式测试仍失败，本 API 未计完成。入口命名冲突、首次重放范围错误和 caller 属性遗漏的实测失败均保留；后两项已按原语义修正并只重查受影响部分。未改固定工具或原泛型域，独立确认待进行。 |
| [into-iter-consumers-source-correspondence](into-iter-consumers-source-correspondence.md) | IntoIter 的 count、last，当前剩余状态及真实 Iterator 绑定 | 两个 API 均未完成。任务 `12969919776e` 已独立确认有限源码对应、count 的 1 个源码义务、last 的原 mut self 拒绝及真实绑定的重复 Iterator 实现；两目标 analyze/reexecute 仍失败。现补入仅限 last 隔离证明副本的最小规范化提案、按值/借用/Drop 对应义务及两个待答选项，尚未授权或执行。真实绑定仍须另解；原候选、全部旧失败及默认聚合保留。局部等待不阻塞原清单中共享 `Index<I>::index` 的后续检查，不代表新增 API 已通过。 |
| [vec-with-capacity-source-correspondence](vec-with-capacity-source-correspondence.md) | with_capacity 的原表达式、官方契约复用、Global 构造及构建隔离 | `6611f73cab83` 已确认有限源码/cfg/const/泛型域、无冗余及固定 Verus 的 Global 构造限制，不是 Rust 缺陷或所有编码不可能的结论。当前默认聚合实际编译成功、3 个义务通过；独立候选仍引用原体，source/candidate 编译均退出 1，真实 analyze/reexecute 均退出 2、零通过义务、无原始 SMT，完整序列比较未变。六项候选配置差异及新构建隔离待独立审阅；首次隔离检查为 8/9，stdout 名称断言已改为实际 AIR/SMT 对应，修改项与覆盖范围两项单独通过，其余未变检查未重跑。原 Global-only、五项原生行为及全部旧失败记录保留，未改写原表达式或新增假设，两轨仍未完成。 |
| [vec-reused-basic-source-correspondence](vec-reused-basic-source-correspondence.md) | Default、is_empty、Deref 三个已有官方契约的原体入口 | `af05f6b80c5a/round-0001.json` 已独立确认官方契约复用、有限源码对应、const 边界、冗余检查及双轨结果。独立原生重跑缺少 cc，另已核对工程侧当轮新构建与七项运行记录；旧失败保留，未变代码不重审。 |
| [source-body-embedding](source-body-embedding.md) | 四个 AsRef/AsMut 源码函数体的独立证明入口 | 已提交的 `fc975bfe5a6c/round-0001.json` 确认四个源码对应、正确性及冗余删减，并确认两个 AsRef 的双轨结果；未变契约不重新审查。 |
| [vec-owned-source-body-embedding](vec-owned-source-body-embedding.md) | 数组和装箱切片移入 Vec 的两个原表达式、原条件及官方委托 | `db4ff3669ca5/round-0001.json` 已独立确认源码对应、原配置、冗余检查和双轨结果。原生独立重跑缺少 cc，另已核对工程侧新构建与运行记录；旧发现不足及测试失败全部保留，未变代码不重审。 |
| [specdet-mutable-return](specdet-mutable-return.md) | `AsMut<Vec<T,A>>`、`AsMut<[T]>` | 删减后的本轮分析和重新执行仍在生成完整性问题前拒绝返回可变引用；全部旧失败保留，不计入双轨通过数量。 |
| [cow-source-body-embedding](cow-source-body-embedding.md) | Cow 四个直接 From 的原表达式和透明枚举观察 | 任务 `4566f129a548` 的独立审阅已确认源码对应、原签名域、透明观察、四个非零正确性义务及无冗余；完整性未完成。 |
| [specdet-cow-lifetime-type](specdet-cow-lifetime-type.md) | 四个 `Cow<'a,[T]>` 返回值 | 直接路径的解析失败已有独立确认。本轮源码及组件对照未找到契约不变的受支持入口，且现有 Cow 观察未登记；工具修改须管理者另行授权，新判断待独立审阅。无比较、查询或完整性证明，不计双轨完成。 |

这里只记录本实验的本地问题。没有向外部仓库提交问题；公开提交仍需授权。
当前结果路径及私有输出目录的重放方式见
[inventory/COVERAGE.md](../inventory/COVERAGE.md)。
环境恢复不等于独立语义确认；项目内
[临时冗余准则](../review-criteria-temporary.txt) 继续适用于当前及后续审查。

## 清单复跑的分区冲突

以下为此前 `closure-engineer` 轮的历史记录；本轮未修改该生成器或重跑未变清单检查。

本轮实际执行源码清单测试时，21 项中只有
`test_persisted_outputs_equal_fresh_extraction` 失败；单独执行
`bash scripts/with_baseline.sh python3 scripts/inventory_source.py --check`
也报告 `inventory/submodules.md` 与重新提取结果不一致。
原始输出保留在 `inventory/closure-engineer/source-tests.log`、
`source-check.stderr` 和 `source-check.exit-code`。
vstd 清单的 27 项测试通过，见 `inventory/closure-engineer/vstd-tests.log`。

原因是 `scripts/inventory_source.py` 生成整个 Markdown 文件，
而 `scripts/inventory_vstd.py` 在同一文件追加有明确起止标记的独立段落。
前者的比较没有区分两者的写入范围，正常生成还会删除后者。
拟仅让源码生成器替换自身的前半部分，逐字保留 vstd 段落及其后文；
vstd 段落仍由原有 vstd 检查验证，不能借此忽略源码清单的差异。
回归测试将覆盖重新生成时保留后文、检测源码部分差异和拒绝损坏的分区标记。
此修复不改变 API 身份、输入域、规格、证明函数体或任何上游程序。

已按上述范围修复。源码清单的 23 项测试通过，两个生成器的 `--check`
也均通过，分别记录在 `inventory/closure-engineer/source-tests-fixed.log`、
`source-check-fixed.log` 和 `vstd-check.log`。原来的失败输出继续保留；
没有重新生成或改写两份 API 数据清单，也没有修改 vstd 的独立段落。

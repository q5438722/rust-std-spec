# Cow 返回类型中的生命周期被当作类型解析

这是本项目对固定 specdet 0.3.0 的 `checker-limitation` 记录。
任务 `4566f129a548` 的独立审阅已通过实际 analyze、replay --reexecute
和解析对照确认当前直接提取路径的失败；这不证明所有等价编码都不可行。
没有修改检查器或缩窄 API，没有向外部仓库提交问题；本地记录不是上游已确认缺陷。

四个当前真实绑定位于 `specs/cow/conversions.rs`，均原样返回 `Cow<'a,[T]>`，
保留 `T: Clone`、数组 const 泛型、借用寿命和默认分配器。
权威源码及 docstring 分别为
`/home/chentianyu/nanvix-rust-std-spec-survey/rust-1.96/library/alloc/src/vec/cow.rs:6-53`；
对应说明见 [源码对应记录](cow-source-body-embedding.md)。
固定工具为官方 Verus `release/0.2026.09.20.aef82ed`、其配套 vstd、
项目私有 Rust 1.98.1 和未修改的 specdet 0.3.0。

四个原表达式各已验证一个正确性义务并编译；去除额外 where 条件后，聚合也编译通过。
因此下面的失败不是 Rust 类型检查或 Verus 源体证明失败。

## 本次实际诊断

`proofs/completeness/cow/cow-engineer/analyze.json` 中四个目标均报告：

```text
stage: observations
code: type_gap
message: Cannot parse source type: "'a"
verdict: not_evaluated
baseline: null
proofs: []
```

实际输入快照和逐目标契约保存在
`proofs/completeness/cow/cow-engineer/analysis-runs/20260922T113813Z-1aa027dfd4/`。
例如移动 Vec 入口的
`targets/e613e9e0b4d0c19df1723877/revisions/0/contract.json`
将返回值记录为 `Cow<'a, [T]>`，但把 `"'a"` 放入 `return_type.type_args`，
并标记为 `kind = unknown`。原始源文件、泛型和无前置条件的后置条件仍完整保留。
没有产生观察式、原始求解查询或完整性证明；不能用总退出码或构建成功替代这三者。

当前检查器的 `adapters/verus/native/extract/extractor.py:99-115`
把泛型参数节点逐一放入类型参数列表，没有将生命周期分开；
随后
`/home/chentianyu/spec-determinism-tool/src/specdet/adapters/verus/type_context.py:513-551`
对这些参数逐一按类型解析，实际失败于生命周期参数。
这说明当前输入在观察构造之前被拒绝；它不证明修正该解析后，外部 Cow 的枚举观察
必然可被解析或完整性必然通过。独立审阅已经确认 `CowObservation` 的透明源码关系
与原 `T: Clone` 输入域，且没有发现四条单等式契约应删的逻辑冗余；
该语义结论不能替代尚未生成的原生比较和查询。

## 重新执行与未采用的办法

实际命令分别保存在本目录结果的 `analyze.command.json` 和 `replay.command.json`。
再次执行使用同一快照：

```sh
bash scripts/with_baseline.sh env TMPDIR=/private/scratch/tmp \
  /home/chentianyu/spec-determinism-tool/.venv/bin/specdet replay \
  --run /path/to/the/saved/analysis-run --reexecute \
  --verus "$PWD/toolchains/verus-x86-linux/verus" \
  --out /private/scratch/replay-runs --json
```

不传新的 `--config`，让原生 replay 复用保存的四目标选择。
最初传入无 selector 的配置副本，导致 replay 额外执行四个未变借用目标；
那次输出和运行目录仍保留，不能将这些额外执行解释为新的独立审查。
`proofs/completeness/cow/check.py` 已改为复用原选择。
本轮收到的 `cow-exact-completeness` 完成通知对应的正是这次旧执行：
`.argus_subagents/cow-exact-completeness.json` 属于任务 `4566f129a548`，
其包装进程虽退出为 0，`.argus_subagents/cow-exact-completeness_logs/stdout.log`
仍明确记录 analyze 和 replay 均退出为 2，且 replay 扩展到八个目标。
它不是本轮新的通过结果；当前检查脚本已要求同样四目标，并对不完整结果返回 2。
Reviewer 应使用 `run_review_command`，在 `{scratch}` 中配置 TMPDIR 和输出，
并以相同 command_id 调用 `get_review_command`，不向源输入写入。

曾尝试为绑定显式写出由 blanket impl 满足的
`Cow<'a,[T]>: CowObservation<T>`，但固定 Verus 的精确 trait-bound 检查拒绝了它。
旧候选和完整诊断留在 `proofs/correctness/cow/cow-engineer/candidate/`、
`aggregate.stderr`；当前已删除该条件。
不以 `'static`、额外 T bound、替代返回值、假枚举、手写成功查询或检查器补丁绕过失败。
检查器对人工改变的类型模型也只给出需批准且不可信的转换，
见其 `adapters/verus/backend.py:667-688`；没有将这条路径冒充原契约的可信分析。

四个 Cow 的完整性和独立双轨确认仍未完成。后续先亲读固定 checker 的类型提取、
类型解析、观察选择、可信转译入口和对应测试，判断是否存在保留原签名及完整观察的
已实现编码；不盲试别名、不手改保存的类型模型，也不原样重跑已失败的全量分析。
当前授权不包含修改、复制修补或部署 checker、Verus/vstd、canonical Rust 或 Argus。

上一工程轮全量 unittest 实际运行 31 项，其中 30 项通过；完整性检查的四个 Cow 子测试失败，
原始输出见 `tests/cow-engineer/full-suite/stderr.log`。
该轮新编译的六项原生测试、十个预期编译拒绝及七个观察/From 客户端义务均通过。
没有将完整性失败改写为测试通过。

## 固定原生入口的源码检查

本轮亲读的工具源码均位于
`/home/chentianyu/spec-determinism-tool/src/specdet/`，没有修改或复制修补工具。
以下判断限于固定 0.3.0 已实现的原生入口、四个现有真实绑定及当前允许的输入域；
不是对所有 Rust 表达方式或未来检查器的不可行性证明。

实际调用顺序是
`analysis/pipeline.py:358-390` 的提取、观察、转译，再到证明生成；
观察阶段返回之前不会保存观察或进入转译。
`adapters/verus/backend.py:522-568` 从原声明调用 `extract_spec`，
`native/extract/extractor.py:1352-1356` 调用 `_extract_return_type`，
后者在 `305-350` 行调用 `_parse_type_node`。
`99-115` 行把 `Cow<'a, [T]>` 的生命周期节点和 `[T]` 一同装入 `type_args`。
随后 `backend.py:703-711,754-784` 调用 `_resolved_function`，
经过 `type_context.py:612-628` 的 `resolve_function_types`，
在 `513-551` 行递归处理每个 `type_args`；
`_type_node` 用 `type __TypeContext = 'a;` 尝试解析，因而报错。
原生两种输出策略、具体及抽象确定性分析都在选择比较前调用这一步。

| 已实现入口 | 实际语义及其对本任务的限制 |
|---|---|
| 源码类型别名 | `type_context.py:478-505,529-547` 能区分别名声明的生命周期、类型和 const 参数，但展开目标后仍调用 `_parse_type_node` 并递归 `resolve`。透明别名若仍展开为原 `Cow<'a,[T]>`，就重新生成相同的生命周期子项；没有试写别名候选。 |
| `parse_input_type` | `type_context.py:129-142,221-237` 的另一套 `TypeExpr` 解析保留完整 `raw` 注解，同时不把生命周期放进类型子项。它不是 `_resolved_function` 的替代入口；`backend.py:875-885` 中抽象输入选择发生在返回观察之后。 |
| 来自 trait bound 的自定义 `view` | `type_context.py:753-780` 只从原函数泛型、where 和 trait 上下文收集已有约束，不从 blanket impl 推导新约束。原绑定只有 `T: Clone`，没有 `Cow<'a,[T]>: CowObservation<T>`。不能把已被 Verus 拒绝的附加 where 条件重新放回绑定。 |
| 源码 impl 和原生预置观察 | `native/view/impl_scanner.py:271-335` 识别固有 `view` 或所列 `View` 等 trait，不登记 `CowObservation` 的 trait impl。`native/view/prelude.py:80-166` 没有 Cow 规则；不能借用丢失变体、要求元素 View 的官方 Cow View。 |
| 显式接受的视图映射 | `native/view/registry.py:344-381` 有底层 L4 接口，但 `backend.py:713-752` 固定传入空 `accepted_views`。`backend.py:2068-2108` 的观察建议只接受已命名策略及抽象输入，不接收任意输出比较或视图声明。底层辅助函数存在不等于真实 CLI 已支持。 |
| 提取或类型模型建议 | `backend.py:648-688` 只有与原提取模型完全相同的建议才直接接受；任何不同模型需要批准，且仍不可信。`568-583` 行在再次提取时重新计算这种信任。手工删掉保存模型中的生命周期不是可信转译。 |
| 源码准备和独立生成器 | `proposal_validation.py:46-80` 只把无解析缺口且保持程序 token 的编辑判为忠实；这不能改变生命周期节点的类别。直接调用生成器也不能代替 CLI：`backend.py:895-921` 在转译前重新计算原观察，拒绝替换比较。 |

因此，调整后置条件表达式并不能跳过真实返回类型的解析。
在上述已实现入口内没有找到同时保持原绑定、全部寿命和类型域、
Borrowed/Owned 及完整有序 Seq 的受支持编码。
本轮没有变更规格表达式、构造新的别名候选、手改保存模型或运行新的全量分析。

## 本轮原生组件对照

`tests/cow-encoding/inspect_native_support.py` 只读取本问题所列 `from_vec`
原契约和其原生源码上下文，再调用固定工具的 `parse_input_type`、
`bound_views` 和 `ViewRegistry`。它不调用替代生成器，不转译模型，
不产生比较或查询；调用前后的整个函数模型保持相同。
实际结果保存在 `proofs/completeness/cow/native-support/inspection.json`：

```text
return_type.name = Cow<'a, [T]>
generics = <'a, T: Clone>
helper_type_syntax.raw = Cow<'a, [T]>
source_bound_views = {}
scanned_view_impls = []
accepted_views = []
registry_resolution.layer = uncovered
registry_resolution.rationale = no L1/L2/L3/L4 rule for Cow (kind=generic)
model_unchanged = true
```

这区分了“辅助语法解析可用”和“原生输出观察已支持”，没有把前者当作贯通检查。
组件对照还确认当前 `CowObservation` 未被登记。
`backend.py:804-816` 在构造比较前拒绝无来源语义的外部未知返回类型；
仅修正生命周期分类并不能据此声称完整 Cow 观察已经可用。
这是当前源码和未修改组件的证据，不冒称已经运行了修复解析后的 CLI。

本轮还通过固定工具的既有 unittest 实际执行了 47 项定向测试。
范围为 `tests/test_type_context.py` 的别名、bound view 和真实类型语法，
`tests/test_native_mechanical.py` 的真实声明提取和显式视图，
`tests/test_backend_models.py` 的未知类型拒绝、模型来源约束及不可信类型建议，
以及 `tests/test_backend_proposals.py` 的源码 token 与信任判断。
命令、退出码和完整输出分别为
`proofs/completeness/cow/native-support/native-tests.command.json`、
`native-tests.exit-code` 和 `native-tests.stderr`；47 项通过，退出码为 0。
已有 VAddr fixture 的类型解析警告保留在日志中。
这些是检查器支持范围的测试，不是四个 Cow 的完整性证明。
没有重跑未变 Rust 构建、Cow 绑定测试、借用证明或收集器；
没有新的可宣称通过的 Cow 双轨结果。
`proofs/completeness/cow/native-support/coverage-check.json` 另外确认覆盖表仍为
138 行，只有四个 Cow 行的独立结论字段变化，其余 134 行逐字相同，
全部原证明及完整性结果字段均未改变。

## 需要另行授权的最小工具范围

当前停止在工具授权边界，仍需正常独立 Reviewer 核对本轮源码路径和组件结果，
随后由管理者另行安排工具工作。本任务未提交、实施或部署工具补丁。

需要授权的第一部分是原生类型提取及解析：
`adapters/verus/native/extract/extractor.py` 与
`adapters/verus/type_context.py` 必须正确区分生命周期实参和类型实参，
同时保留原注解、泛型声明、返回寿命及借用关系。
不能通过只删除字符串、改成静态寿命或修改既存运行的 JSON 来修复。
相应测试至少覆盖含生命周期的真实返回类型、透明别名、嵌套类型及现有 const 参数。

第二部分是让原生观察层从已存在、可调用且适用于原 `T: Clone` 域的透明定义，
建立真实 Cow 的变体加完整序列比较。
当前相关范围是 `type_context.py` 的来源证据、
`native/view/impl_scanner.py` / `registry.py` 和
`backend.py` 的未知类型检查与观察构造；生成器仅在确需保留准确调用形式时受影响。
这不是批准任意观察映射、新假设或更大的可信基础。
修复生命周期解析后仍须实际验证该部分，不能预先计为已支持。

工具变化经授权与独立审查后，先用 `from_vec` 原绑定运行真实 CLI，
检查原生比较、查询和非零义务，再接回四个现有目标及
`proofs/completeness/cow/check.py`，重跑受影响两轨与独立确认。
独立执行继续使用 `run_review_command` / `get_review_command`，
所有输出和 TMPDIR 位于 `{scratch}`；不能改比较目标或写入只读输入。
没有新编码，因而本轮没有需要证明的规格表达式等价替换。

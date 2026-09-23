# Rust 1.96 Vec 的源码与当前证明覆盖

## 泛型 Index 的源码证明成立，完整性仍缺少关联输出观察

`specs/vec/index.rs:9-22` 复用现有官方绑定，不重复登记标准库规格。
入口保留任意 T、`I: SliceIndex<[T]>`、`A: Allocator` 和原关联输出；
共享接收者具名后仍执行 `Index::index(&**vec, index)`。
完整契约包括 trait 继承的 `vec.index_req(&index)`，以及存在同内容切片的
`call_ensures` 后置条件。原 impl 的 inline 和 trait 继承的 track_caller
也保留，没有额外元素 trait、静态寿命、具体索引限制或观察假设。

当前源码及聚合分别在
`proofs/correctness/vec/generic-index/caller-preserved-source/` 和
`caller-preserved-aggregate/` 新编译成功，退出 0，分别为 1 和 4 个通过义务。
前者的实际中间表示只经 Vec Deref 与切片 Index 委托，不调用目标 Vec Index
假设来证明自身。先完成单独入口编译，才接入默认模块及 target include；
with_capacity 的独立入口和 IntoIter 候选不变。

当前真实 analyze 和 `replay --reexecute` 均只选择同一泛型入口，
均退出 2，在 `&<Vec<T, A> as Index<I>>::Output` 处报告 observation_gap。
没有比较式、完整性 harness、SMT 查询或通过义务，不能以客户端或具体实例代替。
完整输入及结果在 `proofs/completeness/vec/generic-index/caller-preserved/`。
固定工具的有限只读调查未找到不新增约束的原生关联输出观察路径；没有修改工具。

要求的完整 unittest 已实际执行：10 个方法中 9 个通过，完整性方法的两个
子项失败，整条命令退出 1，见 `tests/vec-index/suite.stderr`。
首次入口命名冲突、第一次重放范围误选以及遗漏 caller 属性的实际失败均保留。
修正 caller 属性后只重跑受影响的五个方法，全部通过，见
`tests/vec-index/caller-suite.stderr`；当前新程序的 8 项原生测试和
8 个 source/std 客户端义务通过。24 个精确返回类型与接收者寿命拒绝探针
已经执行且符合预期，临时源文件删除，其未变检查未重跑。
原生测试覆盖源码公开支持的 24 类索引、完整内容和顺序、空范围、ZST、
非静态元素、不可 Clone 的借用分配器、安全 panic 及原 trait 的调用位置行为。
最终更新的源码副本、完整契约及单目标重放对应检查通过，正式完整性断言仍失败；
三项定向检查记录于 `tests/vec-index/final-evidence-suite.stderr`。

`coverage.tsv` 仍有 **138** 行，仅更新 Index，其余 **137** 行与
`tests/vec-index/before/coverage.tsv` 逐字段不变；独立双轨完成仍为 **7/138**。
本 API 尚未完成，仍需正常独立源码确认与对上述限制的判断。
精确来源、历史失败、当前命令和 `run_review_command` 私有目录执行方式见
[泛型 Index 说明](../issues/vec-index-source-correspondence.md)。
该方式将 TMPDIR 和全部输出转入 `{scratch}`，保留原 selector、源码副本与
观察要求；当前及后续 Reviewer 继续使用项目内 `review-criteria-temporary.txt`。

## IntoIter 的 count 和 last 保留为未完成候选

两条新候选观察调用开始时的当前 `IteratorSpec::remaining`，不将构造时的
`into_iter_elts` 当作消费后不变量。count 规定精确剩余长度，last 规定完整
None/Some 及末项 T；任意 T、A:Allocator、Item=T、按值接收者和两个原表达式保留。
候选暂存于 `proofs/correctness/into_iter/isolated/consumers.rs`，
辅助分段 trait 声明位于相邻 `iterator_methods.rs`，未覆盖官方其他方法契约。

本轮固定 Verus 在 `proofs/correctness/into_iter/erased-count/` 新编译 count
源体并通过 1 个义务，IR 只调用继承的 len。last 的原 `mut self` 被前端拒绝，
无契约的最小复现也失败。独立真实绑定另因重复 Iterator 实现而编译失败；
没有把源码证明当作真实绑定已经成功。

`proofs/completeness/into_iter/selected-targets/{analyze,replay}.json` 中，
真实 analyze 和 replay --reexecute 均恰好选择两个具体目标，均退出 2，
各目标均为编译错误、零通过义务，没有原始 SMT 查询。完整 usize 与
Option<T> 比较、源码快照、泛型和唯一后置条件均保留。
两个 API 都未完成；依赖及继承的 len 不新增 API 计数。

要求的完整 unittest 已实际执行并失败。修正工程侧 ghost 消除后，只检查了
受影响和新增的 5 项，全部通过；新原生程序的 6 个用例通过，十个拒绝探针的
原结果保留。last 的原生库仅由固定 rustc 编译，不是 Verus 源码证明；
8 个组合客户端仍被真实绑定错误阻断。原失败、最新源库及各项命令见
[源码对应和限制说明](../issues/into-iter-consumers-source-correspondence.md)。

`coverage.tsv` 仍为 138 行，只改变 count/last 两行，其余 136 行逐字段不变；
独立双轨完成数仍为 7/138。由于真实绑定和 last 源入口未编译成功，
没有将候选移入 `specs/into_iter/consumers.rs`，也没有改动默认聚合和配置。
未重跑与本次变化无关的七个已确认目标、with_capacity、Cow 或 AsMut 工作。
任务 `12969919776e` 已独立确认有限源码对应、count 的源码结果及两个具体
工具限制，未确认 last 源码证明、真实绑定或双轨完成。本次只在既有 issue
补入尚未授权的 last 隔离副本规范化提案和待答选项，并确认共享
`Index<I>::index` 可作为不依赖此决定的后续检查对象；没有新增通过结果，
`coverage.tsv` 和全部候选保持不变。项目内临时规格冗余准则继续适用。

## with_capacity 的限制已独立确认，构建隔离仍待审

`specs/vec/with_capacity.rs` 沿用官方
`toolchains/upstream/source/vstd/std_specs/vec.rs:114-123` 的空序列契约，
保留原 `with_capacity_in(capacity, Global)` 表达式，只明确 `Self = Vec<T>`。
完整 usize 输入域、任意 T、默认分配器、const 签名和原 OOM 配置条件均保留。
没有新增标准库假设，也没有增加容量后置条件。
源文档和必要委托已亲读，精确位置及有限对应见
[with_capacity 源码说明](../issues/vec-with-capacity-source-correspondence.md)。

任务 `6611f73cab83` 已独立确认有限源码对应、cfg/const/泛型输入域、
唯一契约无逻辑冗余，以及固定 Verus 在契约求解前拒绝原 Global 构造的限制。
这不是 Rust 缺陷，也不是所有可能编码均不可行的证明。本轮新增的构建隔离
仍待独立审阅；工程执行记录不代替该判断，with_capacity 的两轨仍未完成。

### 当前入口与实际隔离记录

默认 `specs/lib.rs` 保留 `allocator_api` 和全部非容量模块，只移除
`pub mod with_capacity` 及 `const_heap, const_trait_impl`；默认 `specdet.toml`
只从 `targets.include` 移除 `vec/with_capacity.rs`，其他设置和目标不变。
新入口 `specs/with_capacity_candidate.rs` 保留原三项 feature，并以
`pub mod vec { pub mod with_capacity; }` 引用同一份 `specs/vec/with_capacity.rs`。
原 cfg、泛型、const 签名、函数体、契约及 `vec::with_capacity` 命名空间未变；
逐 API 源入口和 Global-only 最小复现也未修改。这是分离默认构建与失败候选，
不是从 API 清单删除困难目标或把候选换成另一份实现。

完整性脚本先调用未改动的 `scripts/borrowed_scratch_config.py`，仅作原四项
路径调整：`project.root`、`adapters.verus.executable`、
`adapters.verus.environment.TMPDIR`、`artifacts.output_dir`。
随后按本轮明确授权另设 `build.entrypoint = "with_capacity_candidate.rs"` 和
`targets.include = ["vec/with_capacity.rs"]`。最终配置共有 **六项** 解码差异，
不是“仅四个路径”，也不与默认目标集合相同；准确记录在
`proofs/completeness/vec/with-capacity/isolation/checker/config-changes.json`。
真实 analyze 仍显式选择 `--target vec/with_capacity.rs`，重放仍为 `--reexecute`。

| 本轮保存的实际执行 | 观察到的结果及证据 |
|---|---|
| 默认聚合固定 Verus `--compile`，无 `--verify-*` 过滤 | 退出 0，`3 verified, 0 errors`，是 reused_basic 的三个源体义务；`proofs/correctness/vec/with-capacity/isolation/default/aggregate.{command.json,result.json,stdout,stderr}` 及当次新生成的 `libvec_specs.rlib`。 |
| 原逐 API 入口与独立候选入口的 `--compile` | 两次均退出 1，保留原 opaque Global 构造错误，没有 Verus 库；`proofs/correctness/vec/with-capacity/isolation/candidate/{source,candidate}.*`。`tests/with-capacity/isolation/regression/candidate-build.result.json` 记录包装脚本退出 1。 |
| 候选真实 analyze 和 replay --reexecute | 两次恰好选择 `vec/with_capacity.rs::vec::with_capacity::with_capacity`，各退出 2，`compile_error`、0 个通过义务、无原始 SMT；完整比较仍为 `(r1)@ =~= (r2)@`。记录在 `proofs/completeness/vec/with-capacity/isolation/checker/`，`tests/with-capacity/isolation/regression/candidate-checker.result.json` 记录包装脚本退出 1。 |
| 未改动的 reused-basic 检查脚本 | 通过默认 `lib.rs` 分析并重新执行，恰好选择 default/is_empty/deref，每个目标每阶段实际验证 1 个义务，查询为 `unsat`，两个 CLI 及包装脚本均退出 0。记录在 `proofs/completeness/vec/reused-basic/isolation/checker/` 和 `tests/with-capacity/isolation/regression/reused-basic.*`；只作连接回归，不重新授予三项 API 语义确认。 |
| 接入独立候选的客户端 | `tests/with-capacity/isolation/regression/clients.*` 记录退出 1，仍是原 Global 构造错误；不是客户端成功。 |

构建脚本现在检查 source 和 candidate，而非 source 和默认聚合；每项仍要求
实际编译成功且恰好 `1 verified, 0 errors`，否则非零退出。完整性脚本执行并
保存两个阶段的失败，不因第一个失败而跳过重放；即使工具返回 0，也拒绝空目标
或零证明义务。未来成功标准未放宽。`tests/test_with_capacity.py` 只调整入口、
路径和快照对应，原正式成功断言保留，未改成 skip/expectedFailure，也未在本轮
重跑整份 API 套件或宣布其通过。

新隔离套件首次执行为 **9 个方法中 8 个通过、1 个失败**，见
`.argus_subagents/vec-capacity-isolation-a8d858022146_logs/stderr.log`。
唯一失败是默认构建测试要求 stdout 含 `vec::reused_basic::default`，
而实际 stdout 只有 `verification results:: 3 verified, 0 errors`。
已将函数对应检查改为读取实际 `vec__reused_basic-final.air` 中的三个
`Function-Def` 和三个 `check-valid`，并要求 SMT 记录恰有三个 `check-sat`
和三个 `unsat`，没有删除源体身份要求。随后仅重跑修改的默认构建测试及已更新的
覆盖范围测试，两项均通过，见 `tests/with-capacity/isolation/selected-tests.stderr`
及同名 `.command.json`、`.result.json`。新默认编译和义务记录在
`proofs/correctness/vec/with-capacity/isolation/default-obligations/`，
首次运行及全部旧输出原样保留。其余未变检查没有重跑；这不是新的一次九项整套运行，
也不代表 with_capacity 双轨通过。

`coverage.tsv` 仍为 **138** 个 API，独立双轨完成仍为 **7/138**。
本轮只更新 with_capacity 一行；其余 **137** 行与
`tests/with-capacity/isolation/before/coverage.tsv` 逐字、逐字段一致。
Cow、AsMut、此前 const/cfg 失败及独立环境缺少 `cc` 的记录全部保留；
本轮不重跑原生行为、不处理 cc 环境，也不继续调查 Global 兼容编码。

### 当前入口的私有目录复查命令

两个脚本的当前调用形式为
`bash scripts/with_baseline.sh python3 proofs/correctness/vec/with-capacity/build.py <new-private-dir>`
和
`bash scripts/with_baseline.sh python3 proofs/completeness/vec/with-capacity/check.py <new-private-dir>`。
每次必须选用尚不存在的新私有目录，不覆盖上述任何证据。当前预期两个包装脚本
都返回 1；这是保留失败，不是放宽它们未来的成功要求。

受限独立 Reviewer 先读取 [项目临时冗余准则](../review-criteria-temporary.txt)，
使用 `run_review_command`，运行中用同一命令编号的 `get_review_command`。
以下命令在项目目录运行；每个示例使用不同的、尚未占用的 `{scratch}` 子目录。
TMPDIR 的 `env` 必须放在 `with_baseline.sh` 后面；日志和编译输出也全部私有。
这是待执行的独立复查入口，不声称工程方已完成独立审阅。

```sh
S='{scratch}/with-capacity-build-check'
test ! -e "$S" || exit 1
mkdir -p "$S/tmp" "$S/default/logs" || exit 1
bash scripts/with_baseline.sh env TMPDIR="$S/tmp" \
  toolchains/verus-x86-linux/verus specs/lib.rs \
  --edition=2021 --crate-type=lib --crate-name vec_specs --compile --num-threads=1 \
  --trace --log-all --log-dir "$S/default/logs" -o "$S/default/libvec_specs.rlib" \
  > "$S/default/aggregate.stdout" 2> "$S/default/aggregate.stderr"
default_code=$?
bash scripts/with_baseline.sh env TMPDIR="$S/tmp" \
  python3 proofs/correctness/vec/with-capacity/build.py "$S/correctness" \
  > "$S/candidate-build.stdout" 2> "$S/candidate-build.stderr"
source_code=$?
bash scripts/with_baseline.sh env TMPDIR="$S/tmp" \
  python3 proofs/completeness/vec/with-capacity/check.py "$S/completeness" \
  > "$S/candidate-checker.stdout" 2> "$S/candidate-checker.stderr"
checker_code=$?
printf 'default=%s source=%s checker=%s\n' "$default_code" "$source_code" "$checker_code" \
  > "$S/exit-codes.txt"
test "$default_code" -eq 0 && test "$source_code" -eq 0 && test "$checker_code" -eq 0
```

默认直接命令没有验证过滤器；候选任一失败仍会收集后续结果，最终返回非零。
也可在另一个全新输出根执行限定的隔离套件，五个输出变量缺一不可：

```sh
S='{scratch}/with-capacity-isolation-suite'
test ! -e "$S" || exit 1
mkdir -p "$S/tmp" || exit 1
bash scripts/with_baseline.sh env TMPDIR="$S/tmp" \
  CAPACITY_ISOLATION_OUTPUT="$S/regression" \
  CAPACITY_AGGREGATE_OUTPUT="$S/default" \
  CAPACITY_PROOF_OUTPUT="$S/correctness" \
  CAPACITY_COMPLETENESS_OUTPUT="$S/completeness" \
  CAPACITY_REUSED_OUTPUT="$S/reused-basic" \
  python3 -m unittest discover -s tests -p test_with_capacity_isolation.py -v \
  > "$S/suite.stdout" 2> "$S/suite.stderr"
suite_code=$?
printf '%s\n' "$suite_code" > "$S/suite.exit-code"
exit "$suite_code"
```

该入口实际执行默认构建、原逐 API/候选构建、候选与 reused-basic 的 analyze/
reexecute 及客户端检查，保留预期的真实失败，不写源输入；不包含本轮禁止重跑的
原生行为或 cc 环境检查。当前已保存的套件失败如上，不将命令可执行性当作审查通过。

### 隔离前的原体证明和原生补充记录

以下保留上一工程轮的执行、候选及失败；其中聚合入口是当时尚含 with_capacity
的 `specs/lib.rs`，不描述上面的当前默认入口。

| 隔离前实际执行 | 结果和记录 |
|---|---|
| 逐 API 入口和聚合的固定 Verus `--compile` | 均退出 1，拒绝原体中的 opaque Global 构造；没有已通过源体义务或 Verus 库。`proofs/correctness/vec/with-capacity/const-features/` 保存命令、输入、日志和中间表示。 |
| 真实 specdet analyze 和 replay --reexecute | 恰好选择本入口，生成完整 Vec 序列比较，但均因同一构造编译失败，已通过义务为零，原始 SMT 查询尚未生成。`proofs/completeness/vec/with-capacity/const-features/` 保存两次实际执行。 |
| 同一原体的原生编译与行为检查 | 固定 Rust 1.98.1 新编译源入口、聚合和测试程序；五项用例通过，另有八个预期拒绝探针及 const/cfg 边界检查。`tests/with-capacity/const-features/` 明确将原生编译与失败的 Verus 编译分开。 |

两个中间表示实际只调用官方 with_capacity_in，输入容量没有改动，也没有调用
目标 with_capacity 的假设。Global-only 最小复现在固定 Verus 下失败、
原生 Rust 编译成功，排除了 Vec 契约和 const 调用作为该诊断的必要触发条件。
没有据此修改固定 vstd 的 opaque 声明或将构造藏入新的信任边界。
这种工具限制和有限源码对应随后获 `6611f73cab83` 独立确认；
原生成功仍不替代任何一轨证明。

两次检查器输入保留完整泛型、参数、返回类型、空前置条件及唯一后置条件，
比较是 `(r1)@ =~= (r2)@`。同一候选及当时七份源码快照已机械核对；
当时的私有配置仅改变四个路径。虽然生成了七个搜索条件模式，编译失败发生在原始
查询生成之前，不能声称关闭这些条件的查询已经执行，更不能报告不可满足。
容量、分配器身份、物理地址、分配失败和溢出路径均不在该正式序列观察中。

原生用例包括非静态且无额外 trait 的元素、0/1/37 请求、填满后的内容顺序和
既有容量、ZST 的 `usize::MAX` 请求，以及必定在分配前失败的字节上界和乘法溢出。
没有把容量当作长度、强加非零请求的精确容量或尝试耗尽内存。
真实标准库的稳定 const 调用被拒绝；开启 const_heap 后的零请求和 ZST 求值通过。
源体还需宿主的 const_trait_impl；自由函数不重新发布 libstd 的稳定性属性。
禁用全局 OOM 处理时，源入口实际被排除，不推断预编译标准库也改变了配置。

首次函数外层 cfg 导致检查器未发现目标；移为同条件的文件内层 cfg 后已修复发现。
首次原生编译缺少 const_trait_impl；仅补全 feature 后重新执行受影响的两轨和
此前尚未执行的测试。全部旧候选和失败保留。
完整 unittest 的日志是 `tests/with-capacity/suite-const-features.stderr`：
15 个测试方法内仍有五个正式成功断言因 Global 限制失败。
另一个仅由 IR 输出换行引起的断言已修正，并单独通过 `suite-lowering.stderr`；
没有重跑未变工作，也没有将整份测试写成成功。

上一工程轮的 `coverage.tsv` 仍有 **138** 行，当时只更新 with_capacity 和三个基础入口的
已审字段，其余 **134** 行逐字段不变，见
`tests/with-capacity/const-features/coverage-changes.json`。
独立双轨完成仍为 **7/138**；with_capacity 未计入，Cow 和 AsMut 的未完成情况不变。
原生 Rust 编译通过不满足本任务要求的非零 Verus 源体义务。

### 隔离前的只读重新执行命令（历史）

以下原命令作为历史尝试保留，不是本轮重跑全 API/原生检查的指令；
脚本当前已改接独立候选，当前入口和新私有输出要求以上节为准。

独立审阅继续读取 [本项目临时冗余准则](../review-criteria-temporary.txt)，
通过 `run_review_command` 执行；运行中仅用同一命令编号的 `get_review_command`。
管理工具使用宿主机路径。以下命令在项目目录运行，输出和 TMPDIR 均进入
私有 `{scratch}`，不写只读源输入、不更换比较目标。
由于当前正式检查确实失败，逐项保存退出码并继续收集其余结果，最后仍返回失败：

```sh
S='{scratch}/with-capacity'
mkdir -p "$S/tmp"
bash scripts/with_baseline.sh env TMPDIR="$S/tmp" \
  python3 proofs/correctness/vec/with-capacity/build.py "$S/correctness"
source_code=$?
bash scripts/with_baseline.sh env TMPDIR="$S/tmp" \
  python3 proofs/completeness/vec/with-capacity/check.py "$S/completeness"
checker_code=$?
bash scripts/with_baseline.sh env TMPDIR="$S/tmp" \
  CAPACITY_PROOF_OUTPUT="$S/correctness" \
  CAPACITY_COMPLETENESS_OUTPUT="$S/completeness" CAPACITY_TEST_OUTPUT="$S/tests" \
  python3 -m unittest discover -s tests -p test_with_capacity.py -v
test_code=$?
printf 'source=%s checker=%s tests=%s\n' "$source_code" "$checker_code" "$test_code"
test "$source_code" -eq 0 && test "$checker_code" -eq 0 && test "$test_code" -eq 0
```

原生库由固定 Rust 编译器另行新建，记录明确标注它不是 Verus 成功输出。
若独立容器缺少 `cc`，应单列链接失败并核对本轮工程侧的新构建及运行记录；
不能以旧程序替代，也不在本任务内开展环境维护。

## Default、is_empty 和 Deref 已获独立确认

`specs/vec/reused_basic.rs` 复用三条固定官方契约，保留 `Vec::new()`、
`self.len() == 0` 和 `self.as_slice()`，只将接收者改为对应的具名共享参数。
没有新增标准库绑定或假设；真实标准库客户端仍使用官方声明。
任意 T、两个分配器泛型、Deref 的 `[T]` 关联类型和接收者寿命均保留。
这些验证入口不另计 API，表仍为 138 行。任务
`af05f6b80c5a/round-0001.json` 已确认三个目标的有限源码对应、官方契约复用、
const 边界、冗余检查和双轨结果，独立双轨确认数为 **7/138**。
本次只同步已提交的独立结论，不重审未变代码。独立原生重跑因容器缺少 `cc`
未能链接；审阅者另核对了工程侧当轮新构建和七项原生运行记录，没有将链接失败
写成独立运行通过。完整结论路径见对应的源码说明；以下保留该工程轮记录。

| 目标 | 源体正确性及本轮编译 | 真实完整性分析和重新执行的完整比较 |
|---|---|---|
| `Default::default<T>` | 1 个义务；只调用官方 `Vec::new` | 各 1 个义务；`(r1)@ =~= (r2)@` |
| `Vec::is_empty<T, A>` | 1 个义务；原 const 函数调用 `Vec::len`，使用其既有长度公理 | 各 1 个义务；`r1 == r2` |
| `Deref::deref<T, A>` | 1 个义务；只调用官方 `Vec::as_slice` | 各 1 个义务；`r1 =~= r2`，完整 slice 内容 |

三个逐 API 文件只导入同一源码入口，不复制另一份契约；构建命令使用
`--verify-only-module reused_basic --verify-function <name> --compile`。
`proofs/correctness/vec/reused-basic/source/` 保存准确命令、退出码、日志、
源码副本、中间表示和本轮新库。聚合 `specs/lib.rs` 实际验证三个义务并编译。
每个中间表示的函数体只调用表中的依赖，没有调用目标 Default、is_empty 或
Deref 假设。依赖自身、底层内存实现及不稳定 const trait 能力不计为本轮已证明 API。

`proofs/completeness/vec/reused-basic/engineer/analyze.json` 和 `replay.json`
各恰好选择三个入口。三个目标每次均有一个通过义务及不可满足的原始查询。
`coverage.tsv` 逐项指向真实生成的 harness、查询及观察记录，不以手写证明代替工具。
两次运行的六份源码快照与当前规格逐字相同。检查器输入的泛型、参数、返回类型、
全部前后置条件和官方 trait 条件的对应由
`tests/reused-basic/engineer/correspondence.json`、`checker-correspondence.json`
记录并机械核对；只允许命名空间、接收者变量以及无语义影响的空白和参数末尾逗号变化。
检查器没有结构化 const/trait 归属字段，故这两项另对照原源码、官方 trait 和编译探针，
不由独立自由函数的名称推定真实 API 身份。

Default、is_empty、Deref 原始查询分别关闭全部 5、7、7 个搜索开关；
没有要求输入为空，没有额外类型界限或其他附加前提。
Vec 的比较忽略既有 View 之外的表示，slice 比较涵盖完整有效内容，
不宣称容量、分配器身份、地址或全局堆状态的确定性。
工具未另做契约可满足性检查；原体证明与空、非空等合法原生调用是补充依据。

本轮实际执行了
`python3 -m unittest discover -s tests -p test_reused_basic.py -v`。
七项通过，包括本轮新编译程序的七个原生用例、六个官方/源码客户端义务、
十四个类型及借用拒绝探针、源码及检查器完整对应、当前中间表示和覆盖范围检查。
原生用例覆盖非静态且无额外 trait 的元素、不可 Clone 的借用分配器、空和预留容量的空向量、
单元素、重复及顺序敏感内容、完整有效前缀和 ZST；ZST 没有错误断言容量为零。
所有临时探针源文件已删除，输入和诊断仍保留。

首次 const 检查中的稳定 `is_empty` 编译已成功；后续不稳定 Default 探针因缺少
宿主要求的 `const_trait_impl` feature 失败。原日志和输入保留在
`tests/reused-basic/suite.*`、`engineer/unstable-default-enabled.*`。
只给该探针补全 `const_default, const_trait_impl`，随后单独执行改变的检查及
此前未执行的两个拒绝检查，三项均通过，见 `suite-const.*` 和 `const-boundaries/`。
没有重跑已通过且未变的检查。稳定运行时 Default、稳定 const is_empty、
不稳定 const Default 和普通 Deref 没有混为同一种能力。
原生执行使用固定 Rust 1.98.1，不据此宣称它与 Rust 1.96 的所有底层行为普遍等价。

`tests/reused-basic/engineer/coverage-changes.json` 确认仅五行变化：
这三个目标及两个所有权转换的已审字段；其他 133 行逐字段不变。
原借用、Cow、所有权转换模块与全部旧失败均保留，没有重新分析未变 Cow 或 AsMut。
首次 Verus 选项错误也保留在 `proofs/correctness/vec/reused-basic/engineer/`。
详细语义与失败说明见
[vec-reused-basic-source-correspondence.md](../issues/vec-reused-basic-source-correspondence.md)。

### 三个目标的只读重新执行

以下保留当次审阅的命令作为既有记录；本次不重新执行三个未变目标。

正常独立 Reviewer 先读取权威源码、共享及 OWN 指南，并应用
[本项目临时规格冗余准则](../review-criteria-temporary.txt)。
通过 `run_review_command` 执行；运行中只用同一命令编号的 `get_review_command`。
管理工具使用宿主机项目路径。以下命令在项目工作目录执行，
全部输出及 TMPDIR 都进入私有 `{scratch}`，不写只读输入、不改变比较目标：

```sh
set -e
S='{scratch}/reused-basic'
mkdir -p "$S/tmp"
bash scripts/with_baseline.sh env TMPDIR="$S/tmp" \
  python3 proofs/correctness/vec/reused-basic/build.py "$S/correctness"
bash scripts/with_baseline.sh env TMPDIR="$S/tmp" \
  python3 proofs/completeness/vec/reused-basic/check.py "$S/completeness"
bash scripts/with_baseline.sh env TMPDIR="$S/tmp" \
  REUSED_PROOF_OUTPUT="$S/correctness" \
  REUSED_COMPLETENESS_OUTPUT="$S/completeness" REUSED_TEST_OUTPUT="$S/tests" \
  python3 -m unittest discover -s tests -p test_reused_basic.py -v
```

构建脚本为三个原体及聚合实际传入 `--compile`；测试只链接这些命令新产生的库，
不以旧二进制替代编译。完整性脚本只调用原生 CLI；测试再检查实际目标集合、
全部契约、完整比较、关闭的搜索开关及非零验证记录。配置副本只改变既定四个路径。
若容器原生链接仍缺少 `cc`，应如实保留错误并核对本轮工程侧新构建记录，
不能把未执行的原生运行写成独立通过。

## 两个所有权输入转换已获独立确认

`specs/vec/owned_conversions.rs` 新增数组及装箱切片到 Vec 的真实 From 绑定，
并已接入原聚合及检查器目标清单。两个契约均无前置条件，只写
`result@ == s@`；任意元素、const 长度、分配器泛型及原配置条件不变。
原表达式、文档、官方委托和条件属性的对应见
[vec-owned-source-body-embedding.md](../issues/vec-owned-source-body-embedding.md)。
任务 `db4ff3669ca5/round-0001.json` 已确认两个目标的源码语义及双轨结果，
独立双轨确认数现为 **4/138**。本轮只更新它们的既有待审说明，不重跑未变代码。
审阅者新编译两个源体并完成真实分析和重新执行；原生重跑因容器缺少 `cc`
未完成，另核对了工程侧当轮新构建和七项运行记录，不能称为全部独立测试通过。
Cow、AsMut 及既有失败均保留，没有重跑旧兼容性调查或修改收集器。
以下详细构建和失败记录属于该所有权转换工程轮。

| 新增入口 | 原表达式正确性及编译 | 真实完整性分析和重新执行 |
|---|---|---|
| `from_array<T, const N: usize>` | 1 个义务通过，保留 `<[T]>::into_vec(Box::new(s))` | 两次各 1 个义务通过，原始查询均不可满足 |
| `from_boxed_slice<T, A: Allocator>` | 1 个义务通过，保留 `s.into_vec()` | 两次各 1 个义务通过，原始查询均不可满足 |

源体构建的命令、退出码、日志、中间表示和本轮新库位于
`proofs/correctness/vec/owned-conversions/`；当前聚合构建为
`aggregate-verus-module.*`。聚合仍包含借用和 Cow 模块，其零义务结果只算编译。
两个源体均不导入目标 From 假设，实际调用的是固定官方 Box、数组转换和
`into_vec` 契约。规格模块布局调整未改变这两个源体，因此没有重复编译未变源体。

当前真实分析和重新执行位于
`proofs/completeness/vec/owned-conversions/verus-module/analyze.json`、
`replay.json`，两个 CLI 退出码均为 0，且仅选择这两个新绑定。
`coverage.tsv` 逐项连接检查器原生生成的 Rust 证明、原始查询及观察文件。
两份源码快照与当前规格逐字相同；原泛型、移动参数和唯一后置条件均保留。
比较式为 `(r1)@ =~= (r2)@`，不是长度或地址比较。
数组原始查询的七个搜索开关、装箱切片的五个搜索开关均关闭；
没有搜索得到的附加前提、手工模型或替代比较。
这些结果只涉及完整有序内容，不证明容量、物理地址或分配器身份。

`tests/test_owned_conversions.py` 已在本轮实际执行。七个原生用例由
`tests/owned-conversions/engineer/native-build.*` 记录的新编译程序运行，
结果见同目录 `native-tests.stdout`。它们同时调用源体库和真实标准库绑定，
覆盖精确函数类型、泛型 const 长度、空输入、单元素、非空重复项及顺序、
ZST、无 Clone/Copy/View/Eq 的借用元素和无 Clone 的非静态自定义分配器。
对非空非 ZST 的装箱切片，还检查原指针、分配器持有的唯一资源、
转移期间没有分配或释放，以及最终恰好一次释放；不向数组要求原堆分配复用。
八个移后复用及元素借用逃逸探针均被预期的 Rust 诊断拒绝，
临时探针源文件已删除，输入及诊断仍保留。

当前规格布局下，默认配置的六个客户端义务及禁用全局 OOM 处理配置的
三个义务通过，见 `tests/owned-conversions/verus-module/`。
中间表示确认后一配置仅移除数组绑定，装箱切片绑定仍在。
首次整份测试执行的完整性检查失败后，只重跑有实质变化的布局、客户端和
完整性记录检查；没有把旧失败日志改成通过，也没有重跑未变原生用例。
最终原生记录检查见 `tests/owned-conversions/suite-native-results.stderr`；
私有配置仅改变四个路径的检查见 `suite-completeness-current.stderr` 中对应的通过项。
源体和聚合都在本轮使用固定 Verus 的 `--compile`，没有以旧二进制替代新构建。

首次直接条件属性和随后普通模块内嵌宏的两次遗漏数组记录分别保存在
`proofs/completeness/vec/owned-conversions/engineer/`、`module-cfg/`。
当前根级 Verus 块中的数组内联模块保留原条件，同时使真实扫描器识别两项。
既有候选快照、两次目标数不足的失败以及本地测试格式断言的修正记录全部保留。
覆盖表改前副本为 `proofs/correctness/vec/owned-conversions/coverage-before.tsv`。
逐字段比对及新证明路径核对见 `tests/owned-conversions/coverage-check.log`：
表仍为 138 行，仅两行改变，原聚合模块、原检查器设置及其余 136 行保持不变。

### 两个新增目标的只读重放

独立审阅继续使用 `run_review_command`；运行中通过同一个命令编号调用
`get_review_command`。管理工具使用本项目宿主机路径，以下命令在该工作目录执行。
先亲读共享和审阅者 OWN 指南，并应用
[临时冗余准则](../review-criteria-temporary.txt)。
所有输出和编译临时目录均放入私有 `{scratch}`；不改写只读源码输入或比较目标。

```sh
set -e
S='{scratch}/owned-conversions'
mkdir -p "$S/correctness/build" "$S/tmp"
for api in from_array from_boxed_slice; do
  code=0
  bash scripts/with_baseline.sh env TMPDIR="$S/tmp" \
    toolchains/verus-x86-linux/verus "proofs/correctness/vec/$api.rs" \
    --edition=2021 --crate-type=lib --crate-name "owned_$api" \
    --compile --num-threads=1 --trace --log-all \
    --log-dir "$S/correctness/$api" \
    -o "$S/correctness/build/libowned_$api.rlib" \
    > "$S/correctness/$api.log" 2> "$S/correctness/$api.stderr" || code=$?
  printf '%s\n' "$code" > "$S/correctness/$api.exit-code"
  test "$code" -eq 0 || exit "$code"
done
code=0
bash scripts/with_baseline.sh env TMPDIR="$S/tmp" \
  toolchains/verus-x86-linux/verus specs/lib.rs \
  --edition=2021 --crate-type=lib --crate-name vec_specs --compile --num-threads=1 \
  -o "$S/correctness/build/libvec_specs.rlib" \
  > "$S/correctness/aggregate.log" 2> "$S/correctness/aggregate.stderr" || code=$?
printf '%s\n' "$code" > "$S/correctness/aggregate.exit-code"
test "$code" -eq 0 || exit "$code"
bash scripts/with_baseline.sh env TMPDIR="$S/tmp" \
  python3 scripts/borrowed_scratch_config.py "$S/completeness"
python3 proofs/completeness/vec/owned-conversions/check.py "$S/completeness"
bash scripts/with_baseline.sh env TMPDIR="$S/tmp" \
  OWNED_PROOF_BUILD="$S/correctness/build" OWNED_TEST_OUTPUT="$S/tests" \
  OWNED_COMPLETENESS_OUTPUT="$S/completeness" \
  python3 -m unittest discover -s tests -p test_owned_conversions.py -v
```

`check.py` 只调用真实 analyze 和 replay，并核对两次恰好选择这两个绑定；
其输出不是自制完整性摘要。Python 测试进一步核对原生源码快照、泛型、
前置条件、完整序列比较、所有关闭的搜索开关以及实际非零验证记录。
如原生链接失败，应保留本次错误，不能转而运行旧程序。

## 已落实的借用独立结论

`/home/chentianyu/.argus-vec-specgen-astra-20260922/projects/s-6a17c286/handoffs/fc975bfe5a6c/round-0001.json`
已正式确认四个借用入口的源码对应、正确性和三条冗余条件的删除；
两个 AsRef 的内容完整性及重新执行也获确认。两个 AsMut 的完整性仍未完成。
`coverage.tsv` 的四个借用行据此更新，其他字段和旧失败记录不变。
借用部分独立双轨确认数为 **2/138**；加上已确认的两个所有权转换，当前为 **4/138**，
不将完整性未完成的 AsMut 或 Cow 计入。
下列借用工程轮的“等待独立审查”描述保留为历史记录，不再表示当前等待环境恢复。
本轮不重审未变借用契约、源体或收集器，也不重新生成已有 Cow 候选。

## 四个 Cow 的源码结论已独立确认，完整性仍受阻

任务 `4566f129a548` 的独立审阅已确认四个原表达式的有限源码对应、
原签名和合法输入域，以及 `CowObservation` 对真实枚举的透明匹配。
四个源体在私有 scratch 中重新编译，各有一个通过义务；聚合只算编译。
按 `review-criteria-temporary.txt` 检查，四条契约均无前置条件，
各自唯一的变体加完整序列等式没有应删的逻辑冗余。
独立 analyze 和 replay --reexecute 只选择同样四个 Cow 绑定，
均在构造观察前报告 `Cannot parse source type: "'a"`，没有比较、查询或完整性证明。

独立执行的 23 项定向测试中，22 项通过；剩余原生链接失败是容器缺少 cc，
没有用旧二进制替代。审阅者另核对了下列工程侧当轮新编译程序和六项原生测试记录。
本轮落实这些已提交的独立结论；以下构建、测试和收集器记录来自上一工程轮，
不冒充本轮重新执行，也不因执行能力已恢复而计入 Cow 双轨完成。

`specs/cow/observation.rs` 用透明的 `CowContents<T>` 同时保留 Borrowed/Owned
和完整 `Seq<T>`；`specs/cow/conversions.rs` 绑定四个真实 From 方法。
原生命周期、`T: Clone`、数组 const 泛型、默认分配器及
`not(no_global_oom_handling)` 条件均保留，没有新增元素类型界限或前置条件。
原表达式、官方依赖和初次失败候选见
[cow-source-body-embedding.md](../issues/cow-source-body-embedding.md)。

| 当前入口 | 本轮源码正确性和构建 | 实际完整性分析及重新执行 |
|---|---|---|
| `from_slice` | 1 个义务通过，并编译 | 生命周期参数解析失败；没有查询或证明 |
| `from_array` | 1 个义务通过，并编译 | 同上，原 const 泛型未删除 |
| `from_vec` | 1 个义务通过，并编译 | 同上，原返回生命周期未改为静态 |
| `from_vec_ref` | 1 个义务通过，并编译 | 同上，原 Vec 借用寿命不变 |

四个当前构建及其 `.command.json`、`.exit-code`、`.log`、`.stderr`、
Verus 中间表示和 `.rlib` 均在 `proofs/correctness/cow/cow-engineer/`。
当前聚合对应 `aggregate-inner-cfg.*`；其 `0 verified, 0 errors` 只计作编译。
最初加入额外 where 条件的失败聚合、随后精确签名的聚合，以及旧候选均仍保留。
四个源体只导入透明观察和官方 vstd，不导入目标假设；
保存的源体和观察文件与当前文件逐字相同。

`proofs/completeness/cow/cow-engineer/analyze.json` 和 `replay.json`
各选择同样四个真实绑定，均以退出码 2 结束。
四个返回类型中的 `'a` 被当作类型解析，实际错误为
`type_gap: Cannot parse source type: "'a"`，均未生成观察、原始查询或证明。
因此没有发布冒充完整性证明的手写 `.rs` 或 `.smt2`。
准确诊断、原生输入和边界见
[specdet-cow-lifetime-type.md](../issues/specdet-cow-lifetime-type.md)。
`replay-expanded.*` 保留最初误扩展到借用目标的执行；当前 `replay.*` 已限定为原四目标，
没有用那次额外执行更新借用的独立结论。

本轮实际执行了 `python3 -m unittest discover -s tests -p 'test_*.py' -v`。
31 项测试中，30 项通过；剩余一项的四个 Cow 完整性子测试如实失败。
完整输出在 `tests/cow-engineer/full-suite/`，没有跳过或放宽这项检查。
`tests/cow-engineer/bindings/native-build.*` 记录本轮新编译原生程序，
`native-tests.stdout` 记录六项行为测试通过；不是执行旧二进制。
测试覆盖四种精确函数类型、全部元素和顺序、空 slice、N=0/非空数组、空/非空 Vec、
ZST、非静态元素，以及 Clone 一经调用即 panic 且没有 View/Copy/Eq 的类型。
十个生命周期和移后复用探针均被正确拒绝，临时 `.rs` 已删除而输入与诊断保留。
`clients.stdout` 中七个义务确认透明观察、变体/顺序可区分，以及真实 From 的泛型客户端；
这些不是源体或完整性证明的替代品。

收集脚本现只更新既有表中的四个借用行，不重建其他 API。
它按保存的源码、依赖、基线和正确性中间表示决定能否保留独立结论；
改变这些输入会重新开放结论，缺少证据则明确报错。
十四项定向回归检查通过，包括新增 checker 目标和本次 Cow 内联模块注册。
`tests/cow-engineer/collector/actual.stdout` 还记录了对真实扩展清单副本的收集：
全部 138 行逐字段不变，四个既有借用独立结论保留。
与本轮起点 `proofs/correctness/cow/cow-engineer/coverage-before.tsv` 相比，
只有四个 Cow 行和四个借用行的独立结论改变，其余 130 行逐字段不变。
逐项核对输出为 `tests/cow-engineer/coverage-check.stdout` 和
`tests/cow-engineer/proof-evidence-check.stdout`。

当前独立双轨确认数仍为 **2/138**。Cow 的源码对应、正确性、冗余及当前解析失败
已有独立结论；可能的受支持编码及真实完整性仍未确认。
本轮先检查固定工具实际实现，只有找到保持原契约的原生入口才重跑受影响证明；
解析失败本身不证明所有等价编码都不可行。

### 固定原生入口检查后的范围

本轮亲读固定 specdet 的类型提取、类型解析、观察选择、可信转译及对应测试。
原生观察无论采用哪种已支持策略，都先解析原返回类型；透明别名展开也回到同一解析。
可单独保留生命周期的辅助解析器没有绕过这一必经入口，
当前真实 `CowObservation` 的 blanket impl 也未被原生观察注册。
`proofs/completeness/cow/native-support/inspection.json` 记录了对 `from_vec`
原保存契约的未修改组件对照：来源视图和 impl 视图均为空，Cow 观察未覆盖，
函数模型保持相同。47 项既有检查器定向测试通过，命令和完整日志在同目录。
它们不生成 Cow 的比较、查询或证明，也不代表新的 Rust 构建或双轨通过。

在固定工具已实现的入口内未找到符合约束的编码；本轮没有盲试别名、
修改契约或检查器，也没有重跑已知失败的四目标分析。
实际调用路径、两层支持缺口及需管理者另行授权的最小工具范围见
[specdet-cow-lifetime-type.md](../issues/specdet-cow-lifetime-type.md#固定原生入口的源码检查)。
新增工具范围判断尚待正常独立审阅。已确认的源体、旧失败和临时冗余准则全部保留。
本轮仅更新 `coverage.tsv` 四个 Cow 行的独立结论字段，
其余 134 行及四行的原证明结果不变；起点保存在
`proofs/completeness/cow/native-support/coverage-before.tsv`。
四个 Cow 仍不计入双轨完成，独立双轨确认数仍为 **2/138**。

### Cow 的只读重放

下列原双轨命令保留供编码或工具发生实质变化后使用；本轮没有这样的变化，
不要求重复已独立确认的构建或已知失败的完整性重放。
复查本轮组件对照时可沿用
`proofs/completeness/cow/native-support/inspection.command.json` 的程序和输入，
把 stdout、stderr、TMPDIR 移到 `{scratch}`。
复查 `proofs/completeness/cow/native-support/native-tests.command.json`
时还须把 cwd 移到 `{scratch}` 下的私有目录，
因为既有工具测试会在 cwd 中建立并清理临时文件；测试选择和工具路径不变。

Reviewer 使用 `run_review_command`，管理工具的工作目录为本项目宿主路径；
运行中通过同一 command_id 调用 `get_review_command`。
先亲读共享及 Reviewer 自身指南，并继续应用
[项目临时冗余准则](../review-criteria-temporary.txt)。
以下命令只把输出写入 `{scratch}`，不改写源输入或比较目标。

```sh
S='{scratch}/cow'
mkdir -p "$S/correctness/build" "$S/tmp"
for api in from_slice from_array from_vec from_vec_ref; do
  code=0
  bash scripts/with_baseline.sh env TMPDIR="$S/tmp" \
    toolchains/verus-x86-linux/verus "proofs/correctness/cow/$api.rs" \
    --edition=2021 --crate-type=lib --crate-name "$api" --compile --num-threads=1 \
    --trace --log-all --log-dir "$S/correctness/$api" \
    -o "$S/correctness/build/lib$api.rlib" \
    > "$S/correctness/$api.log" 2> "$S/correctness/$api.stderr" || code=$?
  printf '%s\n' "$code" > "$S/correctness/$api.exit-code"
  test "$code" -eq 0 || exit "$code"
done
bash scripts/with_baseline.sh env TMPDIR="$S/tmp" \
  toolchains/verus-x86-linux/verus specs/lib.rs --edition=2021 --crate-type=lib \
  --crate-name vec_specs --compile --num-threads=1 \
  -o "$S/correctness/build/libvec_specs.rlib" \
  > "$S/correctness/aggregate.log" 2> "$S/correctness/aggregate.stderr"
bash scripts/with_baseline.sh python3 scripts/borrowed_scratch_config.py "$S/completeness"
python3 proofs/completeness/cow/check.py "$S/completeness"
```

最后一条命令当前会记录四个真实失败并返回 2，而不是把运行完成当作证明通过。
如继续执行原生补充测试，须使用刚编译的库：

```sh
bash scripts/with_baseline.sh env TMPDIR="$S/tmp" \
  COW_PROOF_BUILD="$S/correctness/build" COW_TEST_OUTPUT="$S/tests" \
  COW_COMPLETENESS_OUTPUT="$S/completeness" \
  python3 -m unittest discover -s tests -p test_cow_bindings.py -v
```

这条命令当前仍会在四个完整性子测试失败。若只读容器缺少 cc，应如实保留链接失败，
不得执行旧二进制冒充本次构建，也不转为环境维护任务。

[coverage.tsv](coverage.tsv) 为全部 138 个规范 API 身份各保留一行，
连接源码、docstring、官方视图和既有规格，以及本轮实际证明、命令、结果和问题。
其中 `alloc/…`、`core/…` 路径相对于只读输入
`/home/chentianyu/nanvix-rust-std-spec-survey/rust-1.96/library`；
其余路径相对于本实验目录。未开展的目标明确保留为未运行，不因已有 vstd 声明而视为已证明。

[source_api.json](source_api.json) 和 [source_api.tsv](source_api.tsv)
保留完整签名、类型和 trait 参数、接收者可变性、生命周期、稳定性、cfg、
源码和文档位置及排除理由。[submodules.md](submodules.md) 记录实际子模块、
类型归属、委托和视图依赖。16 个 Vec 源文件均有记录：
稳定公共模块自有可执行条目为 138，另有 164 个被排除候选和
327 个外部继承默认方法实例。后两类不重复计入本模块实现的分母。
宏展开产生的 24 个 PartialEq 方法及派生的 Splice Debug 没有遗漏；
重导出、注释镜像、私有特化和不稳定成员不伪装成新的稳定 API。

[vstd_coverage.json](vstd_coverage.json) 和
[vstd_coverage.tsv](vstd_coverage.tsv) 以官方固定版本重新关联全部 138 个目标：
32 个具有精确绑定，1 个仅有部分绑定，52 个仅有 trait 框架，
22 个有间接依赖，31 个没有覆盖。精确绑定只说明目标和签名域相符，
不表示现有契约充分，也不表示实现已通过本实验的两种证明。
例如范围 `IndexMut` 不具有 usize 索引语法钩子的保证。
四个本轮转换均没有可复用的同目标官方声明；Deref 的声明不被算作 AsRef 的声明。

| 本轮目标 | 源体正确性 | 实际完整性及重新执行 | 当前范围 |
|---|---|---|---|
| `AsRef<Vec<T,A>>::as_ref` | 一个义务通过，并编译 | 两次原始查询均 `unsat`，各一个义务通过 | 两轨已有结果，等待独立审查 |
| `AsRef<[T]>::as_ref` | 一个义务通过，并编译 | 两次原始查询均 `unsat`，各一个义务通过 | 两轨已有结果，等待独立审查 |
| `AsMut<Vec<T,A>>::as_mut` | 一个义务通过，并编译 | 返回可变引用被拒绝 | 不计入双轨通过 |
| `AsMut<[T]>::as_mut` | 一个义务通过，并编译 | 返回可变引用被拒绝 | 不计入双轨通过 |

当前是 **2/138 个 API 已取得本轮双轨结果**，不是 138 个 API 或整个 Vec
模块完成，也不是独立审查已经完成。可变目标只完成了正确性维度。
`specs/lib.rs` 将四个不重复的声明编译为库；该纯声明聚合显示
`0 verified, 0 errors`，只算构建结果，绝不算源体证明。

## 冗余等价删减后的当前结果

`specs/vec/borrowed.rs` 仅删除返回 Vec 的两个契约中的三条同状态 View 等式；
共享值等式、可变初态值等式及可变终态值等式仍保留。两个 slice 契约、
四个可执行函数体、合法输入域和固定工具链均未改变。
逐条蕴含及源码对应见
[source-body-embedding.md](../issues/source-body-embedding.md)。
原来的两个 Vec 正确性入口保存在
`proofs/correctness/vec/before-redundancy/`；
旧规范快照、完整性文件、失败诊断及所有旧运行目录继续保留。

本轮四个源体分别在 `proofs/correctness/vec/redundancy-engineer/<api>.log`
记录一个通过的义务，并在同目录 `build/` 产生库。
`aggregate.log` 记录本轮聚合编译。
`contract-equivalence.log` 的六个通过义务来自
`tests/borrowed_clients.rs`：两个泛型 View 同余证明、
两个从删减后声明推出原契约的客户端、两个允许实际修改内容的写回客户端。
其实际命令为：

```sh
bash scripts/with_baseline.sh \
  env TMPDIR="$PWD/proofs/correctness/vec/redundancy-engineer/tmp" \
  toolchains/verus-x86-linux/verus tests/borrowed_clients.rs \
  --edition=2021 --crate-type=lib --num-threads=1 --log-all \
  --log-dir proofs/correctness/vec/redundancy-engineer/contract-equivalence
```

当前完整性结果和真正重新执行的结果分别为
`proofs/completeness/vec/redundancy-engineer/analyze.json`、`replay.json`。
二者各有两个 `deterministic` 和两个 `not_evaluated`，总退出码均为 2。
两个 AsRef 各有一个通过的义务，原始查询均为 `unsat`；
两个 AsMut 均在提取阶段给出 `unsupported_mutable_return`，
没有生成原始查询或证明。对应 `.rs`、`.smt2` 和实际命令均在同一目录，
未覆盖先前的导出文件。

`inventory/redundancy-engineer/evidence-check.log` 对应收集脚本的实际运行；
该脚本核对两份完整源码快照、泛型、返回类型、零前置条件、当前后置条件、
原观察式、全部七个关闭的搜索 guard，以及非零完整性义务。
`coverage.tsv` 只更新这四个目标，其他 134 行逐字字段不变；
改前清单保存在 `inventory/redundancy-engineer/coverage-before.tsv`。
两个 AsRef 的观察仍分别为 `(r1)@ =~= (r2)@` 和 `r1 =~= r2`，
没有把所选内容比较换成地址、长度或其他较弱关系。

五项绑定及配置测试和一项导出文件测试通过，记录为
`tests/redundancy-engineer/bindings.stderr`、
`completeness-files.stderr`；其中包含五项原生行为测试和八个预期编译拒绝。
配置测试随后仅调整了临时文件的自动清理，修改后的该项单独通过，
记录为 `scratch-config.stderr`，其余未变检查未重跑。
六个 Verus 客户端义务已经按上面的命令实际执行，没有再重复运行。

`runtime-review-readiness.json` 已解除此前的环境等待，不是 API 的语义确认。
独立 Reviewer 仍须亲自判断四个源体嵌入、固定官方依赖和版本边界，
重放当前两轨结果，并按
[临时冗余准则](../review-criteria-temporary.txt) 逐条检查契约。
本轮未生成依赖这些判断的新 API，四行 `independent_review` 仍为 `pending`。

## 独立审查时将全部输出放到私有目录

通过 `run_review_command` 执行下列命令，工作目录使用宿主路径
`/home/chentianyu/rust-std-vec-specgen-astra-2026-09-22`。
`{scratch}` 由审查工具提供；若命令尚在运行，使用同一 `command_id`
调用 `get_review_command`，不要重新提交命令。
以下命令不改写输入文件或项目清单。

`borrowed_scratch_config.py` 只把项目根目录和 verifier 改写为相同目标的
绝对路径，并将 `TMPDIR`、输出目录转至私有目录；解码后的其他配置逐项不变。
原 `specdet.toml`、`with_baseline.sh` 均未修改。
注意 `env TMPDIR=...` 必须放在包装脚本之后，否则会被包装脚本覆盖。

```sh
set -eu
S='{scratch}/borrowed'
mkdir -p "$S/correctness/build" "$S/tests"
bash scripts/with_baseline.sh python3 scripts/borrowed_scratch_config.py "$S/completeness"
for api in as_ref_vec as_ref_slice as_mut_vec as_mut_slice; do
  bash scripts/with_baseline.sh env TMPDIR="$S/completeness/tmp" \
    toolchains/verus-x86-linux/verus "proofs/correctness/vec/$api.rs" \
    --edition=2021 --crate-type=lib --crate-name "$api" --compile --num-threads=1 \
    --trace --log-all --log-dir "$S/correctness/$api" \
    -o "$S/correctness/build/lib$api.rlib" \
    > "$S/correctness/$api.log" 2> "$S/correctness/$api.stderr"
done
bash scripts/with_baseline.sh env TMPDIR="$S/completeness/tmp" \
  toolchains/verus-x86-linux/verus specs/lib.rs --edition=2021 \
  --crate-type=lib --crate-name vec_specs --compile --num-threads=1 \
  -o "$S/correctness/build/libvec_specs.rlib" > "$S/correctness/aggregate.log" \
  2> "$S/correctness/aggregate.stderr"
D=/home/chentianyu/spec-determinism-tool/.venv/bin/specdet
code=0
bash scripts/with_baseline.sh env TMPDIR="$S/completeness/tmp" \
  "$D" analyze --config "$S/completeness/specdet.toml" --json \
  > "$S/completeness/analyze.json" 2> "$S/completeness/analyze.stderr" || code=$?
printf '%s\n' "$code" > "$S/completeness/analyze.exit-code"
test "$code" -eq 0 || test "$code" -eq 2
R=$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["run_dir"])' \
  "$S/completeness/analyze.json")
code=0
bash scripts/with_baseline.sh env TMPDIR="$S/completeness/tmp" \
  "$D" replay --run "$R" --reexecute --config "$S/completeness/specdet.toml" \
  --verus "$PWD/toolchains/verus-x86-linux/verus" \
  --out "$S/completeness/replay-runs" --json \
  > "$S/completeness/replay.json" 2> "$S/completeness/replay.stderr" || code=$?
printf '%s\n' "$code" > "$S/completeness/replay.exit-code"
test "$code" -eq 0 || test "$code" -eq 2
cp inventory/coverage.tsv "$S/coverage.tsv"
bash scripts/with_baseline.sh python3 scripts/collect_borrowed_results.py \
  --correctness-dir "$S/correctness" --completeness-dir "$S/completeness" \
  --coverage "$S/coverage.tsv" > "$S/evidence-check.log"
bash scripts/with_baseline.sh env TMPDIR="$S/completeness/tmp" \
  BORROWED_TEST_OUTPUT="$S/tests" BORROWED_PROOF_BUILD="$S/correctness/build" \
  BORROWED_COMPLETENESS_OUTPUT="$S/completeness" \
  python3 -m unittest discover -s tests -p test_borrowed_bindings.py -v \
  > "$S/tests/bindings.stdout" 2> "$S/tests/bindings.stderr"
```

允许总退出码 2 只是为了继续检查逐目标诊断；收集脚本仍要求两个 AsRef
实际通过，并核对两个 AsMut 的明确限制，不能将任意失败写成通过。
原生 replay 在校验已保存快照后以该快照为输入；
覆盖配置不会把它换回另一份源码。依据是实际入口
`/home/chentianyu/spec-determinism-tool/src/specdet/cli/main.py:199-214,295-323`。
本轮已实际使用这一配置方式分析及重新执行，但工程运行不冒充受限容器中的独立重放。

## 先前 closure-engineer 轮的记录

以下保留前轮记录；其中的“本轮”、未删减契约和旧路径均指该历史轮次。
它们不能替代上面的当前结果，也不表示旧失败已获解决。

本轮未修改四个候选声明、正确性函数体或已发布的完整性文件。
新构建保存在 `proofs/correctness/vec/closure-engineer/`，每个入口的
`.command.txt`、`.stdout.log`、`.stderr.log` 与 Verus 自己管理的日志目录分开。
原有构建和查询记录没有覆盖。独立审查仍须亲自重放，并正式提交源码对应及两轨判断；
本页及清单中四个目标均未记为已独立确认。

## 如何重放

逐 API 的完整正确性命令在 [coverage.tsv](coverage.tsv)。
例如下面命令实际验证和编译源体，而不是调用目标假设的客户端：

```sh
bash scripts/with_baseline.sh toolchains/verus-x86-linux/verus \
  proofs/correctness/vec/as_ref_slice.rs --edition=2021 --crate-type=lib \
  --crate-name as_ref_slice --compile --num-threads=1 --trace --log-all \
  --log-dir proofs/correctness/vec/closure-engineer/as_ref_slice \
  -o proofs/correctness/vec/closure-engineer/build/libas_ref_slice.rlib
```

完整性使用未修改的实际 CLI，配置为 `specdet.toml`。
本轮实际命令如下；因保留两个不支持的可变目标，analyze 和 replay 的总退出码
均为 2，须看逐目标语义结果而不是总退出码：

```sh
bash scripts/with_baseline.sh /home/chentianyu/spec-determinism-tool/.venv/bin/specdet \
  analyze --config specdet.toml --out proofs/completeness/vec/review-runs --json
bash scripts/with_baseline.sh /home/chentianyu/spec-determinism-tool/.venv/bin/specdet \
  replay --run proofs/completeness/vec/review-runs/20260922T070801Z-e3d49695e0 \
  --reexecute --verus toolchains/verus-x86-linux/verus \
  --out proofs/completeness/vec/review-replay-runs --json
```

本轮原始结果为 `proofs/completeness/vec/review-runs/engineer-analyze.json`；
重新执行结果为 `proofs/completeness/vec/review-replay-runs/engineer-replay.json`。
两者指向不同的实际运行目录，源码快照逐字等于当前规范。
每个已发布 `as_ref_*.rs` 仍逐字等于本轮生成的 harness；
相邻 `.smt2` 保留初次运行的原始 native query，本轮查询由清单直接链接。
它们属于 `verus.native` 的模块上下文，真正入口及 verifier 命令在对应
`proof-check-1.json`，重放使用上面的 CLI；不是将模块文件冒充独立 crate。
`as_mut_*.rs` 则明确保留失败输入，因为检查器未生成证明。

上轮 `analyze.json`、`replay.json` 及其目录均保留不动。
本轮首次把 replay 输出放在输入快照的祖先目录，CLI 在运行查询前明确拒绝；
诊断保留为 `proofs/completeness/vec/review-runs/engineer-replay.stderr`。
改用上面不包含输入快照的独立目录后，实际重新执行完成。
这次路径错误与两个可变返回目标的后端限制不同，不能混为一种失败。

观察策略为 `verus-strict-v1`。Vec 输出比较
`(r1)@ =~= (r2)@`；slice 输出比较 `r1 =~= r2`。
二者包含完整长度、每个元素及顺序，不只检查长度。
Vec 的比较不涵盖官方 View 以外的表示，尤其容量、分配器和物理地址；
这不是对所有内存观察的完整性声明。原始查询关闭全部 schema 搜索 guard，
没有使用长度分段或额外输入前提。检查器本身未运行可满足性检查；
本轮用无前置条件、无循环的已验证原函数体及实际调用见证排除空域或错误答案。
`inventory/closure-engineer/borrowed-evidence-check.log` 记录两次运行逐目标的
完整契约、观察式、全部七个关闭的搜索 guard、非零义务和源码快照对应检查。
切片的内容比较依据官方 `toolchains/upstream/source/vstd/slice.rs:170-174`，
不是物理地址相等。

补充检查由以下命令执行，包含源码/契约绑定、精确返回类型、
接收者生命周期、实际元素与次序、ZST、无 Copy/Clone 的元素和分配器、
非 `'static` 借用及可变写回：

```sh
BORROWED_TEST_OUTPUT="$PWD/tests/closure-engineer" \
BORROWED_PROOF_BUILD="$PWD/proofs/correctness/vec/closure-engineer/build" \
bash scripts/with_baseline.sh python3 -m unittest discover \
  -s tests -p test_borrowed_bindings.py -v
```

这两个环境变量只选择测试输出和本轮新编译的库，未改变测试断言或 API。
独立审查时应另选尚未使用的目录，保留这里记录的运行文件。
本轮六项测试全部执行，包含五项原生行为测试和两个写回客户端义务，
输出为 `tests/closure-engineer/test_borrowed_bindings.log`、
`native-tests.stdout` 和 `writeback.stdout`。
测试只把原生调用和客户端证明作为补充。八个应当拒绝编译的探针分别得到
生命周期错误 `E0515` 或返回类型错误 `E0308`；临时源文件已单独删除，
完整编译命令和诊断保留在 `tests/closure-engineer/`。
原生调用使用固定宿主 Rust 1.98.1，不能代替对 Rust 1.96 源码的对应检查。

清单复跑实际发现了源码生成器误处理追加 vstd 段落的问题，修复范围及原始失败
见 [issues/INDEX.md](../issues/INDEX.md)。修复后源码清单的 23 项测试通过，
vstd 清单的 27 项测试也已在本轮通过；两个生成器的 `--check` 均通过。
输出保留在 `inventory/closure-engineer/`。138 个 API 身份、排除项和覆盖分类均未变化。

问题及独立审查范围见 [issues/INDEX.md](../issues/INDEX.md)，
官方来源、宿主版本和证明边界见
[research/GROUND_TRUTH.md](../research/GROUND_TRUTH.md)。

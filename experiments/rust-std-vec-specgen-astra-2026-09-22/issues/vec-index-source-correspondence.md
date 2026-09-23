# 泛型 Vec Index 的源码对应与关联输出观察限制

本记录只涉及原清单的
`<alloc::vec::Vec<T, A> as core::ops::Index<I>>::index`。
源码入口和默认聚合已用固定 Verus 新编译；泛型完整性尚未完成，
独立源码判断及本次结果仍待正常 Reviewer 路径确认。
这里没有修改 Rust、vstd、specdet、IntoIter 候选或待答问题 `d2455d2deb7a`。
问题仅保存在本项目，没有向外部仓库提交。

## 原签名、执行表达式与继承条件

亲读的权威源码根目录是
`/home/chentianyu/nanvix-rust-std-spec-survey/rust-1.96/library`：

- `alloc/src/vec/mod.rs:3825-3832` 保留
  `impl<T, I: SliceIndex<[T]>, A: Allocator> Index<I> for Vec<T, A>`、
  `type Output = I::Output` 和
  `fn index(&self, index: I) -> &Self::Output`，
  唯一执行表达式为 `Index::index(&**self, index)`。
- `core/src/ops/index.rs:1-74` 说明共享索引语法、可不定长的关联输出、
  与接收者相连的共享借用，以及越界可能 panic。
- `core/src/slice/index.rs:9-20,104-214` 给出切片 Index 委托、
  sealed SliceIndex、关联 Output 和安全 index 的越界 panic 说明。
  相关实现位于 `214-841,1007-1075`。
- `core/src/index.rs:1-475` 给出 Last 与 Clamp 的实际实现；
  `core/src/ops/index_range.rs:6-19` 明确 IndexRange 是 `pub(crate)` 类型，
  不能从本项目安全地构造该私有类型来做原生实例测试。

`specs/vec/index.rs:9-22` 是有限源码对应入口，不是新的标准库绑定。
共享 `self` 具名为 `vec: &Vec<T, A>`，`Self::Output` 写为
`<Vec<T, A> as Index<I>>::Output`，执行体仍是
`Index::index(&**vec, index)`。原 I 按值传递，返回借用仍由接收者确定；
没有新增元素 trait、分配器 Clone、静态寿命或具体索引类型限制。
Rust/Verus 中间表示将返回类型正规化为同一个
`<I as SliceIndex<[T]>>::Output`，没有把它强制改为 T 或 `[T]`。

入口名使用 `index_source`。首个自由函数入口也叫 `index`，
固定宏展开后与同名参数产生 E0109/E0618；仅改自由证明入口名称后编译成功。
原参数名、执行表达式、泛型和契约均未改变。
首个候选和失败完整保存在
`proofs/correctness/vec/generic-index/engineer-source/`，
不把这个局部命名问题归为原 Rust 实现错误。

另一个实测差别来自 trait 方法继承的 `#[track_caller]`，不是返回契约。
最初自由入口没有此属性，新增的单项 panic hook 检查实际观察到异常位置落在
`specs/vec/index.rs:19`，而标准库报告调用方的位置；其余七项原生测试没有重跑。
记录为 `tests/vec-index/caller-location-before/caller-location.*`，退出 101。
当前入口保留原 impl 的 `#[inline]`，并显式保留原 Index trait 的
`#[track_caller]`，不改变执行表达式或契约。修正后两份库均重新编译成功；
新程序的调用位置检查通过，source、aggregate 和标准库都报告各自调用点。
更新后的源码也重新经过两轨，结果见下文；此前记录原样保留。

复用的固定官方来源均位于项目
`toolchains/upstream/source/vstd/`：

| 来源 | 本入口依赖的内容 |
|---|---|
| `std_specs/core.rs:47-60` | Index trait 的 `index_req` 前提；即使具体 Vec 声明没有再写 requires，继承条件仍存在。 |
| `std_specs/vec.rs:178-190` | Vec 的 `index_req` 定义及存在切片、`call_ensures` 后置条件。 |
| `std_specs/vec.rs:248-253` | 官方 Vec Deref 返回与 Vec 相同的完整元素序列。 |
| `std_specs/slice.rs:310-313,330-336` | 切片 Index 的前提等于 SliceIndex 的 `in_bounds`，后置条件委托给同一个 SliceIndex::index。 |
| `slice.rs:119-168` | SliceIndex 的原关联输出、`in_bounds` 和 `index_postcondition` 契约。 |

入口的完整契约为：

```rust
requires
    vec.index_req(&index),
ensures
    exists|s: &[T]| #[trigger] s@ == vec@
        && call_ensures(<I as SliceIndex<[T]>>::index, (index, s), r),
```

前提按官方定义展开为：
`forall|s: &[T]| s@ == vec@ ==> index.in_bounds(s)`。
Deref 提供一个与 Vec 序列相同的实际切片，该前提因此适用于它；
随后切片 Index 的官方后置条件直接提供所需的存在见证。
整个推导无需调用目标 Vec Index 假设来证明自身。

没有重复注册官方规格，也没有添加输出唯一性、SliceIndex 规律或关联类型观察公理。
按项目 `review-criteria-temporary.txt` 检查，当前只有一个继承前提和一个
存在性后置条件；前提约束合法调用，后置条件连接源序列与返回内容，不能互删。
没有添加可由同状态逻辑等式推出的重复 View 条款。独立 Reviewer 仍需自己确认。

## 本轮源码编译的实际记录

`proofs/correctness/vec/generic-index/build.py` 对尚不存在的输出目录运行
`scripts/with_baseline.sh` 下的固定 Verus `--compile --num-threads=1`，
保存 argv、退出码、起止时间、输入副本、全部中间表示及新库。
脚本要求库修改时间在本次进程的起止时间内，不接受旧库。

| 输出目录 | 观察到的结果 |
|---|---|
| `proofs/correctness/vec/generic-index/caller-preserved-source/` | 退出 0，`1 verified, 0 errors`，新生成 `libvec_index_source.rlib`。 |
| `proofs/correctness/vec/generic-index/caller-preserved-aggregate/` | 退出 0，`4 verified, 0 errors`，新生成 `libvec_specs.rlib`，没有验证过滤器。 |

先取得单独入口成功，才在 `specs/lib.rs` 加入该模块和所需
`slice_index_methods` feature，在 `specdet.toml` 追加唯一 include 项。
默认聚合仍排除 with_capacity 候选与 IntoIter 调查。

单独入口的 `caller-preserved-source/logs/crate.vir` 保留全部 T/I/A 边界、
继承前提和关联 Output；执行体实际解析为
`alloc::vec::impl&%9::deref` 与 `core::slice::index::impl&%0::index`。
`caller-preserved-source/logs/vec_index-final.air` 的源码义务也只使用这两个
执行委托的后置条件，没有使用目标 Vec Index 的返回假设。
这些是相对于固定官方依赖的正常返回证明，不是 slice 底层实现、panic 不发生、
任意分配器行为或 Rust 1.96 与宿主 Rust 1.98.1 全部实现等价的证明。
早期尚未显式保留 caller 属性的成功编译仍存于 `named-entry/` 和
`engineer-aggregate/`；它们不替代上表的当前库。

## 真实完整性分析停在返回观察构造

`proofs/completeness/vec/generic-index/caller-preserved/analyze.command.json` 和
`replay-selected.command.json` 分别记录真实 analyze 与 `replay --reexecute`。
二者恰好选择 `vec/index.rs::vec::index::index_source`，均退出 2，报告：

```text
observations / observation_gap
No source-bound observation semantics were resolved for &<Vec<T, A> as Index<I>>::Output
```

对应的 `.stdout`、`.stderr` 和 `.result.json` 均保留原生结果。
两次 function_spec 保留 `<T, I: SliceIndex<[T]>, A: Allocator>`、
原 Vec 共享参数、按值 I、关联返回类型，以及上述唯一 requires 和 ensures；
源码副本与当前候选一致，没有 overlay、契约变换或新增可信语义。
分析的原生 contract 文件为：

`proofs/completeness/vec/generic-index/caller-preserved/analysis-runs/20260922T214313Z-cb3833c6bf/targets/387c9c39962aee09c807d471/revisions/0/contract.json`

正确选择的重新执行位于：

`proofs/completeness/vec/generic-index/caller-preserved/selected-replay-runs/20260922T214314Z-af83d7cb7f/`

返回类型被原生提取器表示为 unknown，尚未建立完整元素或切片内容观察。
两个结果都是 `not_evaluated`：没有比较函数、完整性 harness、原始 SMT 查询、
搜索条件或通过义务。因此不能报告完整性、不确定性的语义反例、不可满足，
也不能声称搜索条件已关闭后的证明成功。具体索引客户端不会补上这个缺口。

对固定检查器的受限只读调查定位到
`/home/chentianyu/spec-determinism-tool/src/specdet/`：

- `adapters/verus/native/extract/extractor.py:137-143,335-350` 将该 scoped
  返回类型保留为 unknown；`adapters/verus/type_context.py:113-125` 也不按
  Rust trait 实现正规化关联投影。
- `adapters/verus/type_context.py:515-568,612-630` 会展开别名，但别名展开成
  同一未解析投影不会产生新的元素或切片观察。
- `adapters/verus/backend.py:743-751,783-811,829-839` 在生成相等比较之前
  检查未知返回类型。现有 source-bound View 路径需要真实的 View 依据；
  `SliceIndex` 约束本身没有提供该依据。
- `adapters/verus/native/codegen/gen_det.py:1318-1347` 和
  `adapters/verus/type_context.py:648-795` 支持某些已有 View 边界，但添加
  `I::Output: View` 会改变本 API 的合法泛型域，未采用。

本轮未找到保持原域与完整观察的已实现原生表示；这不是所有未来表示均不可行的
证明。需要修改检查器或扩大可信基础才能继续的路线在此停止。
没有把 I 改成 usize、另计具体索引 API、改比较为地址/长度/布尔量，
也没有复制或修补固定工具。

### 首次重放的范围错误与修正

首次 `engineer/replay.command.json` 显式传入只有 include、没有 select 的
scratch 配置。原生 `--config` 替换了保存的 selector，实际重放了 14 个默认目标，
违反本任务的单目标范围。该输出与旧失败完整保留，但不作为本任务的正确重放，
也不重新授予任何既有 API 语义确认。

固定 `cli/main.py:199-239` 表明，不传 `--config` 才会恢复原分析保存的
selector、源副本与环境。只修正该命令后重新执行，未重跑未变的 analyze；
`engineer/replay-selected.*` 恰好选择本入口并得到同一 observation_gap。
当前 `check.py` 已去掉该覆盖参数，检查两次的精确目标集合及非零证明要求。
首次分析的有效配置中 `selectors = ["vec/index.rs"]` 继续保留。
随后只有 candidate 的 caller 属性发生实质修正，才对新源码运行
`caller-preserved/` 中的 analyze/reexecute；当前脚本这次也实际执行并返回 1，
没有误选其他目标。

### 本地驱动的失败可见性与证明判定修复

本次失败通知中的外层 stderr 为空，是因为 `check.py` 捕获了子进程输出，
又在判定失败时直接返回 1；真正的 `observations/observation_gap` 留在
`analyze.stdout` 和 `replay-selected.stdout` 的逐目标 JSON 中。
驱动现将子进程 stderr、两个失败阶段的原生诊断及报告路径传到外层 stderr，
不再因首个阶段失败而省略另一个阶段的诊断，原始输出和退出码仍完整保存。

同时将证明判定从 `any(...)` 改为非空集合上的 `all(...)`：
目标列表和结果列表都必须恰好对应本入口，每个证明都须 verified 且义务数大于零。
这与现有 `test_full_generic_completeness` 的逐证明要求一致，不把部分通过或
零义务当作完成。没有改测试断言、API 契约、接收者、固定工具或观察策略；
这项本地驱动修复不解决关联输出观察限制，也不是独立审阅。

本次使用新的 `local-debug-f48561d3-source/` 和
`local-debug-f48561d3-aggregate/` 正确性目录重新编译，分别通过 1 和 4 个义务。
真实 analyze/reexecute 各执行一次，仍分别退出 2，未生成完整性证明；
驱动退出 1，现在外层日志明确包含两阶段的 observation_gap：
`proofs/completeness/vec/generic-index/local-debug-f48561d3/stderr.log`。
使用这些新产物执行一次
`python3 -m unittest discover -s tests -p test_vec_index.py -v`，
10 个方法中 9 个通过，完整性方法的两个阶段子项失败；源码原生程序的
8 项测试通过。结果保存在 `tests/vec-index/local-debug-f48561d3/suite.stderr`。
旧失败与其余覆盖行保留，本 API 仍未完成。

## 原生行为与类型检查的范围

`tests/vec_index_behavior.rs` 逐一包含原源码可公开使用的 24 类 SliceIndex：
usize、旧 ops 六种范围、Bound 对、新 range 四种范围、11 类 Clamp 及 Last。
另外的私有 IndexRange 只核对其源码与可见性，不假造可访问的替代类型。
通用函数指针检查保留任意 T、I、A 及 `&I::Output`；运行内容比较覆盖空范围、
边界、重复项及顺序、ZST、无额外 trait 的非静态元素、不可 Clone 的借用分配器，
并比较安全越界、反向范围和包含式端点溢出的 panic。测试不调用 unchecked 方法。

官方 `std_specs/slice.rs:17-262` 的具体观察实现只覆盖 usize 与旧 ops 六种范围。
本入口保持官方完整泛型契约，不擅自为其他源码支持的索引添加未证明的规律。
原生实例比较不等于这些规律已在固定 vstd 中得到形式证明。

`tests/vec_index_clients.rs` 是通用契约及完整元素/切片内容的 source/std 客户端；
不作为泛型完整性证明。`tests/test_vec_index.py` 还保留正式完整性成功断言，
不以 skip 或 expectedFailure 隐藏当前限制；返回类型与接收者寿命的临时
Rust 探针执行后只删除临时源文件，命令、输入文本和诊断保留。
本轮完整命令
`python3 -m unittest discover -s tests -p test_vec_index.py -v`
已执行，`tests/vec-index/suite.stderr` 记录 10 个方法：9 个通过，
完整性方法的 analyze/replay 两个子项失败；整条命令退出 1，未改成预期失败。
其中 24 个 source/aggregate/std 类型与接收者寿命拒绝探针均符合原签名预期，
临时 `.rs` 均已删除，输入文本、E0308/E0515/E0502 及原退出码保存在
`tests/vec-index/engineer/probe-*`。

caller 属性修正后只运行受影响的五个方法，全部通过，命令与结果为
`tests/vec-index/caller-suite.{command.json,result.json,stderr}`。
当前新库链接的新原生程序实际通过 **8 项**，见
`tests/vec-index/caller-preserved/native-run.stdout`；其中一项逐一核对 panic
调用点，七项保留完整内容、范围、借用和安全 panic 比较。
新的 source/std 客户端实际通过 **8 个义务**，见同目录 `clients.stdout`。
未变的 24 个拒绝探针及源索引类型清单检查没有重复执行。
最后对更新后的检查器输入、精确重放范围和覆盖行再次作对应检查；
两项通过，泛型完整性方法的两个成功断言仍因真实退出 2 而失败。
这三项的命令、退出码和诊断在
`tests/vec-index/final-evidence-suite.{command.json,result.json,stderr}`，
不是新一轮完整套件，也没有再次执行未变的求解或原生程序。

覆盖表仍有 138 行，只更新本 Index 一行；其余 137 行与
`tests/vec-index/before/coverage.tsv` 逐字段相同。
独立双轨完成数仍为 **7/138**，本 API 不计完成。

## 独立复查使用私有输出目录

先读取项目内 `review-criteria-temporary.txt`；环境能力以
`runtime-review-readiness.json` 为准，不再监听项目外的旧等待路径。
Reviewer 应通过 `run_review_command` 执行，运行中使用同一命令编号的
`get_review_command`。以下命令从项目根目录启动；`{scratch}` 由该接口提供：

```sh
S='{scratch}/vec-index'
test ! -e "$S" || exit 1
mkdir -p "$S/tmp" || exit 1
bash scripts/with_baseline.sh env TMPDIR="$S/tmp" \
  python3 proofs/correctness/vec/generic-index/build.py "$S/source" \
  > "$S/source.stdout" 2> "$S/source.stderr"
source_code=$?
bash scripts/with_baseline.sh env TMPDIR="$S/tmp" \
  python3 proofs/correctness/vec/generic-index/build.py "$S/aggregate" --entry aggregate \
  > "$S/aggregate.stdout" 2> "$S/aggregate.stderr"
aggregate_code=$?
bash scripts/with_baseline.sh env TMPDIR="$S/tmp" \
  python3 proofs/completeness/vec/generic-index/check.py "$S/checker" \
  > "$S/checker.stdout" 2> "$S/checker.stderr"
checker_code=$?
bash scripts/with_baseline.sh env TMPDIR="$S/tmp" \
  INDEX_PROOF_OUTPUT="$S/source" INDEX_AGGREGATE_OUTPUT="$S/aggregate" \
  INDEX_COMPLETENESS_OUTPUT="$S/checker" INDEX_TEST_OUTPUT="$S/tests" \
  python3 -m unittest discover -s tests -p test_vec_index.py -v \
  > "$S/tests.stdout" 2> "$S/tests.stderr"
tests_code=$?
printf 'source=%s aggregate=%s checker=%s tests=%s\n' \
  "$source_code" "$aggregate_code" "$checker_code" "$tests_code" > "$S/exit-codes.txt"
test "$source_code" -eq 0 && test "$aggregate_code" -eq 0 \
  && test "$checker_code" -eq 0 && test "$tests_code" -eq 0
```

包装脚本之后的 `env TMPDIR` 以及脚本内所有库、日志和检查器输出均指向私有目录。
scratch 配置仅改变原四个路径；当前 replay 恢复该次分析的原配置，不改目标或比较。
完整性当前失败应保持失败，并继续收集后续测试结果。
这些是可供独立执行的命令，不宣称工程侧已完成独立审阅。

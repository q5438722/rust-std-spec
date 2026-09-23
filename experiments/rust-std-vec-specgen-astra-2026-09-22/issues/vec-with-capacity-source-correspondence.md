# with_capacity 的原表达式与 Global 构造限制

本次保留 `Self::with_capacity_in(capacity, Global)`，只将 `Self` 明确为
原 impl 的 `Vec<T>`。候选在 `specs/vec/with_capacity.rs`，逐 API 入口在
`proofs/correctness/vec/with_capacity.rs`。没有增加输入限制、元素 trait、
分配器参数或标准库假设，也没有调用目标 with_capacity 来证明自身。
任务 `6611f73cab83` 已独立确认有限源码对应、cfg/const/泛型域、无契约冗余，
以及固定 Verus 在契约求解前拒绝原 Global 构造的有限限制。
类别为已确认的 `verus-limitation`，不是 Rust 实现或文档缺陷，也不证明所有可能
编码均不可行。本轮构建隔离仍待正常独立审阅，继续适用
[本项目临时冗余准则](../review-criteria-temporary.txt)。
工具仍是项目固定的官方 Verus `release/0.2026.09.20.aef82ed` 及未修改的 vstd，
宿主为 Rust 1.98.1；没有将它们与权威语义源码 Rust 1.96 混为同一版本。

## 当前入口：隔离默认构建，不改原候选

`specs/lib.rs` 仅移除 with_capacity 模块及其 `const_heap, const_trait_impl`
feature，保留 `allocator_api` 和全部原非容量模块。默认 `specdet.toml` 仅移除
该目标的 include 项，其他设置及目标不变。`specs/with_capacity_candidate.rs`
则保留原三项 feature 和 `pub mod vec { pub mod with_capacity; }`，直接引用
同一份 `specs/vec/with_capacity.rs`，不复制或重写其 cfg、泛型、const、签名、
原 `Vec::<T>::with_capacity_in(capacity, Global)` 表达式或唯一后置条件。
逐 API 源入口和 Global-only 最小复现也保持不变。

正确性脚本改为构建 source 和 candidate，两项仍分别要求实际编译成功及
1 个通过义务，否则非零退出。完整性脚本先用未改动的 scratch helper 调整
四个私有路径，再显式设置独立 `build.entrypoint` 和唯一的 `targets.include`；
这六项授权差异完整保存在
`proofs/completeness/vec/with-capacity/isolation/checker/config-changes.json`。
不能把最终候选配置称为仅四路径变化或与默认目标集相同。
真实 analyze 仍选 `vec/with_capacity.rs`，replay 仍用 `--reexecute`；
两个失败都执行、落盘并导致包装脚本非零退出。空目标或零义务即使伴随退出 0，
也不满足脚本的成功条件。

隔离前默认聚合实际退出 1 的基线仍在
`proofs/correctness/vec/with-capacity/const-features/aggregate.{result.json,stderr}`。
本轮 `isolation/default/aggregate.*` 记录无验证过滤器的默认 `--compile`
退出 0、3 个真实 reused_basic 源体义务通过及新生成的 `libvec_specs.rlib`。
这只恢复默认构建；`isolation/candidate/{source,candidate}.*` 中的两个原体
编译仍均退出 1，拒绝原 Global 构造，构建包装脚本也退出 1。
这些 `isolation/` 构建路径均位于 `proofs/correctness/vec/with-capacity/`。

本轮完整性实际结果在 `proofs/completeness/vec/with-capacity/isolation/checker/`：
恰好一个原目标 `vec/with_capacity.rs::vec::with_capacity::with_capacity`，
完整序列比较 `(r1)@ =~= (r2)@` 未变。analyze 和 reexecute 均退出 2，
实际 Verus 子进程均退出 1，证明为 `compile_error`、0 个通过义务且无原始 SMT，
包装脚本退出 1。独立候选客户端同样保留该失败。
未修改的 reused-basic 检查脚本在默认 `lib.rs` 下恰好检查原三个目标，
两阶段每目标各 1 个通过义务、均退出 0；这只是连接回归，不是重新语义审查。

新隔离套件首次执行的已保存日志
`.argus_subagents/vec-capacity-isolation-a8d858022146_logs/stderr.log`
为 9 项中 8 项通过、1 项失败：默认编译 stdout 只有三义务的汇总，
未含测试断言要求的 `vec::reused_basic::default` 名称。
这一断言已改为核对实际 AIR 中三个源体的 `Function-Def`、三个 `check-valid`
及 SMT 记录中的三个 `check-sat`、三个 `unsat`，未放宽义务数或源体对应。
仅修改的默认构建测试和更新后的覆盖范围测试再次执行，两项通过；
命令、退出码和输出见 `tests/with-capacity/isolation/selected-tests.*`，
新库及逐源体记录见 `proofs/correctness/vec/with-capacity/isolation/default-obligations/`。
首次断言失败保留，不伪称重新运行了整套九项，也不重复未变的候选和 reused-basic 检查。
原完整 API 套件的成功要求未放宽，未改 skip/expectedFailure，本轮没有重跑它。
逐项结果和不覆盖旧证据的当前命令见
[覆盖说明](../inventory/COVERAGE.md#当前入口的私有目录复查命令)。
本轮不新增独立完成 API，不重跑原生/cc 环境工作，也不继续探索 Global 编码。

## 原源码与正式观察

已亲读权威
`/home/chentianyu/nanvix-rust-std-spec-survey/rust-1.96/library/alloc/src/vec/mod.rs:467-525`，
所属 `impl<T> Vec<T>` 在 `447` 行。原签名是
`pub const fn with_capacity(capacity: usize) -> Self`，运行时自 Rust 1.0 稳定，
const 能力受 `const_heap` 控制，函数仅在 `not(no_global_oom_handling)` 下存在。
默认分配器仍为真实 `Global`。
原 Vec 模块在 `alloc/src/vec/mod.rs:93` 导入 `crate::alloc::Global`，
`std/src/alloc.rs:72` 重新导出同一个类型；入口没有引入同名替代分配器。

固定官方 `toolchains/upstream/source/vstd/std_specs/vec.rs:114-123`
分别给 with_capacity 和 with_capacity_in 相同的返回序列契约。
本入口沿用唯一的 `v@ == Seq::<T>::empty()`，没有前置条件。它描述正常返回的
完整空序列，不证明返回一定发生，不覆盖容量、分配失败、panic 或全局堆状态。
没有另加空长度条件，因为完整空序列已经蕴含它。

已沿原调用亲读以下委托。

| 源码 | 本次据以解释的行为 |
|---|---|
| `alloc/src/vec/mod.rs:915-978` | const impl 内的 with_capacity_in 建立 `len: 0`；容量文档允许超额分配。 |
| `alloc/src/raw_vec/mod.rs:168-180,428-483` | 通过元素 Layout 计算字节布局；零字节直接返回未分配状态，否则调用分配器。布局错误在分配之前返回。 |
| `alloc/src/raw_vec/mod.rs:570-576,617-620`；`alloc/src/vec/mod.rs:1442-1448` | 未分配状态的内部容量为零；对外 ZST 容量为 `usize::MAX`，不是空序列长度。 |
| `alloc/src/raw_vec/mod.rs:25-29,882-907`；`core/src/alloc/layout.rs:59-122,526-533` | checked_mul 先排除乘法溢出；随后要求字节数不超过 `isize::MAX + 1 - alignment`。失败产生 CapacityOverflow，最终 `capacity overflow` panic，不是元素数一律不能超过 isize::MAX。 |

因此非 ZST 正常返回时容量至少为请求值，不要求始终精确相等；零请求不分配。
ZST 即使请求 `usize::MAX` 也不分配。分配失败另走 `handle_alloc_error`，
不能由正常返回的 Seq 契约冒称已形式化覆盖。这些依赖不另计为本轮证明的 API。

## 当前固定 Verus 拒绝原体中的 Global

首次实际执行固定 Verus `--compile` 的命令、退出码及诊断保存在
`proofs/correctness/vec/with-capacity/source/source.{command.json,result.json,stderr}`。
退出码为 1，在求解源体义务和生成库之前报告：

```text
error: disallowed: constructor for an opaque datatype
    Vec::<T>::with_capacity_in(capacity, Global)
                                       ^^^^^^ this constructor is disallowed
```

固定 `toolchains/upstream/source/vstd/std_specs/alloc.rs:6-11` 把真实 Global
登记为带 `external_body` 的外部类型。固定 Verus 的
`toolchains/upstream/source/vir/src/well_formed.rs:310-340` 对此类数据类型的
构造访问直接报错。这与 with_capacity_in 的序列后置条件是否充分是不同的问题。
`proofs/correctness/vec/with-capacity/global_constructor.rs` 保留只含 Global
构造的最小复现，不把它计为 API 正确性证明。

这项发现最初按固定工具限制提交独立判断，现已获上述有限确认；
不是 Rust 源码或文档缺陷。
当前没有实施可执行改写。用 `Global::default()` 替代原表达式、给入口增加分配器
实参、把构造隐藏到 external_body 或新增假设，均不满足当前任务边界；
改动 canonical Rust、Verus/vstd、检查器或 Argus 也不在授权范围内。
本地记录未向外部仓库提交。

## 保留配置条件的发现修正

首次真实 specdet 输出在 `proofs/completeness/vec/with-capacity/engineer/`。
它因函数上的 `#[cfg(not(no_global_oom_handling))]` 报告 `partial_discovery` 和
`target_not_found`，没有发现本入口，退出码为 2；这不算完整性分析通过。
原候选和输出均保留。

沿既有所有权转换的已审方法，当前把完全相同的条件移到仅含该入口的源文件：
`#![cfg(not(no_global_oom_handling))]`。函数体、签名及契约不变，
设置 `no_global_oom_handling` 时仍由真实 Rust 编译器排除整个入口；
不是删除配置条件或改变检查器。当前表示已被真实检查器发现，恰好选择一个目标；
默认构建下的发现结果不能推广到任意构建配置。

证明 crate 显式启用 `allocator_api, const_heap, const_trait_impl` 来编译原 const 委托；
这些 feature 只服务源体表示，不把真实标准库的不稳定 const 能力称为稳定接口。
自由函数入口不重新发布 libstd 的稳定性属性，正式对应限于该配置下的源体及
正常返回内容；原 API 的运行时/const 可用性须另由真实标准库编译探针确认。

## 隔离前的两轨执行与最小复现

`proofs/correctness/vec/with-capacity/const-features/` 保存隔离前逐项入口和
`specs/lib.rs` 的两条 `--compile` 命令、源输入、退出码、日志及中间表示。
两次都在 Global 构造检查处退出 1，没有通过的源体义务，也没有产生 Verus 编译库。
中间表示仍可检查：两处原体均只有一个 `alloc::vec::...::with_capacity_in` 调用，
参数是原 `capacity: usize` 和真实 Global 构造，返回 `Vec<T, Global>`，
只有原 Rust 泛型隐含的 Sized 要求，没有调用目标 with_capacity 假设。
提取的原体见 `tests/with-capacity/lowering/{source,aggregate}.lowered-body.txt`。
这确认了调用关系，不把失败的中间表示称为已完成证明。

`proofs/completeness/vec/with-capacity/const-features/` 中的真实 analyze 和
`replay --reexecute` 恰好选择本入口，使用同一候选和问题，均退出 2。
两个生成文件都保留任意 T、一个 usize 参数、`Vec<T>` 返回值、空前置条件及
完整官方后置条件；比较为 `(r1)@ =~= (r2)@`，不是容量或长度代理。
二者都在实际 Verus 检查中因同一 Global 构造错误失败，已通过义务为零。
原始 SMT 查询没有生成，不能声称不可满足，也不能声称关闭搜索条件的查询已经通过。
仅有七个待用搜索条件的模式定义，不是实际执行过的受限输入分析。
工具也没有另证契约可满足性或全局堆状态。

实际输入、完整比较、两个失败验证进程和重新执行对应关系已机械核对，
记录在 `tests/with-capacity/const-features/checker-correspondence.json`。
当时两次检查器源码快照逐文件对应七份规格输入，私有配置仅改变四个路径。
没有移除 Global 表达式来换取一个与原体脱离的成功检查。

最小 Global 构造在固定 Verus 下同样报错，在同一 Rust 1.98.1 的原生编译器下
实际编译成功，日志为
`tests/with-capacity/const-features/global-constructor-{verus,rustc}.{command.json,result.json,stderr}`。
它不使用 Vec、容量参数、Seq 契约或 const 调用，隔离了本次工具拒绝的触发点。
此有限结论随后获 `6611f73cab83` 独立确认，不扩大为对所有可能编码或其他工具版本的结论。

## 隔离前的原生行为、const 与配置检查

当时源体和聚合均由固定 Rust 1.98.1 原生编译器新编译成功；
它们不是 Verus 成功输出，`linked-inputs.json` 明确作了区分。
新测试程序同时调用真实标准库和该原表达式入口，五个用例实际通过：
精确 `fn(usize) -> Vec<T>` 类型、非静态且无额外 trait 的元素、
0/1/37 请求下空内容与容量下界、填满请求数量后的顺序和原容量、
对齐为 64 的 ZST 在 `usize::MAX` 请求下的最大容量，以及两类字节溢出 panic。
非 ZST 溢出请求分别覆盖 `isize::MAX / size_of::<u16>() + 1`、
`isize::MAX + 1` 个 u8 和 usize 乘法溢出；它们在分配之前失败，没有尝试耗尽内存。
容量和指针的原生观察、以及原源码中零字节绕过分配的分支，不是堆行为的形式证明。

八个参数、返回类型、默认分配器和局部元素借用逃逸的拒绝探针按原签名失败；
临时 Rust 文件均已删除，输入保留在 `.input.json` 中。
稳定运行时调用的新测试程序在 `RUSTC_BOOTSTRAP=0` 下编译通过。
真实标准库的稳定 const 调用被拒绝；启用 const_heap 后，零请求和 ZST 最大请求的
实际 const 求值通过。编译原体还须开启宿主要求的 const_trait_impl。
这些探针不承诺任意非零堆分配可以用于静态常量。
禁用全局 OOM 处理时，源入口库编译成功，但访问 with_capacity 被拒绝；
这不是重新构建了采用另一配置的预编译标准库。

首次原生构建缺少 const_trait_impl，在执行任何测试方法前失败，
输入及诊断保留在 `tests/with-capacity/native/` 和 `suite.stderr`。
只补全实际编译器要求的 feature，未改源体、契约或输入域；受影响的两轨均重新执行，
先前 `source/`、`module-cfg/`、`engineer/` 中的候选与错误仍在。

随后实际执行 `python3 -m unittest discover -s tests -p test_with_capacity.py -v`，
完整记录在 `tests/with-capacity/suite-const-features.stderr`。
15 个测试方法中，五个正式成功断言因 Global 限制失败，分布在源体/聚合、
客户端及完整性三个方法内；另一个 IR 检查因输出换行误报。
仅修正该检查的空白规范化后，单独执行该方法通过，见 `suite-lowering.stderr`，
没有重跑未变的原生用例、构建或检查器。旧误报仍保留，整份测试不记作通过。

## 已确认结论与隔离待审范围

原表达式、配置作用域、官方契约复用、输入域和上述固定工具限制已有独立确认。
本轮尚需独立审查的是默认/候选入口隔离、六项配置差异、目标和比较的对应、
真实失败保留及默认连接回归；工程侧记录不等于独立审阅通过。
不能以默认构建、原生编译或完整序列比较文件替代未完成的正确性与完整性证明。
唯一后置条件没有冗余条款，容量、分配、溢出和 const 稳定性也没有被伪装成
Seq 契约已经证明的内容。当前不满足完成条件，不增加独立双轨完成数量。
覆盖表仍为 138 行、独立双轨完成仍为 7；本轮仅更新 with_capacity 一行，
其余 137 行及 Cow、AsMut、const/cfg、独立容器缺少 cc 的历史失败不变。
私有 scratch 的具体命令见 [覆盖说明](../inventory/COVERAGE.md)；
`review-criteria-temporary.txt` 保持原样。

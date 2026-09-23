# 固定来源、工具版本与转换的证明边界

## 泛型 Index 保留继承前提，完整性停在关联输出观察

本轮亲读 Rust 1.96 `alloc/src/vec/mod.rs:3825-3832`、
`core/src/ops/index.rs:1-74`、`core/src/slice/index.rs` 中的 sealed trait 和
全部相关实现，以及 `core/src/index.rs` 的 Last/Clamp。
索引并不限于 usize 和旧 ops 范围：源码共有 25 类实现，其中 IndexRange
是 core 私有类型，其余 24 类均纳入本轮原生比较；没有将这些实例另计为 API。
来源根目录仍为 `/home/chentianyu/nanvix-rust-std-spec-survey/rust-1.96/library`。

`specs/vec/index.rs` 只建立共享接收者具名展开的自由证明入口，仍执行
`Index::index(&**vec, index)`；T、I、A 和原关联 Output 不变。
契约同时保留固定官方 `std_specs/core.rs:47-60` 的继承前提和
`std_specs/vec.rs:178-190` 的存在切片、call_ensures 后置条件。
Deref（`std_specs/vec.rs:248-253`）提供同序列切片，切片 Index
（`std_specs/slice.rs:310-313,330-336`）委托原 SliceIndex 契约
（`slice.rs:119-168`）。不新增标准库声明、输出唯一性规律或观察假设。
这里只得到相对于这些固定依赖的正常返回证明，不重新证明底层切片实现。

自由入口最初与参数同名，引发宏展开 E0109/E0618；改入口名称为 index_source
后编译通过，原候选和失败保留。另一个实际差别是 trait 继承的 track_caller：
未显式保留时 panic hook 报告入口内部位置，标准库报告调用点。
修正只保留原 inline 和该继承属性；新库的精确调用位置测试通过，
没有改变执行表达式、返回契约或合法泛型域。

当前 `proofs/correctness/vec/generic-index/caller-preserved-source/` 和
`caller-preserved-aggregate/` 的 Verus --compile 均退出 0，分别通过 1 与 4
个义务，均保存了本次新库。实际 IR 与 AIR 仅使用 Vec Deref 和切片 Index 的
执行委托，关联输出仍为 I 的 SliceIndex::Output，不循环依赖 Vec Index 目标。
当前原生程序 8 项通过，source/std 客户端 8 个义务通过；24 个返回类型和借用
拒绝探针的原预期全部满足。它们不证明 Rust 1.96 和宿主 1.98.1 普遍等价，
也不替代全泛型域的完整性分析。

当前真实 analyze/reexecute 的记录在
`proofs/completeness/vec/generic-index/caller-preserved/`：
恰好一个目标，两次均退出 2，原泛型、参数、关联返回类型、requires/ensures
和源码副本完整对应。失败发生在 observations/observation_gap；
尚无比较、查询、搜索条件或完整性义务。原生检查器没有从 SliceIndex 约束解析出
所需关联输出观察，本轮也没有找到保持原域的已实现替代表示。
没有据此宣布契约内在不确定、声称 usize 实例证明了泛型 API，或修改固定工具。

首次显式 replay --config 覆盖了已保存的 selector，误选 14 个目标；
这个范围错误及输出没有删除或冒称单目标结果。只去掉该覆盖参数后，
重放恢复了原 selector；后续只有 caller 属性变化才重新分析当前源码。
完整 unittest 仍保留正式失败：10 个方法中完整性方法的两个子项失败；
修正后仅执行受影响的检查。默认聚合、with_capacity 隔离及其余 137 行覆盖保留，
总数 138、独立双轨完成 7，本 Index 未计完成。
有限源码对应、冗余检查、所有准确记录和独立私有目录命令见
`issues/vec-index-source-correspondence.md`；独立判断尚未完成。

## IntoIter 的当前剩余状态与两个尚未解决的编译限制

本轮亲读 Rust 1.96 `alloc/src/vec/into_iter.rs:245-308`，特别是
`count(self) -> usize` 的 `self.len()`（301-303）和
`last(mut self) -> Option<T>` 的 `self.next_back()`（306-308）；
同时核对 `core/src/iter/traits/iterator.rs:193-221,238-256`。
完整 `impl<T, A: Allocator>`、Item=T 和按值语义保留。trait 默认遍历说明
没有被用来将具体覆盖方法重写成循环。

官方 `vstd/std_specs/iter.rs:12-54,245-300` 已给出当前 remaining 及
next/next_back 转移、ExactSizeIterator::len 的精确长度关系；
`std_specs/vec.rs:350-385,393-401` 给出真实 IntoIter 的类型、恒为 true 的
prophetic laws 及 Vec::into_iter 构造关系。构造时 into_iter_elts 与 remaining
相等，不推出消费后的同一关系。本轮不新增 iterator View、该关系的公理、
元素 trait 或静态寿命要求，依赖和继承的 len 都不新增 API 计数。

`proofs/correctness/into_iter/isolated/consumers.rs` 的两条真实绑定候选只有
一个后置条件：count 返回当前 remaining 的精确长度；last 为空时返回 None，
否则返回末项本身。辅助分段 trait 声明只补 count/last，依据固定官方
`rust_verify_test/tests/external_traits.rs:344-373`，不重建 IteratorSpec。
原体以局部同名 trait 放在真实 IntoIter 类型上，避免 Rust orphan impl；
这个名称作用域转换不代替标准库绑定或独立源码确认。

最新 count 在 `proofs/correctness/into_iter/erased-count/` 由固定 Verus
--compile 实际生成新库，1 个源体义务通过，IR 只调用 len。
last 的原 mut self 在前端被拒绝；无任何契约的同签名最小复现也失败。
固定 `rust_verify/src/rust_to_vir_func.rs:416-424` 明确拒绝该 receiver。
具体标准库绑定另在独立 crate 中报告重复 Iterator 实现，IR 同时列出既有
IntoIter Iterator impl 和具体假设的同一实现路径；单独 count、无后置条件的
诊断也失败。这些是本版本、本输入路线的可复现限制，不是所有编码不可能或
上游 Rust 有缺陷的结论，没有修改固定工具。

本轮真实 analyze 与 replay --reexecute 恰好选择两个具体目标，均退出 2，
每个目标都是编译错误、零通过义务，无原始 SMT 查询。count 的原生比较为
`r1 == r2`，last 同时比较 Option 变体及 Some 中的 T；没有派生布尔观察替代。
三份输入快照、泛型、按值参数、返回类型与当前候选完整契约一致。
具体比较、原生 harness 和错误保存在
`proofs/completeness/into_iter/selected-targets/`。没有声称原始查询不可满足、
搜索条件关闭后的成功或契约可满足性已获工具证明。

完整 unittest 已实际执行并失败，包含绑定、last、组合客户端和完整性失败。
运行还发现早期手写 ghost 注解没有随 --compile 消除；依据固定宏的
`verus_keep_ghost_body` 条件修正后，新 count 源库及新链接程序重新通过。
`tests/into-iter-consumers/selected-tests.stderr` 中 5 项受影响或新增检查通过；
新程序的 6 个原生用例通过，包含安全 Drop、ZST、非静态元素和不可 Clone 的
借用分配器。last 库仅为固定 rustc 编译的原体，明确不冒称 Verus 源码证明。
十个签名/寿命拒绝探针的原结果保留，没有为 usize 结果捏造元素寿命约束；
临时 .rs 已删除。8 个泛型状态组合客户端仍因绑定错误未产生通过义务。

两个 API 均不计完成，独立双轨总数保持 7/138；只有相应两行覆盖改变。
未经编译通过的绑定和 last 原体没有接入 specs/into_iter、默认聚合或检查配置。
临时冗余准则保持，正常独立审阅仍须确认源码和状态对应及这两个限制。
本轮不改动其他 136 行、已确认七个目标、with_capacity 隔离、Cow 或 AsMut，
也不把正常返回契约、final 状态或具体 Drop 测试当作析构的形式证明。
完整来源、历史失败和私有输出命令见
`issues/into-iter-consumers-source-correspondence.md`。

## with_capacity 的限制已确认，默认构建与候选分离

已亲读 Rust 1.96 `alloc/src/vec/mod.rs:467-525`，并沿
`with_capacity_in` 的 const impl（`915-978`）、
`raw_vec/mod.rs:168-180,428-483,570-576,617-620,882-907` 和
`core/src/alloc/layout.rs:59-122,526-533` 核对容量、ZST 和溢出。
默认分配器是原 Global；非 ZST 正常返回的容量至少为请求值，文档允许超额容量。
零字节布局不分配，ZST 对外容量始终为 usize::MAX；布局失败在分配之前发生，
isize::MAX 限制的单位是字节，不是一概限制元素个数。

候选 `specs/vec/with_capacity.rs` 保留原调用表达式，只明确 `Self = Vec<T>`，
沿用官方 `vstd/std_specs/vec.rs:114-123` 的唯一空序列后置条件。
无前置条件、额外元素 trait 或新增假设。文件内层 cfg 保留原 OOM 条件；
const 源体在宿主编译器下须开启 const_heap 和 const_trait_impl。
原 libstd 的不稳定 const 可用性与验证自由函数的稳定性元数据不能混为一谈。

任务 `6611f73cab83` 已独立确认上述有限源码对应、cfg/const/泛型域、唯一条款
无逻辑冗余及原 Global 构造的固定 Verus 限制。不是 Rust 源码/文档缺陷，也不是
所有可能编码均不可行的证明。本轮只作构建入口隔离，新的隔离尚待独立审阅，
不重新调查 Global 兼容性或改变信任边界。

### 隔离前的已保存依据

关键限制发生在契约义务之前：固定官方 `vstd/std_specs/alloc.rs:6-11`
将 Global 作为 opaque 外部类型，固定 Verus 不允许原体中的构造访问。
隔离前逐项、聚合 `--compile` 以及仅含 Global 构造的最小复现均实际失败；
中间表示确认原体只调用 with_capacity_in，未循环调用目标假设。
这说明官方委托后置条件可复用，并不意味着原表达式的每个构造均已受工具支持。
没有改变固定工具，也没有采用可执行改写绕过此限制。

当时真实 analyze 与 replay --reexecute 均发现一个目标并生成完整序列比较，
同一候选的两次 Verus 检查却都失败、零通过义务，未生成原始 SMT 查询。
输入对应和完整比较已经核对，但不能报告正确性、确定性、不可满足或关闭搜索条件
后的成功。隔离前记录在 `proofs/correctness/vec/with-capacity/const-features/`、
`proofs/completeness/vec/with-capacity/const-features/`；
首次发现失败、此前候选及后续诊断都保留。

当时固定 Rust 1.98.1 对原体及聚合的原生编译成功，新测试程序的五个用例通过；
八个精确类型和元素寿命拒绝探针、const 与 OOM 配置检查也实际执行。
它们不构成 Rust 1.96 与宿主版本全部实现等价的证明，也不证明容量或分配行为。
首次缺少 const_trait_impl 的编译错误，以及完整 unittest 中的正式失败均保留；
仅由 IR 换行导致的本地断言已单独修正验证，不重复未变工作。
具体输入、语义边界、原生结果和已确认的有限限制见
`issues/vec-with-capacity-source-correspondence.md`。
上一工程轮覆盖表仍为 138 行，仅本目标和三个基础入口的已审字段变化，其余 134 行不变。
独立双轨完成仍为七个；Cow、AsMut 和本目标的未完成部分没有被计作通过。

### 当前入口、六项配置差异与实际结果

默认 `specs/lib.rs` 只移除 with_capacity 模块及 `const_heap, const_trait_impl`，
保留 `allocator_api` 与所有非容量模块；默认 `specdet.toml` 只移除该 include 项。
独立入口 `specs/with_capacity_candidate.rs` 保留原 feature 行和
`pub mod vec { pub mod with_capacity; }`，引用同一份 `specs/vec/with_capacity.rs`；
原 cfg、任意 T、const 签名、`Vec::<T>::with_capacity_in(capacity, Global)`、
契约和命名空间均未变。逐 API 入口及 Global 最小复现不变，不用新实现换取成功。

候选检查脚本先由未改动的 `scripts/borrowed_scratch_config.py` 完成四项路径
调整，再显式改 `build.entrypoint` 与 `targets.include`。最终六项授权差异见
`proofs/completeness/vec/with-capacity/isolation/checker/config-changes.json`；
不能把它称为与默认目标集相同的纯路径配置。analyze 仍只选
`vec/with_capacity.rs::vec::with_capacity::with_capacity`，重放仍实际 `--reexecute`，
完整序列比较 `(r1)@ =~= (r2)@` 未变，不移除 Global 来生成脱离原体的证明。

`proofs/correctness/vec/with-capacity/isolation/default/aggregate.*` 保存默认
固定 Verus `--compile --num-threads=1`、无验证过滤器的退出 0 和
`3 verified, 0 errors`，并有当次新生成的 `libvec_specs.rlib`。
隔离前 `const-features/aggregate.result.json` 的退出 1 和原 opaque 构造诊断
仍保留。当前 `isolation/candidate/{source,candidate}.*` 也均退出 1；
源体和独立候选仍未完成正确性。正确性脚本每项仍要求成功编译及 1 个通过义务。
这些相对路径均位于 `proofs/correctness/vec/with-capacity/`。

候选当前 analyze/reexecute 记录在
`proofs/completeness/vec/with-capacity/isolation/checker/`，两次均退出 2、
`compile_error`、0 个通过义务、无原始 SMT；两个包装脚本均退出 1。
完整性脚本即使面对退出 0，也拒绝空目标或零义务。
未改动的 reused-basic 脚本通过默认 `lib.rs` 完成两阶段连接回归，
恰好三个原目标，每目标每阶段各 1 个通过义务，CLI 均退出 0；
记录在 `proofs/completeness/vec/reused-basic/isolation/checker/`。
这不重授三项 API 的语义确认，也不扩大已确认范围。

`tests/with-capacity/isolation/regression/` 保留构建、两组检查器和客户端结果，
客户端仍因原 Global 构造退出 1。新隔离套件首次执行为 9 项中 8 项通过、1 项失败，
见 `.argus_subagents/vec-capacity-isolation-a8d858022146_logs/stderr.log`：
默认编译 stdout 只有三个义务的汇总，未含测试要求的源函数名称。
修正后的断言核对实际 AIR 中三个源体的 `Function-Def`、三个 `check-valid`，
并要求 SMT 记录恰有三个 `check-sat` 和三个 `unsat`。
仅修改的默认构建测试与更新后的覆盖范围测试再次执行，两项通过，记录为
`tests/with-capacity/isolation/selected-tests.command.json`、
`selected-tests.result.json` 和 `selected-tests.stderr`；
新默认编译位于 `proofs/correctness/vec/with-capacity/isolation/default-obligations/`。
首次失败及原默认构建均保留，未重复其余未变检查，也不声称另跑了一次九项全套。
原完整 API 套件的正式成功断言未改 skip/expectedFailure，本轮未重跑或宣布它通过；
原生行为与 cc 环境工作也未重复。

本轮覆盖表仅更新 with_capacity 行，其余 137 行与
`tests/with-capacity/isolation/before/coverage.tsv` 逐字、逐字段一致，
总数仍为 138、独立双轨完成仍为 7；本目标仍是双轨未完成。
Cow、AsMut、此前 const/cfg 和独立原生链接缺少 cc 的失败全部保留。
新私有输出目录的当前命令及隔离待审范围见 `inventory/COVERAGE.md`；
项目临时 `review-criteria-temporary.txt` 原样保留，工程执行不替代独立确认。

## 三个已有官方契约的原体复用

本轮亲读 Rust 1.96 `alloc/src/vec/mod.rs:4256-4264,3033-3049,3749-3756`，
`core/src/default.rs:7-140` 和 `core/src/ops/deref.rs:3-151`。
三个原体分别是 `Vec::new()`、`self.len() == 0`、`self.as_slice()`。
Default 不需要 `T: Default`；is_empty 与容量无关；Deref 的 `Target=[T]`
及共享接收者寿命确定返回的是完整已初始化前缀，而不是 spare capacity。

固定官方 `vstd/std_specs/vec.rs:105-108,214-219,248-253` 已有三条具体契约，
`std_specs/default.rs:5-11`、`std_specs/core.rs:29-36` 保留相应 trait 结构，
没有附加方法前后置条件。`specs/vec/reused_basic.rs` 逐字复用具体契约，
不新增 `assume_specification`；其接收者命名及自由函数命名空间变化与原体对应。
Default 依赖官方 new；is_empty 依赖 len 和既有长度公理；Deref 依赖 as_slice。
本轮另外亲读这些委托的 Rust 文档和实现，但不把依赖本身计为已证明 API。

三个逐 API 正确性入口直接导入同一文件，没有独立的模型或契约副本。
固定 Verus 对当前源体各完成一个义务并实际编译，聚合完成三个义务并编译，
记录在 `proofs/correctness/vec/reused-basic/source/`。
实际中间表示分别只调用 new、len、as_slice，没有以目标假设证明自身。

`proofs/completeness/vec/reused-basic/engineer/` 保存真实分析和重新执行，
各恰好选择三个入口、每个入口各一个通过义务和不可满足的原始查询。
Vec、bool、slice 的比较分别为 `(r1)@ =~= (r2)@`、`r1 == r2`、
`r1 =~= r2`。所有搜索开关关闭；没有把输入限制为零长度或添加类型要求。
两次运行的六份源码快照与当前规格一致；完整声明、输入和原体的机械对应见
`tests/reused-basic/engineer/correspondence.json` 及 `checker-correspondence.json`。
检查器的 const/trait 归属不由自由函数记录表达，仍须另行核对真实源码和编译边界。

本轮新编译程序的七个原生用例通过，另有六个客户端义务和十四个按预期拒绝
的类型及借用探针。它们包含非静态、无额外 trait 的元素和不可 Clone 的本地
分配器；覆盖空、预留容量而为空、单元素、重复与顺序、ZST 及返回有效前缀。
稳定 const is_empty 编译通过。不稳定 const Default 的首次探针缺少
`const_trait_impl` 而失败，补全宿主要求的两个 feature 后仅执行改变或此前
未执行的三项检查，全部通过；原输入和失败保留。记录见 `tests/reused-basic/`。
源体 Default 仍只表示稳定运行时方法，未把 const trait 能力提升为稳定接口。

这些是相对于固定 vstd 和其既有内容观察的组合证明，已由任务
`af05f6b80c5a/round-0001.json` 独立确认，包含有限源码对应、const 边界和冗余检查。
独立审阅的原生链接因缺少 `cc` 失败；其另核对了工程侧当轮新构建及七项运行
记录，没有冒称独立原生重跑成功。本次仅同步既有结论，不重审未变代码。
工具未另证契约可满足性；新编译的合法调用只提供补充依据。
序列不证明分配器身份、物理地址、容量或全局堆状态，Rust 1.98.1 上的原生
运行也不证明它与 Rust 1.96 的所有底层实现普遍等价。
覆盖表仅改变三个新目标及两个所有权转换的已审字段，其余 133 行及旧失败不变。
独立审阅继续适用项目内临时冗余准则，有限源码对应见
`issues/vec-reused-basic-source-correspondence.md`，不以执行能力代替语义确认。

## 两个所有权输入转换的当前依据

任务 `db4ff3669ca5` 的独立审阅已确认本节两个目标的有限源码对应和双轨结果。
本轮亲读其 `round-0001.json` 后同步原待审说明，不重新验证未变代码。
审阅者实际重新编译源体并运行真实完整性分析和重放；原生链接受容器缺少
`cc` 限制，另核对了工程侧当轮新构建及七项运行记录。该限制不被隐藏，
确认范围不扩展到 Cow、AsMut 或其他依赖 API。
以下源码阅读和执行记述保留自所有权转换工程轮，其中的“本轮”不指当前三个复用目标。

本轮亲读 Rust 1.96
`/home/chentianyu/nanvix-rust-std-spec-survey/rust-1.96/library/alloc/src/vec/mod.rs:4362-4375,4401-4416`
以及 `library/core/src/convert/mod.rs:458-592` 的实现和文档。
数组转换分配 Vec 并移动元素，原体为 `<[T]>::into_vec(Box::new(s))`；
装箱切片转换转移既有分配，原体为 `s.into_vec()`。
后者的委托源码 `library/alloc/src/slice.rs:463-486` 以原指针、长度和原分配器
调用 `Vec::from_raw_parts_in`，并明确不克隆、不另行分配。

固定官方 `toolchains/upstream/source/vstd/std_specs/smart_ptrs.rs:12-21`
提供分配器泛型 `into_vec` 和 `Box::new` 的内容关系；
`array.rs:11-21,90-126` 提供数组完整序列及数组到切片转换，
`slice.rs:13-17` 和 `view.rs:22-29,104-108` 提供 slice、引用与 Vec 观察。
本轮 Verus 中间表示确认数组原式实际经过这些官方调用。
没有新增同名视图或可信答案，没有从依赖客户端冒充目标证明。

`specs/vec/owned_conversions.rs` 的两条真实绑定均只规定 `result@ == s@`。
其任意 T、const N、A: Allocator、移动语义及配置条件不变。
数组条件仅作用于根级 Verus 块中的数组内联模块；装箱切片仍不受该条件限制。
默认和禁用全局 OOM 处理两种客户端编译及中间表示确认了这个作用域。
两条契约没有前置条件；长度和逐元素关系已由完整序列等式蕴含，不重复列出。
新增契约和源体的有限对应已由上述正常独立审阅确认，不由工程执行能力自动授予。

两个源体在 `proofs/correctness/vec/owned-conversions/` 各验证一个义务并实际编译；
最新聚合为同目录 `aggregate-verus-module.*`，保留原有模块，零义务仅算编译。
真实完整性分析与重新执行均在
`proofs/completeness/vec/owned-conversions/verus-module/` 各验证两个目标，
每个目标每次一个义务、原始查询均不可满足。完整比较为返回 Vec 的全部有序序列，
原始查询关闭全部搜索开关，没有缩窄合法输入或手工改写模型。
工具本身没有额外证明契约可满足性；无前置条件的源体及合法原生调用提供本轮补充依据。

`tests/owned-conversions/engineer/` 记录本轮新编译程序的七个原生用例及八个拒绝探针。
自定义分配器没有 Clone，借用局部计数器并拥有唯一的 Box 资源；
非空非 ZST 装箱切片转换保持原存储地址和该资源，转换时未调用分配或释放，
最后释放由同一分配器完成。这是指定输入上的原生补充结果，不是由 Seq 得到的
地址或分配器恒等证明，也不被扩展为数组必须复用某个原堆分配的关系。
原生程序和复制的两个原体使用项目私有 Rust 1.98.1，
不能据此宣称 Rust 1.96 与宿主所有底层实现普遍等价。

本轮仅更新 `inventory/coverage.tsv` 的两个相应行，其他 136 行和全部 Cow、
AsMut 失败继续保留。首次直接条件属性、随后模块内普通宏所致的数组发现遗漏、
以及本地结果格式断言的失败日志也均保留；只修正规格布局和测试，不修改检查器。
精确路径、历史候选及当前私有输出重放命令见
`issues/vec-owned-source-body-embedding.md` 和 `inventory/COVERAGE.md`。
本轮没有重跑未变兼容性调查，也没有修改收集器、官方工具或其他实验。

## 借用依赖已有独立确认

本轮已亲读
`/home/chentianyu/.argus-vec-specgen-astra-20260922/projects/s-6a17c286/handoffs/fc975bfe5a6c/round-0001.json`。
其中正式审查确认四个原借用表达式的源码对应及正确性、三条同状态冗余条件的删除，
以及两个 AsRef 的内容完整性分析和重新执行。两个 AsMut 仍缺完整性，不计入双轨完成。
本轮只落实这项既有判断，不重审未变契约；下文此前轮次的待审说明仍作为历史保留。
`runtime-review-readiness.json` 已解除旧环境等待，它不授予 Cow 的语义确认。

## Cow 的真实构造和当前观察

以下源码阅读及 Rust 构建记述来自上一工程轮，保留其依据；
本轮新增工作是本节末尾的固定检查器入口检查，不重复未变源码证明。

本轮亲读 Rust 1.96 `library/alloc/src/vec/cow.rs:6-53` 的四段文档和四个函数体、
`library/core/src/convert/mod.rs:458-593` 的 From 契约，以及
`library/alloc/src/borrow.rs:86-180` 的 Cow 文档和两个变体。
`library/alloc/src/slice.rs:836-846` 明确 `[T]` 的 ToOwned::Owned 为默认分配器的 Vec<T>。
三个借用构造必须为 Borrowed；移入 Vec 必须为 Owned。四者都不分配、不克隆，
并保持全部元素及顺序；Cow 类型需要 Clone 并不意味着这些转换调用 Clone。

官方 `toolchains/upstream/source/vstd/std_specs/borrow.rs:80-89` 的 Cow slice View
额外要求 `T: View`，且消除了枚举变体，故本轮没有使用它或修改它。
`specs/cow/observation.rs` 对真实 Cow 直接匹配，产生
`CowContents<T>::Borrowed(Seq<T>)` 或 `Owned(Seq<T>)`。
它使用枚举定义及官方 slice/Vec 序列，无新公理、任意函数或可信观察关系。
`specs/cow/conversions.rs` 的每条契约只写一个观察等式，不重复已蕴含的
变体条件、长度或逐元素关系。没有前置条件，也没有新增泛型或生命周期限制。

四个源体分别保留 `Cow::Borrowed(s)`、`Cow::Borrowed(s as &[_])`、
`Cow::Owned(v)`、`Cow::Borrowed(v.as_slice())`。
数组 cast 依赖官方 `toolchains/upstream/source/vstd/array.rs:10-20,90-126`；
Vec 引用依赖 `std_specs/vec.rs:236-240`，原方法文档和实现为
Rust 1.96 `library/alloc/src/vec/mod.rs:1808-1841`。
官方 `std_specs/convert.rs:8-21` 的 From 扩展框架原样保留，
本项目只添加四个不同 UFCS 身份的真实绑定。正确性入口没有导入这些假设。

本轮四个源体各验证一个义务并编译；当前聚合编译也通过。
这些结果位于 `proofs/correctness/cow/cow-engineer/`。
但是实际 specdet 分析和重新执行均因把返回类型中的 `'a` 当作类型而中止，
没有生成所需比较、查询或完整性证明。详见
`issues/specdet-cow-lifetime-type.md` 和 `proofs/completeness/cow/cow-engineer/`。
这四个 API 仍不计入双轨完成；也不从这个前置解析失败推断后续观察必定可支持。
本轮没有修改被解释源码、固定工具或其他实验。

任务 `4566f129a548` 的独立审阅随后确认了上述有限源码对应、原输入域、
透明观察及四个非零正确性义务，并按项目临时准则确认没有应删的逻辑冗余。
审阅者实际 analyze、replay --reexecute 及解析对照确认的是当前直接路径的失败，
不是所有等价编码都不受支持。当前工作只检查固定工具已实现的入口；
未变源体、借用契约及收集器沿用已确认结论，不重新生成。

本轮进一步亲读固定 specdet 的原生类型、观察和转译实现及相应测试，
并在 `from_vec` 原保存契约上检查未修改的辅助解析和视图注册组件。
辅助解析能保留完整 `Cow<'a,[T]>` 注解，但所有原生观察先经过仍失败的类型解析；
来源 trait bound 和 impl 注册也没有为现有 `CowObservation` 建立输出观察。
47 项既有工具定向测试通过，只说明所检查的支持边界，不是 Cow 完整性结果。
实际依据为 `proofs/completeness/cow/native-support/inspection.json`、
`native-tests.stderr` 及 `issues/specdet-cow-lifetime-type.md` 中的精确源码路径。
在已实现入口内未找到符合本任务约束的编码，当前停在管理者需另行授权的工具范围；
本轮未修改任何规格、源体或工具，新判断仍须独立审阅。

## 本轮等价删减与研究范围

本轮读取的共享及工程师指南分别为
`/home/chentianyu/.argus-vec-specgen-astra-20260922/skills/_shared_verticals/software/verus-spec-generation-and-repair.md`
和该目录下 `engineer/formal-verification/verus-spec-generation-and-repair.md`。
项目 Wiki 原索引为空；本轮把固定 View 的已验证同余关系及信任边界写入
`.autors/rust-std-vec-specgen-astra-2026-09-22/wiki/pages/contracts/borrowed-vec-view.md`。
建议中提到的 `RESEARCH_NOTES.md`、`METHOD.md` 不在当前项目中；
本轮沿用本文件记录实际依据，没有创建替代方法或计划文件。

项目内 `runtime-review-readiness.json` 说明受限审查执行已恢复，
同时明确没有授予任何 API 语义确认。本轮不再等待旧环境条件，
也没有监听项目外的操作记录。仍须由正常独立 Reviewer 检查原源码、
官方 View/Deref 依赖、既有证明入口的对应、双轨结果和临时冗余准则。

当前 `specs/vec/borrowed.rs` 只删了三个可由同状态逻辑值等式推出的 View 条款；
没有改动函数体、类型、生命周期、合法输入、slice 契约或终态值等式。
完整的逐条依据及原候选位置见 `issues/source-body-embedding.md`。
本轮重新编译了四个源体及规范聚合；六个同余、原契约和写回客户端义务通过。
两个 AsRef 的实际分析与重新执行均各有一个通过义务和 `unsat` 原始查询。
两个 AsMut 本轮仍在问题生成前报告 `unsupported_mutable_return`；
这不是 Verus 正确性失败，也不是两个 API 的双轨完成。

本轮主要记录位于 `proofs/correctness/vec/redundancy-engineer/`、
`proofs/completeness/vec/redundancy-engineer/`、
`tests/redundancy-engineer/` 和 `inventory/redundancy-engineer/`。
`inventory/COVERAGE.md` 给出准确命令和私有目录重放方式。
`specdet.toml` 和固定工具均未修改；配置副本只调整四个路径，
完整比较策略、目标、前提和求解设置保留。源体等价判断和两个 AsRef 的
独立语义确认尚未完成，因此尚未推进依赖它们的新 API。
当前 2/138 只表示工程双轨结果，不能当作模块完成或正式独立结论。

## 初始基线与此前工程轮的记录

以下保留初始生成及 `closure-engineer` 轮的说明；
其中“本轮”、原契约和旧输出均指这些历史轮次，不替代上面的当前结果。

本轮在执行前亲自读取了共享工作指南
`/home/chentianyu/Argus/argus/verticals/software/skills/verus-spec-generation-and-repair.md`
和工程师指南
`/home/chentianyu/Argus/argus/verticals/software/skills/engineer/formal-verification/verus-spec-generation-and-repair.md`。
同时读取本实验 Wiki 的
`.autors/rust-std-vec-specgen-astra-2026-09-22/wiki/INDEX.md`；本轮仍无页面。
后续独立审查仍需重新读取共享指南和审查者自己的指南，不能由这份记录代替。

## 官方工具与 Rust 语义源码是不同版本

被解释的只读源码是
`/home/chentianyu/nanvix-rust-std-spec-survey/rust-1.96/library`。
没有读取旧生成 Vec 规格、旧证明、兼容后端或 Slice 实验结果作为依据。
本实验的固定 Verus 是官方 `release/0.2026.09.20.aef82ed`，
提交 `aef82eda71838deef4a8cd0260fda6c9504be9b9`；
其宿主为 Rust 1.98.1，而不是 Rust 1.96。

官方网络来源经 Argus 获取，精确保存位置如下：

| 来源 | 本实验保存的原文 |
|---|---|
| GitHub 官方 release 元数据及 Linux 发布文件摘要 | `toolchains/.argus/sources/a792f531e8046ee03896a302.txt` |
| 官方 release tag 对应的提交 | `toolchains/.argus/sources/702bc082a66e9add4cb589b2.txt` |
| 该提交的 `rust-toolchain.toml` | `toolchains/.argus/sources/af46cfcf08e5371929bd43cf.txt` |

`scripts/install_baseline.sh` 只向本实验的 `toolchains/` 下载、解压和安装。
发布 zip 的 SHA256 与 GitHub 官方 asset digest 相同；安装输出保留在
`.argus_subagents/vec-official-baseline_logs/stdout.log`。
`scripts/check_baseline.py` 随后逐字比较全部 3,873 个发布文件，以及
官方提交归档中的 133 个 vstd 文件，结果在
`toolchains/readiness/baseline-content.json`。
本次工程复跑另存的逐字比较结果为
`toolchains/readiness/borrowed-closure-engineer/20260922T065737Z/baseline.stdout.json`，
仍是 3,873 个发布文件和 133 个 vstd 文件相同，没有重装或修改工具。
发布自带的 `libvstd.rlib` 和 `vstd.vir` 没有重建或修改；
源文件来自同一官方提交的 `toolchains/upstream/source/vstd`。
没有使用其他实验的安装、缓存或可写验证目录。

Rustup 的六个要求组件实际安装成功，但最初的命令在随后尝试更新 Rustup 自身时
因隔离的 CARGO_HOME 内没有 Rustup 而返回错误。安装脚本已按其原生 help
改为 `--no-self-update`；没有重新下载或重装已安装组件。
后续实际 rustc、Verus、库构建和证明执行确认了当前安装可用。

| 实际执行的程序 | 结果文件 |
|---|---|
| Verus `0.2026.09.20.aef82ed` | `toolchains/readiness/verus-version.txt` |
| rustc `1.98.1 (48a229cea 2026-09-01)`，x86_64 Linux | `toolchains/readiness/rust-version.txt` |
| 项目私有 Rustup 当前工具链 `1.98.1-x86_64-unknown-linux-gnu` | `toolchains/readiness/active-rust-toolchain.txt` |
| 发布内的 Z3 `4.16.0` | `toolchains/readiness/z3-version.txt` |
| 实际 specdet `0.3.0`，Python Z3 `4.12.5` | `toolchains/readiness/specdet-version.txt`、`specdet-doctor.json` |
| checker CLI help 与 Python 实际加载路径 | `toolchains/readiness/specdet-cli.txt` |
| Verus 的本版本 help | `toolchains/readiness/verus-help.txt` |

两个 Z3 版本不同，未将它们混为一个求解器。Verus 义务由发布的求解器验证，
specdet 的原生查询由其实际 Python 后端求解；两者的当前结果均保留。
checker 入口加载的是
`/home/chentianyu/spec-determinism-tool/src/specdet/cli/main.py` 和
`src/specdet/adapters/verus/backend.py`，与本轮读取的文档和源码一致。

## 已有视图与原实现的连接

先确认官方视图和委托关系，再生成 `specs/vec/borrowed.rs`：

| 对象或依赖 | 固定官方定义或只读源码 |
|---|---|
| `Vec<T,A>@ : Seq<T>`，无额外 T bound | `toolchains/upstream/source/vstd/view.rs:104-108` |
| `[T]@ : Seq<T>` | `toolchains/upstream/source/vstd/slice.rs:13-17` |
| 共享引用透明传递既有 View | `toolchains/upstream/source/vstd/view.rs:22-29` |
| Vec Deref 的完整内容契约 | `toolchains/upstream/source/vstd/std_specs/vec.rs:248-253` |
| Vec DerefMut 的初始/最终写回契约 | `toolchains/upstream/source/vstd/std_specs/vec.rs:255-261` |
| Rust 1.96 的 Deref / DerefMut 函数体 | `library/alloc/src/vec/mod.rs:3749-3765` |
| 四个原转换实现 | `library/alloc/src/vec/mod.rs:4274-4300` |
| AsRef / AsMut 的 trait 文档及签名 | `library/core/src/convert/mod.rs:109-223,226-375` |

这些官方 View 是本轮既定的可信抽象，没有再定义一个同名或替代 View。
源体证明是相对于未修改官方 vstd 的组合证明，不是在本轮重新证明 RawVec
及分配器的底层内存实现。slice 目标依赖的是既有 Deref 契约，不是假设该目标
AsRef 的答案。`proofs/correctness/vec/closure-engineer/as_ref_slice/crate.vir:3458-3490`
显示了实际检查的函数体与该调用关系。

两个只读契约无前置条件。返回 Vec 的契约为
`result == vec` 和 `result@ == vec@`；返回 slice 的契约为
`result@ == vec@`。前者的完整值等式位于 Verus 的值模型中，
不冒充物理指针表示的完整建模。两者保持任意 T、`A: Allocator` 和原接收者生命周期，
不要求 Copy、Clone、View、DeepView 或 `'static`。
原方法的函数体仍是单个 `self`，证明入口只是命名空间嵌入和绑定变量改名。
具体对应检查及尚待独立确认的部分见
`issues/source-body-embedding.md`。

## 当前检查能说明什么

`inventory/coverage.tsv` 将整个源码范围与当前结果连接起来。
四个独立源体 crate 分别实际验证一个义务并编译，且没有导入目标假设。
两个只读目标由真实 specdet 直接解析原 `assume_specification` 的完整 UFCS 身份；
不需要分析适配器，没有采用模型建议或更换 backend。
原始运行及重新执行均各得到一个已验证义务和不可满足的原始查询。
`scripts/collect_borrowed_results.py` 校验两次源码快照、泛型和返回类型、
零前置条件、原后置条件、观察关系、原始查询的全部关闭 guard 及非零义务，
再逐字导出所需的 `.rs` 和 `.smt2`。
本次工程复跑复用了该脚本的逐目标检查函数；已发布的 `.rs` 与新生成文件
仍逐字相同，当前查询和重放目录由 `inventory/coverage.tsv` 直接链接。
具体检查输出为 `inventory/closure-engineer/borrowed-evidence-check.log`。

这只证明所选内容观察的完整性。Vec 的容量、分配器身份和物理地址不在其
序列 View 内；其他全局堆状态也不是该 checker 问题的观察量。
工具明确报告没有运行前提/契约可满足性检查，没有把这一空缺写成通过。
本轮另外检查了合法调用见证：原函数体没有前置条件、循环或新可信答案；
原生调用覆盖空/非空、有序且含重复元素、ZST、非 Copy/Clone、非静态借用，
以及调用者经可变借用改变内容、顺序和 Vec 长度/容量。
两个 Verus 客户端证明也展示了不被冻结的合法写回，但不用于替代源体证明。

当前两个 AsMut 目标的正确性通过，而完整性被实际后端明确拒绝，
没有原生查询或成功 harness。可复现诊断及准确归属见
`issues/specdet-mutable-return.md`。
独立审查尚未进行；本实验没有据此宣告整个 Vec 模块完成，也没有公开提交问题。

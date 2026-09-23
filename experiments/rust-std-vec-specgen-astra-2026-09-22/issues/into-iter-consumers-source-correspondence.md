# IntoIter 的 count 和 last 与当前剩余状态

本记录范围是 Rust 1.96 `alloc/src/vec/into_iter.rs:245-308` 中的两个消费方法。
本轮仍未完成：count 源体已验证并重新编译，真实绑定与 last 原签名存在两个
可复现的固定工具限制。任务 `12969919776e` 的既有独立审阅已确认有限源码语义、
状态对应及这两个具体限制；这不等于两个 API 的双轨证明完成。
不涉及上游实现修改，不向外部仓库提交问题。

## 2026-09-22 的接收者规范化提案，尚未获准执行

本次只补齐局部决定及其依据，没有修改或编译规范化的 Rust 代码。
操作者要求提出问题，不是授权改写。两个原候选、原失败及默认聚合均保留；
count/last 不增加完成数，也不因等待此决定而阻塞不相关 API。

既有独立审阅还确认了 count 的非零源码义务、签名与寿命拒绝探针，以及两目标
analyze/reexecute 的真实编译失败。独立原生重跑因缺少 cc 和 C 启动对象未完成；
工程侧六个原生用例不能弥补 last 源码证明或真实绑定失败。
这些是 `12969919776e` 的既有结论，本次没有宣称新的独立审阅或重新执行。

### 最小改动只限 last 的隔离证明副本

原执行代码来自 `alloc/src/vec/into_iter.rs:306-308`，现有
`proofs/correctness/into_iter/source_last.rs` 保留了它：

```rust
fn last(mut self) -> Option<T> {
    self.next_back()
}
```

拟议执行代码仍位于同一 `impl<T, A: Allocator> Iterator for IntoIter<T, A>`
及 `type Item = T` 下：

```rust
fn last(self) -> Option<T> {
    let mut iter = self;
    iter.next_back()
}
```

若获准，仅在 `proofs/correctness/into_iter/` 下另存明确标识的隔离证明副本，
不覆盖原 `source_last.rs`、原标准库文件或现有失败快照。
现有 ghost 后置条件逐字保留在 `let mut iter = self` **之前**，观察调用入口的
`IteratorSpec::remaining(&self)`，仍完整规定 None/Some 及末项 T。
不增加前置条件、元素或分配器 trait 界限、寿命限制、observer 或公理。
count 不需要这项接收者改动；两条真实标准库绑定的目标和签名也不改。

这不是“仅加证明注解”：它改变了源码证明副本的可执行绑定与移动位置。
需要操作者明确允许这一有限源码对应方法，之后仍须独立审查，不能凭 Manager
判断或一次编译成功就采用为原体证明。

### 按值、借用与 Drop 的对应义务

外部仍按值消费整个 `IntoIter<T, A>`，不是改成 `&mut self`。拟议局部绑定接收
这个值的所有权，不复制或克隆元素、迭代器或 A；调用者在调用后不能再次使用
迭代器。`next_back` 只临时可变借用局部值，返回值仍是移出的 `Option<T>`，
不能逃逸指向局部迭代器的引用，也不能把 T 原本允许携带的非静态引用收窄。

需要特别审查的差别是析构作用域：原值属于参数绑定，拟议值属于函数体内
`let` 绑定；完整移动后的 `self` 不再拥有一个待析构副本。
按该方法只有一个拥有资源的执行绑定、且尾表达式仍为同一 `next_back` 的结构，
预期均在返回前销毁剩余区，并由同一个 IntoIter Drop 释放分配。
非空时移出的末项不再属于剩余区；正常返回后它由调用者持有。
这里的“预期”是待核对的源码对应判断，不是已经完成的 Drop 或展开等价证明。

原 Drop 在 `alloc/src/vec/into_iter.rs:541-559` 使用 `DropGuard`：
先销毁剩余切片，再释放分配。审查必须比较移动前后剩余区、末项所有权、
分配器析构及释放次数，并覆盖元素析构发生 panic 时返回值与 guard 的清理；
不得以 `final` 等式或普通返回内容证明替代这些检查。
不新增 `no_unwind`，不保证地址或栈布局相同，不把有限原生运行推广为所有
T、A 或 Rust 1.96 与宿主 Rust 1.98.1 的普遍等价。

语言规则的参考是本次读取的 Rust Reference
[移动与反初始化](https://doc.rust-lang.org/reference/expressions.html#r-expr.move)
及[参数、局部绑定的析构作用域](https://doc.rust-lang.org/reference/destructors.html#drop-scopes)。
它们支持上述需要比较的规则，不替代本项目指定版本的源码和对应证明。

### 真实绑定仍是另一项未解决的问题

固定前端在 `rust_verify/src/rust_to_vir_func.rs:416-424` 拒绝 `mut self`；
拟议改动只尝试避开这个已确认的语法分支，不能保证后续移动及 prophetic
remaining 的证明会通过。

`current-bindings/`、`binding-reproduction/` 已记录重复 Iterator 实现。
单独 count 以及去掉后置条件的对照同样失败，与 last 的接收者无关。
即使规范化副本成功，也不能据此接入默认聚合、宣布绑定成功或完成两个 API。
真实绑定须另找保持固定工具、原目标及现有契约的合法编码；此提案不授权
修改 Verus/vstd/std/specdet、增加额外假设或扩大可信基础。
条件未变时不重跑该失败；若另一个问题最终也需要越过授权边界，须另提具体方案。

### 获准后的验证顺序与停止条件

1. 先核对原体与副本的唯一执行差异、完整泛型及 ghost 消除，保留输入快照。
   用固定 Verus 实际 `--compile` 这个隔离副本；要求相关源码义务非零，
   IR 调用仍为官方 `DoubleEndedIterator::next_back`，不调用 last 的目标假设，
   不用 `external_body`、`admit` 或新的可信包装。若出现新前端或移动错误，
   保存新诊断，不继续改写其他执行代码。
2. 以原始 rustc 源体和获准副本作成对运行，检查空、单元素、重复且顺序敏感、
   next/next_back/交错推进、耗尽、ZST、非静态元素及不可 Clone 的借用分配器。
   比较剩余元素与返回元素的销毁、分配器释放和安全的单次析构 panic 清理。
   保留移后复用、错误返回类型、活动借用及寿命逃逸的拒绝检查；不运行 UB 反例。
   原生结果只作补充，不替代源码对应及形式证明。
3. 真实绑定只有在编码有实质变化后才重编译。绑定通过后，再检查原有八个
   组合客户端，并用真实 specdet 执行 analyze 与 `replay --reexecute`。
   两阶段必须准确选择原 count/last，维持完整 usize/Option<T> 比较、
   原输入域与同一候选；不能把零义务、编译失败或缺少原始查询写成通过。
4. 有效的新结果另存新输出目录，不覆盖旧失败。任何采用须经过原体/副本、
   借用与 Drop 影响、真实绑定和两条证明轨道的独立审查，并继续应用
   `review-criteria-temporary.txt`。规范化一项成功不改变整项完成标准。

### 正式待答问题及两个选项

需要决定的是：是否允许仅在 last 的隔离源码证明副本中，将上述
`mut self` 改为按值 `self` 加 `let mut iter = self`，并在源码对应义务
经独立审查成立后，用该副本承担这一 API 的源码正确性证明？

| 选项 | 允许范围与后果 |
|---|---|
| 仅授权这一隔离证明副本的规范化 | 允许尝试上面的唯一执行差异及必要的对应验证；原候选继续保留，采用仍需独立审查，真实绑定仍须另解。不是标准库源码、工具、额外假设或可信基础变更许可。 |
| 不授权，保持原体证明边界 | 不实施该规范化，count/last 保持未完成；只在出现实质不同且原授权内的编码或新的明确决定时再处理。继续不依赖该决定的既定 API，不以同样的问题或失败反复唤醒。 |

没有默认同意、超时同意或由本次通知推定的许可。问题登记在本项目现有 Manager
待答流程中；未答复前不创建规范化源文件，不把该记录置为可执行的证明重试。
原失败任务及其审阅记录不改写为完成，也不因登记问题而重新启动。

### 局部等待期间可继续的既定 API

本次对照 `inventory/coverage.tsv`、源码和固定 vstd，选择原清单中的
`<alloc::vec::Vec<T, A> as core::ops::Index<I>>::index` 作为不依赖此决定的
后续检查对象，不是新增目标。它目前尚无项目源码证明或完整性结果。
原体在 `alloc/src/vec/mod.rs:3825-3832`：

```rust
fn index(&self, index: I) -> &Self::Output {
    Index::index(&**self, index)
}
```

它使用共享接收者和已独立确认的 Vec Deref 路径，不消费 IntoIter，也不使用
count/last 的新增绑定。官方依赖是
`vstd/std_specs/vec.rs:178-190,248-253` 的 Vec 索引及 Deref 契约，以及
`vstd/std_specs/slice.rs:310-313,330-336` 的切片索引契约；均位于固定
`toolchains/upstream/source/` 下，不需接收者规范化。

可在现有授权内继续原体、官方契约与来源关系的检查及源码证明，再检查真实
完整性入口。必须保留 `T, I: SliceIndex<[T]>, A: Allocator`、`I::Output`、
原输入域和返回借用寿命，不把 API 偷换成仅 usize 的索引；完整元素或切片
观察、关联输出类型的检查器支持仍需新增证据，不能预先宣称两轨可通过。
这项依赖判断不授权修改切片项目；只在本 Vec 工作目录内复用固定 vstd。
AsMut、Cow、with_capacity 的既有不同限制及旧失败继续保留，不安排无变化重跑。

## 当前能够确认的结果

最新 count 结果在 `proofs/correctness/into_iter/erased-count/`：固定 Verus
`--compile` 退出 0，原体有 1 个通过义务，产生本次新库，IR 的执行调用只有
继承的 len。这个源 crate 不导入目标 count/last 假设。
last 的原 `mut self` 在前端被拒绝；不含任何契约的最小复现也失败。
真实标准库绑定单独编译仍报告重复的 Iterator 实现，不能接入默认构建。

`proofs/completeness/into_iter/selected-targets/{analyze,replay}.json` 是本轮
真实 analyze 和 `replay --reexecute` 的两目标结果：两次均退出 2，
两个目标分别为编译错误、零通过义务，没有原始 SMT 查询，不能报告 unsat。
每个目标的原生 harness、契约、观察和错误输出均由结果中的路径直接定位。
count 比较完整 usize：`r1 == r2`。last 比较完整 Option<T>：
`((r1 is Some) == (r2 is Some)) && ((r1 is Some) ==> (r1->Some_0 == r2->Some_0))`。
后者同时比较变体和 Some 中的 T，不是只比较是否非空。
没有改写类型模型、忽略元素、添加搜索条件或采用新的 observer 公理。

修正 ghost 消除后，`tests/into-iter-consumers/selected-tests.stderr` 中的
5 个受影响或新增检查通过；它们包含新 count 库、原生运行、签名/契约、
两个实际检查器输入与完整观察的对应、默认入口及其余覆盖行的保持。
新链接程序的 6 个用例全部通过，见
`tests/into-iter-consumers/erasure-and-correspondence/runtime.stdout`。
该程序的 count 来自本轮 Verus 库；last **仅**来自本轮固定 rustc 编译的原体，
明确记录于相邻 `native-scope.json`，不是失败后的 Verus 证明替代品。
本轮没有 last 的 Verus 库，也没有成功的真实绑定库。

原生用例核对空、单元素、重复且顺序敏感的内容、前端/后端/交错推进和完全耗尽，
另有 ZST、非静态无额外 trait 的元素、不可 Clone 且借用局部状态的分配器。
安全 Drop 用例确认 count 销毁剩余元素，last 返回元素在显式 drop 前未被销毁，
先前移出的元素没有重复销毁。这些是 Rust 1.98.1 上的具体运行，
不证明 Rust 1.96 与宿主底层实现的普遍等价，也不把析构升格为形式保证。

8 个泛型组合客户端均保留在 `tests/into_iter_consumers_clients.rs`，
分别从官方构造、next、next_back 及混合推进关系出发；本次实际编译被绑定错误
阻断，没有客户端义务通过。十个签名及寿命拒绝探针已运行，
输入和诊断在 `tests/into-iter-consumers/engineer/{reuse,return,lifetime}-*.{input.json,stderr}`，
临时源文件已删除。count 没有伪造元素寿命逃逸要求，其结果是 usize。

两个 API 都仍不计完成；138 行覆盖中只更新这两行，其余 136 行逐字段保持。
独立双轨完成数仍为 7/138。尚未创建 `specs/into_iter/consumers.rs` 或接入
默认 `specs/lib.rs` / `specdet.toml`，因为任务要求先使真实绑定及两个原体编译通过。
with_capacity 隔离、七个已确认目标、Cow、AsMut 和所有旧失败记录保持原样。

## 源码和证明入口

权威源码位于
`/home/chentianyu/nanvix-rust-std-spec-survey/rust-1.96/library/`。
`IntoIter<T, A>` 的 `Iterator` impl 保留 `T, A: Allocator` 和 `Item = T`；
`count(self) -> usize` 的原体是 `self.len()`（301-303），
`last(mut self) -> Option<T>` 的原体是 `self.next_back()`（306-308）。
`core/src/iter/traits/iterator.rs:193-221,238-256` 描述消费迭代器的返回观察；
其中默认实现的遍历说明不要求将这两个具体覆盖方法改写成遍历。

`proofs/correctness/into_iter/{source,source_last}.rs` 在真实 `std::vec::IntoIter<T, A>` 上使用
局部同名 `Iterator` trait，避免外部 crate 对标准库类型实现标准库 trait 的
orphan 限制。它只容纳上述两个源码方法，不代替真实标准库绑定，不引入模型类型、
View、观察函数或信任假设。原 impl 泛型、关联类型、接收者和可执行表达式不变；
新增内容仅为独立证明所需的 trait 名称作用域和后置条件。原 trait 的其他方法
不复制到该局部 trait；两个原体仍调用标准库的 ExactSizeIterator::len 与
DoubleEndedIterator::next_back。原源码的 inline/stable 元数据不属于证明契约。

`proofs/correctness/into_iter/isolated/consumers.rs` 是尚未接入默认聚合的真实
标准库绑定候选。相邻 `iterator_methods.rs` 依据固定官方
`toolchains/upstream/source/rust_verify_test/tests/external_traits.rs:344-373`
的 `test_trait4`，分段外部 trait 声明仅补充缺失的 count/last 方法；
不另建 IteratorSpec，不覆盖 next、next_back、len 或其他方法契约。

## 观察和明确的依赖

两条契约无前置条件。count 返回调用开始时
`IteratorSpec::remaining(&iter).len()`；last 在该序列为空时返回 None，
否则返回 `Some(IteratorSpec::remaining(&iter).last())`，包括元素本身而非仅
Some 判别或长度。两条契约均只有一个完整返回关系，没有另列其蕴含的性质。

固定官方依赖为：

- `toolchains/upstream/source/vstd/std_specs/vec.rs:350-385` 的 IntoIter 外部类型、
  `IteratorSpecImpl` 和恒为 true 的 `obeys_prophetic_iter_laws`。
- `toolchains/upstream/source/vstd/std_specs/iter.rs:288-300` 的 ExactSizeIteratorSpec
  与 len 的当前剩余长度关系，以及 `:245-279` 的 next_back 末项返回和状态转移。
- 组合客户端另用 `std_specs/vec.rs:393-401` 的 Vec::into_iter 构造关系和
  `std_specs/iter.rs:35-54` 的 next 首项返回和状态转移。
- vstd 的 Seq 长度、索引、last、drop_first/drop_last 与 Option 逻辑相等。

`into_iter_elts(iter) == remaining(&iter)` 只作为构造时的既有关系读取，不提升为
消费后不变量。上述依赖和继承的 len 不增加 API 计数。
对应 Rust 委托源码是 `into_iter.rs:273-280,424-446,473-481`，
`core/src/iter/traits/exact_size.rs:1-123`，构造为 `alloc/src/vec/mod.rs:3894-3931`。

所有形式结果只描述正常返回；不增加 no_unwind，不将 final 状态解释为 Drop
已被证明。`into_iter.rs:541-559` 销毁剩余元素，last 移出的返回值不再属于剩余区；
安全原生 Drop 用例将作为补充，不扩展形式证明范围。

项目内 `review-criteria-temporary.txt` 继续适用，执行能力及客户端证明均不能
代替独立确认或两条源码正确性证明。

## 首次源码入口的诊断

`proofs/correctness/into_iter/isolated-build/` 保留首次编译退出 1、候选源码与
E0034 诊断。命名返回值的 Verus 宏在 impl 中生成
`constrain_type(result, self.count())` / `self.last()`，与真实标准库方法歧义，
未进入证明义务；展开输出见 `proofs/correctness/into_iter/expansion/source.stdout`，
生成位置为固定 `builtin_macros/src/syntax.rs:1097-1127`。

随后 `explicit-postcondition/` 保留直接调用 ensures 内置函数的未通过版本；
该写法没有进入 Verus 表达式转换，编译器将其中的相等按 Rust PartialEq 解析。
没有采纳错误诊断所建议的 PartialEq 约束。

`explicit-imports/` 保留关闭隐式 prelude 的失败；这也禁用了 Verus 宏所需的
工具属性名称解析，不能作为当前入口。已恢复普通 prelude。

当前候选使用显式返回类型的 ensures 内置注解，并仅以官方
`verus_proof_expr!` 转换其中的逻辑表达式。这样无需宏生成歧义的返回类型推断
调用，原签名与尾表达式均保留；不更改宏、类型或执行路径，也不用目标假设证明自身。

该版本的实际编译在 `ghost-postconditions/count.stderr` 报告
`The verifier does not yet support the following Rust feature: mut self`，
尚未产生源码义务。固定
`toolchains/upstream/source/rust_verify/src/rust_to_vir_func.rs:416-424`
在 `ImplicitSelfKind::Mut` 分支直接拒绝该接收者，错误与后置条件真假无关。
完整候选、命令、退出码和此前三个失败版本都已保留。

两个逐 API 入口现分别导入 `source.rs` 的 count 和 `source_last.rs` 的 last，
避免 last 的前端错误遮蔽 count 的验证。两份都保留原 impl 泛型及 Item=T。
`diagnostics/mut_self.rs` 进一步移除全部候选契约，仅保留真实类型及原 last
签名、原体，以判别是否是规格编码引起的错误。未将 `mut self` 改成共享或可变
借用，未将原体改成另一段程序，也未修改固定工具。

count 单独入口最初的验证过滤器还同时匹配 trait 声明和实现，见
`separate-count/count.stderr`；现使用唯一的 `IntoIter::count`。
随后 `count-source/count.stderr` 报告 duplicate specification。最初将源码
impl 与标准库绑定分开，但 `current-bindings/bindings.stderr` 证明单独绑定
也有同一错误，不能将其归因于局部源码 trait。当前 `isolated/lib.rs` 只编译
真实绑定；两个源码 crate 不导入 count/last 候选假设。

`current-count/count.stdout` 实际为 `1 verified, 0 errors`，本次新库为
`current-count/build/libinto_iter_count.rlib`。其 `count/crate.vir:1082-1200`
保留任意 T、A:Allocator、按值 self、唯一当前 remaining 长度后置条件及原体；
可执行调用仅为继承的 `ExactSizeIterator::len`，没有目标 count 调用或
external_body、额外前提和析构保证。它是源码正确性结果，不是真实绑定成功。

`current-bindings/bindings/crate.impl_names` 同时列出已有的
`alloc::vec::into_iter::impl&%6` Iterator 实现和来自具体假设的同一路径；
固定 `vir/src/traits.rs:1368-1384` 拒绝重复记录。单独 count 的真实绑定以及
移除后置条件的诊断版本均在 `binding-reproduction/` 退出 1，
因此不能靠删去当前 remaining 观察来修复。这两个诊断不代替候选契约，
也不证明一切可能的编码均不可行。未修改官方 IteratorSpec 或导入的实现。

## 真实完整性分析的目标选择

首次真实 analyze 和 replay --reexecute 在
`proofs/completeness/into_iter/engineer/` 均实际退出 2。除两个具体标准库绑定，
发现器还选中了同文件的两个辅助 trait 方法，共四项；这不满足本任务的目标对应，
不能使用那次结果作为两目标结果。

现将原样的两条辅助方法声明移至 `isolated/iterator_methods.rs`，由同一个
`isolated/lib.rs` 导入，目标文件仍只含两个完整的具体绑定。观察、泛型和合法域
未变，辅助声明及官方依赖不计 API。所有旧失败保留；默认 specs/lib.rs 和
specdet.toml 没有接入未经证明的候选。

## 首次运行暴露的 ghost 注解消除问题

`tests/into-iter-consumers/suite.stderr` 保存首次完整 unittest：9 个测试中
4 个通过，5 个测试未通过，其中完整性测试的两个阶段分别报告失败，总计
6 项失败断言。真实绑定、组合客户端、last 源体和两次完整性检查都明确失败，
没有改成 skip 或 expectedFailure。十个移后复用、错误返回类型、last 元素寿命
逃逸探针按预期拒绝，临时 .rs 已删除。

当次新编译的原生程序在四个涉及源码 count 的用例中触发 builtin::ensures
的 not implemented。`--compile` 仍保留 `verus_keep_ghost`，所以该条件不能
用来消除手写 ghost 语句；这不是 count 标准库实现的问题。固定
`builtin_macros/src/lib.rs:136-158` 明确区分元数据保留和
`verus_keep_ghost_body`。当前两个源码注解均改用后者，只改变 ghost 消除条件，
不改变后置条件、原签名或两个可执行表达式；此前失败和旧库仍保留。
新 count 库及受影响的运行随后重新检查，未变的标准库绑定失败不重复执行。

上述修正后的实际编译和运行已经完成，结果见本记录开头。
旧 `current-count/` 库不是当前原生通过的依据；最新库只取自 `erased-count/`。
last 的 ghost 条件同样修正，但原 `mut self` 未改；未重复执行不受该消除条件
影响的前端拒绝诊断。其独立最小复现没有 ghost 注解，仍可作为这个限制的依据。
完整 discover 命令的首次失败保留，不声称完整套件后来全部通过；没有重跑未变的
绑定、组合客户端或失败的完整性分析来制造额外记录。

## 私有输出和独立确认

`proofs/correctness/into_iter/build.py DIRECTORY count`、`... last` 和
`... bindings` 各创建新输出目录，保存实际命令、退出码、源输入、日志及新库。
bindings 的零义务仅能表示类型检查，不是 API 正确性。当前 last 和 bindings
命令仍应失败；测试中的成功要求没有放宽。

`proofs/completeness/into_iter/check.py DIRECTORY` 使用原生检查器。
相对于默认配置，最终只有五项设置不同：`project.root` 选择尚未集成的同一
隔离输入目录，`targets.include` 仅选择 consumers.rs，verifier 路径规范化，
TMPDIR 和输出目录转到私有目录。其余解码后的配置在对应测试中逐项相等。
这不是默认聚合的重放，也不是把输入根目录改变冒称为单纯输出重定向。
分析和重新执行的三份源文件快照均与当前隔离输入逐字节一致，泛型、按值参数、
完整返回类型、无前置条件和唯一后置条件一致。两次原生比较的通过义务均为零。
搜索 schema 有保存，但没有 SMT 查询，因此不声称已经执行关闭全部搜索条件的查询。

以下是上一轮提供的完整复跑方式，保留用于有实质变化后的验证，不是本次重跑
未变失败的指令。独立审查使用正常的 `run_review_command` /
`get_review_command`，亲读权威源码、当前候选及临时冗余准则，输出放私有 scratch：

```sh
bash scripts/with_baseline.sh env TMPDIR={scratch}/tmp \
  INTO_ITER_OUTPUT_DIR={scratch}/into-iter-consumers \
  python3 -B -m unittest discover -s tests -p test_into_iter_consumers.py -v
```

未设置复用记录变量时，该命令实际新编译两个逐 API 入口、真实绑定和原生程序，
执行组合客户端与拒绝探针，再实际运行 analyze 和 replay --reexecute；
全部输出在指定私有目录。它应如实暴露尚未解决的编译及完整性失败。
工程侧受影响检查的原命令保存在
`tests/into-iter-consumers/selected-tests.command.json`，首次完整命令在
`.argus_subagents/vec-into-iter-tests-12969919776e.json` 中。
固定工具、合法输入域及可信基础均保持不变，不重审未变的隔离工作。
两个具体工具限制已由上述既有独立审阅确认，不是 Rust 实现或文档缺陷；
本次新增的隔离副本提案尚未授权、执行或经过独立审查。

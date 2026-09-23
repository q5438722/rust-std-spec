# 将原借用转换函数体放入独立证明入口

本记录在创建证明副本之前提出，供独立 Reviewer 检查源码对应关系。它是
`source-proof-translation`，源码对应及冗余删减现已获独立确认，不是标准库缺陷。

## 已提交的独立结论

依据
`/home/chentianyu/.argus-vec-specgen-astra-20260922/projects/s-6a17c286/handoffs/fc975bfe5a6c/round-0001.json`
中的正式审查，四个借用入口的源码对应、完整泛型、生命周期展开和正确性均成立；
三条冗余 View 条款的删除成立。两个 AsRef 的当前内容观察已完成独立分析及重新执行。
两个 AsMut 只确认了源码对应和正确性，完整性仍因检查器的可变返回限制未完成。
这项结论相对于该轮固定候选、官方依赖和基线，不适用于后续改变的契约。
以下工程记录及其中当时尚待审查的说明原样保留，本轮不重新审查未变的借用契约。

Rust 1.96 的只读输入
`/home/chentianyu/nanvix-rust-std-spec-survey/rust-1.96/library/alloc/src/vec/mod.rs`
在 4274–4300 行给出四个不同的 trait 实现。每个函数体只有 `self`。
`AsRef<Vec<T,A>>` 和 `AsMut<Vec<T,A>>` 返回原接收者；
两个 slice 返回由 Rust 的 `Deref`/`DerefMut` 强制转换产生，相关实现位于
3749–3765 行。trait 文档在同一 Rust 树的
`library/core/src/convert/mod.rs:113-151,217-247,369-375`。

独立 crate 不能重新实现标准 trait 与标准类型的既有组合。因此，拟采用
以下命名空间嵌入，保持所有可执行表达式、类型和合法输入不变：

下面保留提出此嵌入时的原始契约；本轮只对它的冗余后置条件作等价删减，
具体证明和当前形式见文末。

```rust
// 原实现中的方法：
fn as_ref(&self) -> &Vec<T, A> { self }
// 独立证明入口；唯一表达式仅作绑定变量改名：
pub fn as_ref_vec<'a, T, A: Allocator>(vec: &'a Vec<T, A>)
    -> (result: &'a Vec<T, A>)
    ensures result == vec, result@ == vec@,
{ vec }
```

其余三个入口只分别改变原方法对应的返回类型和可变性：
`as_ref_slice` 返回 `&'a [T]`，`as_mut_vec` 返回
`&'a mut Vec<T,A>`，`as_mut_slice` 返回 `&'a mut [T]`。
显式 `'a` 是原单一接收者生命周期省略规则的展开，不添加生命周期边界。
`T` 和 `A: Allocator` 全部保留，不增加 `Copy`、`Clone` 或 `'static`。
slice 入口仍使用原来的隐式强制转换，不改成调用其他方法。

这不是新增可信函数。四个证明 crate 不导入本实验的
`assume_specification`；只允许官方未修改 vstd 的既有 View、
`Deref` 和 `DerefMut` 依赖。不会用目标 API 的假设证明自己。
若该原样表达式不受 Verus 支持，将保留失败并另行提出修改，而非静默改写。

验证将核对源 trait 参数、签名、生命周期展开和函数体的 token 对应；
核对规范、正确性入口及实际完整性输入中的同一契约；随后编译并执行
源体函数和真实 trait 调用的类型、完整内容、顺序及可变写回测试。
正确性文件为 `proofs/correctness/vec/as_{ref,mut}_{vec,slice}.rs`，
完整性文件为 `proofs/completeness/vec/as_{ref,mut}_{vec,slice}.rs`。

固定工具为官方 `release/0.2026.09.20.aef82ed`、其发布的 vstd 和 Rust 1.98.1。
Rust 1.96 是被解释的语义源码版本，不冒充工具宿主版本。

## 删减之前的工程结果

实际采用的四个副本与这里提出的形式相同，没有改写隐式强制转换。
`tests/test_borrowed_bindings.py` 的源码对应测试逐一检查四个原 impl 的唯一性、
完整泛型签名、接收者生命周期展开、原 `self` 与新绑定 `vec` 的 token 对应，
并检查规格和正确性入口中的后置条件逐项相同，没有新增前置条件。
本轮该测试通过，输出为 `tests/closure-engineer/test_borrowed_bindings.log`。

`proofs/correctness/vec/closure-engineer/` 下的 `as_ref_vec.stdout.log`、
`as_ref_slice.stdout.log`、`as_mut_vec.stdout.log`、`as_mut_slice.stdout.log` 均记录
`verification results:: 1 verified, 0 errors`，并产生了相应 `.rlib`。
例如 `proofs/correctness/vec/closure-engineer/as_ref_slice/crate.vir:3458-3490`
保留了非 external 的实际函数体，并显示隐式转换解析到
`alloc::vec::impl&%9::deref`，经 `core::ops::deref::Deref::deref` 调用；
没有调用或假设目标 `AsRef::as_ref`。
这与 Rust 1.96 原 `self` 的接收者类型及强制转换方向一致。

两个只读目标的实际 specdet 原始结果和重新执行均为
`deterministic`、`baseline.status = unsat`，各验证一个完整性义务。
详见 `proofs/completeness/vec/review-runs/engineer-analyze.json`、
`proofs/completeness/vec/review-replay-runs/engineer-replay.json` 及
`inventory/coverage.tsv` 中逐目标的生成代码、原生查询和命令。
两个可变目标的正确性义务同样通过，但检查器尚不支持返回可变引用；
限制另见 [specdet-mutable-return](specdet-mutable-return.md)，不能把这两个 API
记为双轨通过。

这些是已执行的机械检查结果，不是独立审查结论。
本记录仍为 `needs-review`，对应关系须由后续独立审查确认。
四个声明及四个源体均保持原样；仅测试输出可另选目录，以免覆盖既有记录。
本轮工程检查不能代替 Reviewer 通过正式审查操作提交的判断。
没有改动 canonical Rust、vstd、Verus 或 checker 的授权，也没有进行这些改动。

## 当前源码对应和等价删减

本轮重新对照的权威源码仍是
`/home/chentianyu/nanvix-rust-std-spec-survey/rust-1.96/library/alloc/src/vec/mod.rs`。
四个实现分别为：

| 实现与位置 | 原函数体及返回方式 | 当前证明入口 |
|---|---|---|
| `AsRef<Vec<T,A>>`，4275-4279 | `fn as_ref(&self) -> &Vec<T,A> { self }`，返回共享接收者 | `proofs/correctness/vec/as_ref_vec.rs` |
| `AsMut<Vec<T,A>>`，4282-4286 | `fn as_mut(&mut self) -> &mut Vec<T,A> { self }`，可变重借用 | `proofs/correctness/vec/as_mut_vec.rs` |
| `AsRef<[T]>`，4289-4293 | `fn as_ref(&self) -> &[T] { self }`，隐式 `Deref` | `proofs/correctness/vec/as_ref_slice.rs` |
| `AsMut<[T]>`，4296-4300 | `fn as_mut(&mut self) -> &mut [T] { self }`，隐式 `DerefMut` | `proofs/correctness/vec/as_mut_slice.rs` |

共同的 `impl<T, A: Allocator>`、隐含的 `T: Sized`、接收者生命周期及 `{ self }`
均不变。`Deref`/`DerefMut` 在同文件 3749-3765 行调用
`as_slice`/`as_mut_slice`；1808-1878 行的文档和实现说明它们以 Vec 指针和
长度返回整个有效内容区，而不是已分配但未初始化的容量区。
trait 文档和方法签名位于
`/home/chentianyu/nanvix-rust-std-spec-survey/rust-1.96/library/core/src/convert/mod.rs:109-138,217-245,305-308,369-376`。
它们要求转换不可失败；Vec 实现没有新增值域限制。
`Borrow` 的等价性要求没有被搬到 `AsRef`，合法引用的内部不变式也没有变成新前置条件。

既有官方桥接位于
`toolchains/upstream/source/vstd/std_specs/vec.rs:236-261`。
本轮生成的 `proofs/correctness/vec/redundancy-engineer/as_ref_slice/crate.vir:3458-3483`
和 `as_mut_slice/crate.vir:3544-3564` 显示实际非 external 源体分别解析到
`Deref::deref` 和 `DerefMut::deref_mut`，没有调用目标 AsRef/AsMut 假设。
这仍是相对于官方桥接契约的组合证明，不是本轮重新证明 RawVec 内存实现。
Rust 1.96 源码与 Rust 1.98.1 宿主之间的这个有限对应仍需独立判断，
不能据此宣布两个版本普遍等价。

遵照项目内 `review-criteria-temporary.txt`，只删除以下三条：

| 保留条件 | 可由它推出的已删除条件 |
|---|---|
| `result == vec` | `result@ == vec@` |
| `*result == *old(vec)` | `result@ == old(vec)@` |
| `*final(result) == *final(vec)` | `final(result)@ == final(vec)@` |

依据是固定官方 `view.rs:10-29,103-108` 的 spec 函数同余和共享引用的
View 透明性；可变引用的状态解释来自原 Verus 借用语义，
没有虚构一个 `View for &mut A`。这里的等号是逻辑值等式，
不是 Rust `PartialEq` 或指针身份。初态等式不能替代终态等式，
更不能推出 `final(vec)@ == old(vec)@`。
两个 slice 契约没有同类型值等式可替代其跨类型内容关系，故保持原样。

`tests/borrowed_clients.rs:11-19` 的两个泛型证明没有目标 API 假设调用或前置条件，
分别验证共享引用和值的同余；21-39 行的两个客户端只使用删减后的声明，
却仍要求原来的完整后置条件。41-55 行的既有客户端允许 push 和元素替换。
该文件本轮实际得到 `6 verified, 0 errors`，日志为
`proofs/correctness/vec/redundancy-engineer/contract-equivalence.log`。
原契约推出新契约仅是合取消去；这六个义务检验了需要证明的反向蕴含和合法写回。
它们不是源体证明的替代品。

四个当前源体另行各验证一个义务并编译；
两个 AsRef 的当前分析和重新执行各得到一个完整性义务及 `unsat` 原始查询。
精确结果见 [当前覆盖记录](../inventory/COVERAGE.md)。
两个 AsMut 仍只有正确性结果，完整性在生成前受阻。
旧 Vec 证明入口保存在 `proofs/correctness/vec/before-redundancy/`，
未删减规范仍在原始
`proofs/completeness/vec/runs/20260922T060638Z-a38ccd282e/workspace/vec/borrowed.rs`。
此记录仍等待正常独立 Reviewer 的正式判断；环境恢复记录和工程证明均不替代它。

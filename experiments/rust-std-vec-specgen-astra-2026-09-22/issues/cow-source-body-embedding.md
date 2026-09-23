# Cow 四个直接转换的源码对应

本记录在建立证明入口之前提出。四个入口只为避免标准 trait 的重复实现而改变函数名，
不改写任何可执行表达式。任务 `4566f129a548` 的独立审阅已确认这四个入口的
有限源码对应、透明观察、源码正确性及冗余检查；完整性仍未完成。
当前属于 `source-proof-translation`，不是标准库缺陷，也未向外部提交问题。

权威输入为
`/home/chentianyu/nanvix-rust-std-spec-survey/rust-1.96/library/alloc/src/vec/cow.rs`。

| 原签名与源码 | docstring | 独立入口及原表达式 |
|---|---|---|
| `impl<'a,T:Clone> From<&'a [T]>`，12-14 | 6-11 | `from_slice`：`Cow::Borrowed(s)` |
| `impl<'a,T:Clone,const N:usize> From<&'a [T;N]>`，25-27 | 19-24 | `from_array`：`Cow::Borrowed(s as &[_])` |
| `impl<'a,T:Clone> From<Vec<T>>`，38-40 | 32-37 | `from_vec`：`Cow::Owned(v)` |
| `impl<'a,T:Clone> From<&'a Vec<T>>`，51-53 | 45-50 | `from_vec_ref`：`Cow::Borrowed(v.as_slice())` |

所有结果均为 `Cow<'a,[T]>`。保留原生命周期、`T: Clone`、数组 const 参数、
默认分配器和父模块 `not(no_global_oom_handling)` 条件。不增加元素的 View、Copy、
Eq 或静态生命周期要求，也不将移动路径改写为克隆或重新分配。
`core/src/convert/mod.rs:458-593` 要求 From 不失败并消费传入的值；
这四段文档还明确要求正确变体以及不分配、不克隆。

`alloc/src/borrow.rs:86-180` 给出 Cow 的文档和枚举表示。
固定官方 `toolchains/upstream/source/vstd/std_specs/borrow.rs:20-24`
已公开这两个变体，但 80-89 行的 slice Cow View 需要 `T: View + Clone`，
且只返回 Seq，不能作为本任务的完整观察。
当前 `specs/cow/observation.rs` 对原枚举直接匹配，返回
`CowContents::Borrowed(Seq<T>)` 或 `CowContents::Owned(Seq<T>)`；
不引入不解释函数、假设或新可信依赖。

原拟借助检查器支持的源码 spec `view` 方法确定观察；当前实际输入在构造观察之前
被生命周期类型解析拒绝，详见 [检查器限制](specdet-cow-lifetime-type.md)。
`CowObservation<T>` 是本项目的 spec 扩展 trait，不是另一个官方 View 实现；
其实现覆盖每个 `Cow<'a,[T]> where T: Clone`。
最初候选为向检查器显式提供观察能力，曾在绑定中写入
`where Cow<'a,[T]>: CowObservation<T>`。即使该条件由 blanket impl 满足，
固定 Verus 仍要求 assume_specification 的 trait bounds 与原签名逐项相同；
聚合构建实际报告 `assume_specification trait bound mismatch`。
原候选及诊断保存在 `proofs/correctness/cow/cow-engineer/candidate/` 和
`aggregate.stderr`。当前已删除四个附加 where 子句；真实绑定及源体均只保留原 `T: Clone`。
四个原表达式本身各验证一个义务并编译，不受该绑定修正影响。

最初的 native discovery 还因聚合模块的外层
`#[cfg(not(no_global_oom_handling))]` 被判为不可达，见
`proofs/completeness/cow/cow-engineer/discover.json`。
固定检查器 `adapters/verus/discovery.py:38-65,97-143` 无法求值这个 bare cfg，
并将未知外层条件视为未启用。当前只将聚合中的相同条件移到 Cow 模块内部；
两个子文件和四个证明入口的 crate 内层条件均保留。Rust 下启用和停用条件不变，
没有将不存在的 API 纳入目标，也没有改动原始函数表达式。
本次检查限定于固定基线中未设置 `no_global_oom_handling` 的配置，
不宣称检查器能分析该条件的所有配置。

数组的原始 cast 依赖固定官方 `vstd/array.rs:10-20,90-96,112-126` 的
数组序列及 unsizing 桥接；Vec 引用依赖 `vstd/std_specs/vec.rs:236-240`。
`std_specs/convert.rs:8-21` 的 From 框架保留不动；
四个真实 UFCS 绑定不能与框架冲突，也不能导入源体证明来证明自己。
正确性入口只导入透明观察和固定官方 vstd，不导入目标 `assume_specification`。

上一工程轮保存的中间表示确认了这两处调用：
`proofs/correctness/cow/cow-engineer/from_array/crate.vir:5358-5388`
在非 external 的 Borrowed 构造中调用 `vstd::array::array_as_slice`；
`proofs/correctness/cow/cow-engineer/from_vec_ref/crate.vir:4312-4348`
调用 `alloc::vec::impl&%1::as_slice`，分配器参数为 Global。
这两个可执行函数体没有调用目标 From；观察函数只出现在后置条件中。

本任务沿用官方 Verus `release/0.2026.09.20.aef82ed`、未修改的配套 vstd 和
项目私有 Rust 1.98.1。被解释的语义源码仍是 Rust 1.96；
证明是相对于官方数组、切片和 Vec 桥接的组合证明，不重新证明底层内存实现。
不修改 canonical Rust、Verus/vstd、checker、Argus 或其他实验。

新契约各用一个枚举观察等式，同时给出变体和完整有序内容，不再重复长度或逐元素等式。
独立审阅已按 `review-criteria-temporary.txt` 检查四条契约：均无前置条件，
各自唯一的观察等式是必要条件，没有发现应删的逻辑冗余。
审阅者还在私有 scratch 中使用固定 Verus `--compile` 重建聚合与四个源体，
四个源体各验证一个义务；聚合的零义务仅算编译。
这一结论相对于上述官方依赖成立，不是重新证明底层内存实现。

独立执行的 23 项定向测试中，22 项通过，原生程序链接因只读容器缺少 cc 而失败；
审阅者另核对了工程侧当轮新编译程序及六项行为测试的成功记录，没有用旧二进制替代。
独立 analyze 和 replay --reexecute 均在观察构造前遇到生命周期解析失败，
故这些已确认结论不等于四个 API 的双轨完成。
后续只对实质变化重新检查，未变源体、借用契约及收集器不重新生成或审查。
项目临时冗余准则继续适用于后续独立审阅。

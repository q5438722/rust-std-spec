# 两个所有权转换的源码对应

任务 `db4ff3669ca5` 的独立审阅已确认两个入口的源码对应、正确性、完整性及重放。
本轮已亲读其 `round-0001.json`，只落实已提交的结论，不重审或重跑未变代码。
没有改写 Rust 源码、可执行表达式、固定 Verus/vstd 或检查器；没有公开提交问题。
审阅已应用
[本项目临时规格冗余准则](../review-criteria-temporary.txt)。

独立审阅在只读环境中新编译两个源体及聚合，两个源体各通过一个义务；
真实分析和重新执行各为两个目标生成非零通过义务，原始查询均不可满足。
九项测试中八项通过，原生链接因容器缺少 `cc` 未完成；审阅者另核对工程侧
当轮新构建及七项原生运行记录，没有把旧二进制冒充独立重跑。
正式依据为
`/home/chentianyu/.argus-vec-specgen-astra-20260922/projects/s-6a17c286/handoffs/db4ff3669ca5/round-0001.json`。
下文保留工程轮的尝试和失败，原先要求独立确认的事项现已由上述有限结论解决。

## 原源码与证明入口

本轮亲读的权威源码位于
`/home/chentianyu/nanvix-rust-std-spec-survey/rust-1.96/library`。

| 原实现及文档 | 独立证明入口 | 保留的原表达式 |
|---|---|---|
| `alloc/src/vec/mod.rs:4362-4375` | `proofs/correctness/vec/from_array.rs` | `<[T]>::into_vec(Box::new(s))` |
| `alloc/src/vec/mod.rs:4401-4416` | `proofs/correctness/vec/from_boxed_slice.rs` | `s.into_vec()` |

证明入口仅把 trait 方法移入独立 crate 并改名，为返回值增加 ghost 名称和后置条件；
第二个入口把原 `Self` 明确写为该 impl 的 `Vec<T,A>`。
数组仍为任意 `T` 和 `const N: usize`，装箱切片仍为任意 `T` 和 `A: Allocator`。
没有前置条件或新增 Clone、Copy、View、Eq、静态生命周期约束。
两个入口均不导入目标 From 的假设。数组保留
`not(no_global_oom_handling)`；装箱切片没有该条件。

`core/src/convert/mod.rs:458-592` 的 From 文档要求消耗输入、保持值的意义及内容。
数组方法明确移动元素而非克隆；装箱切片方法明确转移既有堆分配。
委托方法 `alloc/src/slice.rs:463-486` 还说明不克隆、不分配，其原体以
`Box::into_raw_with_allocator` 取得原指针及分配器，再以相同长度和分配器构造 Vec。

## 官方依赖和观察范围

`toolchains/upstream/source/vstd/std_specs/smart_ptrs.rs:12-21`
分别提供分配器泛型 `into_vec` 的内容等式和 `Box::new` 的 pointee 值等式。
`array.rs:11-21,90-126` 定义完整数组序列及数组到切片的内容桥接；
`slice.rs:13-17` 和 `view.rs:22-29,104-108` 提供 slice、引用及 Vec 的既有观察。
`inventory/vstd-tests/binding_probes.rs:49-53` 和 `binding_results.json`
只说明这些依赖已有客户端，不被计为本轮目标证明。

本轮实际 Verus 中间表示显示，数组原表达式调用官方 `Box::new`、
`vstd::array::array_as_slice` 和 `into_vec`；装箱切片直接调用 `into_vec`，
保留 `A` 并以 Move 读入 `s`。对应记录为
`proofs/correctness/vec/owned-conversions/from_array/crate.vir:4583-4618`
和 `from_boxed_slice/crate.vir:3433-3452`。
这项组合证明依赖固定官方边界，不重新证明分配器或裸指针的底层实现。

两个契约各只写 `result@ == s@`，覆盖全部元素、长度和顺序。
长度及逐元素等式已经被该序列等式蕴含，不另加冗余条款。
它不表述分配地址、容量或分配器身份；这些性质必须另看原源码、
官方委托边界和针对性原生测试，不能由序列确定性推出。
数组输入不存在必须复用的原堆分配，不能向它强加装箱切片的地址关系。

## 条件属性在首次完整性分析中遗漏数组

`proofs/completeness/vec/owned-conversions/engineer/analyze.json` 和
`replay.json` 保存首次真实执行。检查器两次都只发现装箱切片，虽返回退出码 0，
运行脚本仍因目标集合不等于两项而报错；没有把它写成两个目标完成。
原候选保存在 `proofs/correctness/vec/owned-conversions/owned_conversions.source.rs`
及检查器自己的源码快照中，失败记录保留。

固定检查器的
`/home/chentianyu/spec-determinism-tool/src/specdet/adapters/verus/discovery.py:38-64,168-187`
只解析 feature、test 和 Verus ghost 条件，不识别 `no_global_oom_handling`，
因此跳过带有该外部属性的声明。这不是数组语义或 Verus 源体证明失败。

当前规格把同一条件移到仅含数组声明的内联 `array` 模块内：
`pub mod array { #![cfg(not(no_global_oom_handling))] ... }`。
模块和声明的有效条件相同，装箱切片仍无此条件；契约、泛型、输入及输出没有变化。
这是声明的命名空间和属性作用域调整，不是可执行实现改写，也没有替换检查器输入模型。
真实 Verus 仍按原条件编译包含该声明和生成证明的模块。
独立审阅须确认该有限对应及当前构建条件，不能把扫描器未解析任意 cfg
解释为所有构建配置均已验证。

该调整的首次布局把 `verus!` 放在 Rust 内联模块内部。真实运行
`proofs/completeness/vec/owned-conversions/module-cfg/` 仍只发现装箱切片：
数组处的具体诊断变成 `Item macro expansion is not included in source discovery`。
`discovery.py:293-295` 对普通宏调用直接停止遍历；这次不是同一个 cfg 诊断。
该布局、聚合构建及失败输出均保留，不能由只发现一个目标的退出码 0 推出任务成功。
`tests/owned-conversions/suite.stderr` 也如实记录完整性测试失败；
另外七项测试通过，包括七个原生用例、八个预期拒绝探针，以及默认配置六个、
禁用全局 OOM 处理配置三个客户端义务。

当前把数组内联模块和装箱切片声明一起放入根级 `verus!`，不再嵌套普通宏调用。
数组模块仍使用同一个内层条件，两个声明仍是同一真实 UFCS 绑定和序列等式。
这一改动针对已读到的宏遍历边界；后续结果须由真实编译、发现和重放确认，
而不能由本段解释推定通过。

## 工程执行记录与现已确认的范围

当前布局的聚合实际编译成功，日志为
`proofs/correctness/vec/owned-conversions/aggregate-verus-module.log`。
两个原体未变化，各自本轮已完成的一个义务及编译结果仍在同目录
`from_array.log` 和 `from_boxed_slice.log`。
`tests/owned-conversions/verus-module/` 的六个默认配置客户端义务及
三个禁用全局 OOM 处理配置义务均通过；两份中间表示分别保留和移除数组绑定，
装箱切片在两者中均保留。

真实检查器随后在
`proofs/completeness/vec/owned-conversions/verus-module/analyze.json` 和
`replay.json` 中都恰好发现这两个真实绑定。两次 CLI 均退出成功，
每个目标每次均有一个通过义务，原始查询均不可满足。
完整比较是 `(r1)@ =~= (r2)@`；原泛型、空前置条件及唯一内容等式保持不变。
所有搜索开关在原始查询中关闭，没有更换模型或比较策略。

本地完整性测试最初误用了发现覆盖度和空搜索记录的数据格式。
核对实际结果及固定工具的数据定义后，仅修正本地测试断言，没有重跑未变检查器。
先前错误日志保留；最后对四个原生证明记录的检查通过，
见 `tests/owned-conversions/suite-native-results.stderr`。
私有配置的结构比较另确认只改变源码根、工具路径、临时目录和输出目录。

七个原生用例均运行本轮新编译的源体库，并与真实标准库绑定对照。
非静态、不可克隆的自定义分配器保留其唯一资源；非空非 ZST 的装箱切片保留
原存储，在转移期间未分配或释放，最终由相同分配器释放一次。
八个移后复用及借用逃逸探针按原签名被拒绝，临时源文件已清理。
这些结果记录在 `tests/owned-conversions/engineer/`，不取代两轨证明。

独立审阅已亲读上述原源码、官方委托和原条件，确认当前命名空间嵌入、
非零源体义务、完整内容观察及无应删冗余，并区分原生分配补充证据的范围。
两个所有权转换现计入独立双轨确认；没有关闭 Cow 或 AsMut，也没有删除旧失败。

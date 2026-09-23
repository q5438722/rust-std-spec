# 三个已有官方规格的源码入口

本轮只复用固定官方契约，不新增 `assume_specification`，不改动 Rust、
Verus/vstd 或检查器。有限源码对应、规格复用、const 边界、冗余检查及双轨结果
已由任务 `af05f6b80c5a` 独立确认，依据为
`/home/chentianyu/.argus-vec-specgen-astra-20260922/projects/s-6a17c286/handoffs/af05f6b80c5a/round-0001.json`。
本次仅同步已提交结论，不重审未变代码；后续审阅仍适用
[本项目临时冗余准则](../review-criteria-temporary.txt)。

独立审阅新编译了三个逐 API 入口和聚合，并实际执行分析及重新执行。
其原生测试因容器缺少 `cc` 未能链接，不能记作独立原生运行通过；
审阅者另核对了工程侧当轮新构建及七项原生运行记录、当前输入对应和生成时间。
以下保留原工程轮的依据、失败与修正记录。

## 已亲读的语义与官方边界

权威 Rust 1.96 源码根为
`/home/chentianyu/nanvix-rust-std-spec-survey/rust-1.96/library`。

| 原实现和文档 | 官方契约 | 保留的原表达式 |
|---|---|---|
| `alloc/src/vec/mod.rs:4256-4264`；`core/src/default.rs:7-140` | `toolchains/upstream/source/vstd/std_specs/vec.rs:105-108` | `Vec::new()` |
| `alloc/src/vec/mod.rs:3033-3049` | 同文件 `214-219` | `self.len() == 0` |
| `alloc/src/vec/mod.rs:3749-3756`；`core/src/ops/deref.rs:3-151` | 同文件 `248-253` | `self.as_slice()` |

`Default` 对 Vec 不要求元素实现 Default，返回空向量且尚不分配。
这不是零容量的普遍结论，ZST 必须单独处理。`is_empty` 只判断长度，
预留容量不影响真值。Deref 的关联类型是 `[T]`，返回与共享接收者关联的
整个有效前缀，不暴露容量中的未初始化元素。

官方 trait 规格 `std_specs/default.rs:5-11` 只要求 `Self: Sized`，
没有附加方法条件；`std_specs/core.rs:29-36` 保留 `Target: ?Sized`
以及 `&self -> &Self::Target`，也没有附加方法条件。
本轮 Vec 具体实例不增加任何元素 trait 或静态生命周期界限。

依赖分别是官方 `Vec::new` 的空序列契约（`std_specs/vec.rs:100-103`）、
`Vec::len` 和既有长度公理（同文件 `80-97`）、`Vec::as_slice`
的完整序列契约（同文件 `236-240`）。
已读 Rust 委托实现及文档分别为 `alloc/src/vec/mod.rs:448-466`、
`3009-3031`、`1808-1841`。这些依赖及底层分配、裸指针实现不计为本轮证明的 API。

## 唯一输入与有限命名变化

`specs/vec/reused_basic.rs` 同时包含三个真实原表达式和其官方契约。
三个 `proofs/correctness/vec/{default,is_empty,deref}.rs` 仅用 `#[path]`
导入这份文件并重新导出相应函数；逐 API 命令选择其中一个函数验证，
聚合另行编译验证全部三个。specdet 直接分析这一源文件，而不是客户端或模型。

Default 保留任意 `T`、无参数及 `Vec<T>` 返回类型；其他两项保留
`T, A: Allocator`，把共享接收者分别命名为官方契约中的 `v`、`vec`。
省略生命周期仍展开为同一个接收者生命周期。唯一后置条件及 ghost 返回名称
逐字沿用官方声明；没有前置条件、忽略字段、自定义观察或额外假设。
真实标准库调用仍通过未改动的官方绑定。

`is_empty` 的入口保留 `pub const fn`。Rust 1.96 的 Default 实现是
受 `const_default` 控制的 `impl const Default`；本轮官方绑定及证明入口
验证稳定运行时方法，不把不稳定的 const trait 实现误称为稳定能力。
Deref 原 Vec impl 不是 const，入口也不是 const。
这三个入口只作验证表示，不替换或扩展标准库 API。

每个契约只有一个条款：空序列、布尔值与零长度的双向等价、完整 slice 序列。
不重复增加长度或逐元素条件，也不以容量、物理地址或分配器身份代替内容观察。
前述独立审阅已确认这种复用和有限表示；单纯构建及工具能力本身仍不能替代语义确认。

## 首次命令的诊断

`proofs/correctness/vec/reused-basic/engineer/default.stderr` 保存首次命令
在验证前退出 255 的诊断：此版本实际要求 `--verify-function` 与
`--verify-only-module` 配合，不能使用 help 所述的 `--verify-module`。
仅修正项目构建命令；原候选及失败输出保留，没有改写源体或契约。

完整 `unittest discover` 首次运行有七项通过、一项 const 探针失败；
稳定 `is_empty` 探针已编译成功。失败的 Default 探针只启用了
`const_default`，宿主 Rust 1.98.1 明确诊断还须启用 `const_trait_impl`。
原输入和错误保留在 `tests/reused-basic/engineer/unstable-default-enabled.*`，
整份运行保留在 `tests/reused-basic/suite.*`。这不是三个源体或契约的失败。
仅为这个不稳定能力探针补全两个 feature，并把各 const 检查分开，
便于只执行改变的检查和此前未执行的拒绝探针，不重跑已通过的七项或稳定 const 检查。

修正后的不稳定 Default 探针、稳定调用拒绝以及源码入口仅供运行时调用的拒绝
检查均通过，见 `tests/reused-basic/suite-const.stderr`。
这三个检查不要求元素实现 Default；临时 Rust 文件已删除，输入留在对应 `.input.json`。

## 当前编译、原生测试与完整性

`proofs/correctness/vec/reused-basic/source/` 保存三个原体各一个义务及实际编译，
以及聚合的三个义务和编译。三个入口都直接导入当前 `reused_basic.rs`。
原体的实际中间表示分别位于该目录的 `default/crate.vir:3475-3540`、
`is_empty/crate.vir:3541-3634`、`deref/crate.vir:3635-3732`；
具名参数、无前置条件和实际调用均已机械检查。函数体只出现 new、len、as_slice
依赖，不出现任何目标 API 的假设调用；没有新增证明公理。

真实 analyze 和 replay --reexecute 已在
`proofs/completeness/vec/reused-basic/engineer/` 完成，各恰好选择三个入口，
每个目标每次一个通过义务，原始查询均不可满足。
Default 比较 `(r1)@ =~= (r2)@`，is_empty 比较 `r1 == r2`，
Deref 比较 `r1 =~= r2`，后者是完整 slice 的外延内容比较，不是地址或长度代理。
所有原始查询的搜索开关均关闭，分别为 5、7、7 个。没有改写比较、增加输入限制
或将命名后的入口另计为 API。分析与重放的源码快照均逐字对应当前六份规格输入。

`tests/reused-basic/engineer/checker-correspondence.json` 记录检查器实际泛型、
参数、返回类型、唯一后置条件、比较式、原始查询假设和验证计数。
`correspondence.json` 将它们连接到官方完整声明和原函数体；
官方 Default/Deref trait 规格没有遗漏的附加方法前后置条件。
检查器的自由函数记录不表达原 trait 身份或单独的 const 元数据，
这些信息仍须由此处源码对应、真实标准库客户端和编译探针判断。
其 `contract_feasibility` 仍为 `not_run`，不把确定性当作可满足性证明。

同一轮新编译原生程序通过七个用例；十四个类型、局部借用逃逸和活跃共享借用
拒绝探针按预期失败。六个客户端义务同时覆盖官方绑定和源码入口。
完整结果在 `tests/reused-basic/engineer/`；const 检查的修正及旧失败如上保留。
运行时只测试指定输入，正式内容结论相对于未改动的官方 vstd 观察。
Vec 空序列本身不证明容量为零或无分配，slice 观察也不证明分配器或地址恒等。
Rust 1.96 文档的无分配说明来自原 Vec::new 委托边界，不扩大 Seq 契约的含义。

覆盖表仍有 138 行，只更新这三个目标和两个所有权转换的审阅状态，
其余 133 行逐字段不变。原借用、Cow、AsMut 及全部旧失败没有重跑或改判。
上述双轨结果和有限源码表示已获前述独立确认，不扩大为容量、分配器、
地址或底层内存实现的形式证明。私有 scratch 命令见
[覆盖说明](../inventory/COVERAGE.md)，不在本工程任务内启动 Reviewer。

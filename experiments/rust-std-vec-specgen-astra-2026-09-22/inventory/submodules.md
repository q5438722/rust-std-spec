# alloc::vec 源码清单与依赖图

## 边界与复跑

- 权威语义输入：`/home/chentianyu/nanvix-rust-std-spec-survey/rust-1.96/library/alloc/src/vec`；仅为必要的 trait 文档、稳定性和委托边界读取相邻 alloc/core。
- JSON 是完整记录；TSV 是本模块函数候选表，必须筛选 `status=included`，不能把排除行当作目标。
- 清单由 Rust AST 生成，不用 `pub fn` 正则计数。原源码、字节位置、generic/bounds、receiver、生命周期、cfg、docstring 与稳定性属性保留。
- parser 所需 grammar 缺失已经由实际 import 失败确认，再仅局部安装 `tree-sitter-rust==0.24.0`；宿主 `tree-sitter==0.25.2`。依赖固定在 `inventory/source-tests/requirements.txt`。
- grammar 不支持的 `const impl`、条件 `[const]`、`macro non_null` 仅在内存解析副本做等长替换；JSON 逐项记录，不改源文件或可执行证明副本。
- 核心 trait 只使用无错误的指定 AST 节点；相邻 core 文件中无关内建 derive-macro stub 不纳入 vec 的文件计数。
- 未评估任何 existing-vstd coverage。官方证明基线由父任务提供：`release/0.2026.09.20.aef82ed` / Rust `1.98.1`。这里没有正确性/完整性证明通过声明。

```sh
PYTHONDONTWRITEBYTECODE=1 python scripts/inventory_source.py
PYTHONDONTWRITEBYTECODE=1 python scripts/inventory_source.py --check
PYTHONDONTWRITEBYTECODE=1 python -m unittest discover -s inventory/source-tests -p 'test_*.py'
```

共 **16 个 vec 源文件，138 个源码所有的稳定公开 executable 条目**；另有 164 个排除函数候选，327 个 trait 默认方法实例单列。

## 每个源文件（没有零目标文件被隐藏）

| 文件 | 稳定 executable | 排除函数候选 | 实际职责 |
|---|---:|---:|---|
| `cow.rs` | 5 | 0 | 源码归属于 vec 的 Cow<[T]> 转换与 FromIterator；即使 owner 不是 Vec 也计入。 |
| `drain.rs` | 7 | 4 | 带源 Vec 独占借用的区间移出迭代器；析构移动尾部；keep_rest/allocator 不稳定。 |
| `extract_if.rs` | 4 | 2 | 闭包决定移出项的惰性迭代器；new 私有、allocator 不稳定；Iterator/Drop/Debug 稳定。 |
| `in_place_collect.rs` | 0 | 9 | 私有 InPlaceCollect/SpecInPlaceCollect/AsVecIntoIter 与原地收集；模块长文为不变量来源。 |
| `in_place_drop.rs` | 0 | 3 | 两个私有 Drop guard，分别销毁已写目标区与原源布局分配。 |
| `into_iter.rs` | 14 | 15 | 拥有分配的双端移出迭代器；显式消费者、Clone/Default/Drop；私有回收接口与不稳定优化 trait。 |
| `is_zero.rs` | 0 | 59 | 私有 unsafe IsZero 及标量、元组、Option 宏展开；全部逐项排除为私有专门化。 |
| `mod.rs` | 79 | 43 | Vec 表示、固有方法、转换/借用/顺序/散列/析构；含稳定 doc(hidden) 自由函数 from_elem。 |
| `partial_eq.rs` | 24 | 0 | __impl_slice_eq1 宏的每次调用展开 eq/ne；双 allocator、异元素类型、反向切片及 Cow 左侧均保留。 |
| `peek_mut.rs` | 0 | 5 | 整个公开 PeekMut surface 属 vec_peek_mut 不稳定功能；new 私有；保留排除清单。 |
| `set_len_on_drop.rs` | 0 | 4 | 私有长度提交 guard；源码以局部长度避免别名分析开销。 |
| `spec_extend.rs` | 0 | 6 | 私有 SpecExtend：一般迭代器、TrustedLen、IntoIter 移入、借用 Clone、TrivialClone 切片。 |
| `spec_from_elem.rs` | 0 | 6 | 私有 SpecFromElem：Clone 通用路径、IsZero、i8/u8/() 专门路径。 |
| `spec_from_iter.rs` | 0 | 3 | 私有 SpecFromIter 分派；IntoIter 未推进/足够剩余时复用分配，否则 SpecExtend。 |
| `spec_from_iter_nested.rs` | 0 | 3 | 私有嵌套分派，解决 Iterator 与 TrustedLen 重叠。 |
| `splice.rs` | 5 | 2 | Drain 包装与延迟替换；显式 next/next_back/size_hint/Drop，另有内建 derive(Debug)::fmt。 |

## 类型、表示与必须先连接的观察

- **`pub struct Vec<T, #[unstable(feature = "allocator_api", issue = "32838")] A: Allocator = Global>`**（`alloc/src/vec/mod.rs:438-441`）：buf: RawVec<T,A> + len；Seq 只描述初始化前缀，capacity/layout/allocator 与 spare 独立。省略 A 的源码 impl 维持默认分配器，显式 A 的 impl 绝不收窄。
- **`pub struct IntoIter<
    T,
    #[unstable(feature = "allocator_api", issue = "32838")] A: Allocator = Global,
>`**（`alloc/src/vec/into_iter.rs:45-61`）：buf/cap/alloc 持有原分配，ptr/end 表示 remaining；ZST 用 end 字节差；构造/消费者/借用必须共享状态关系。
- **`pub struct Drain<
    'a,
    T: 'a,
    #[unstable(feature = "allocator_api", issue = "32838")] A: Allocator + 'a = Global,
>`**（`alloc/src/vec/drain.rs:21-33`）：tail_start/tail_len/iter/vec；与源 Vec 的 head/removed/tail 分区连接，析构复原不能由 final 自动假设。
- **`pub struct Splice<
    'a,
    I: Iterator + 'a,
    #[unstable(feature = "allocator_api", issue = "32838")] A: Allocator + 'a = Global,
>`**（`alloc/src/vec/splice.rs:20-27`）：drain + replace_with；复用 Drain 视图并附替换迭代器状态；Debug derive 的 I:Debug、A:Debug、I::Item:Debug 均保留。
- **`pub struct ExtractIf<
    'a,
    T,
    F,
    #[unstable(feature = "allocator_api", issue = "32838")] A: Allocator = Global,
>`**（`alloc/src/vec/extract_if.rs:21-38`）：vec/idx/end/del/old_len/pred；已保留区、空洞、未检查区、范围外尾部及可变闭包状态一起连接。
- **`pub struct PeekMut<
    'a,
    T,
    #[unstable(feature = "allocator_api", issue = "32838")] A: Allocator = Global,
>`**（`alloc/src/vec/peek_mut.rs:15-21`）：vec 的末项独占借用包装；类型/方法当前均不稳定，只有表示分析，不列为稳定目标。
- **Cow/Box/切片/数组 owner**：本目录内的转换与比较也计入；Cow 保留 Borrowed/Owned 变体和借用寿命；Box 转换保留分配所有权；元素类型/allocator 不合并。
- **共享观察不是已有 view 声明**：`vec_contents`、`owned_remaining`、`drain_regions`、`extract_regions` 等是所需关系的名字，不是已实现或已证明的幽灵状态；父任务须对固定 vstd 先比对再决定复用。
- **借用**：返回 `&[T]`/`&mut [T]` 与本次 receiver 借用关联；可变引用需要初始内容、最终写回和未借用区 frame，不能禁止合法写入。`leak<'a>` 保留 A:'a 与返回类型隐含 T:'a，不加 `'static`。
- **回调**：FnMut/FnOnce、Clone、PartialEq、Hasher、Formatter 与 Drop 的可观察状态/异常行为不能隐藏成选答案的纯函数。

## 实际委托与表示依赖（并非证明完成顺序）

```text
Vec 基本表示 ── RawVec / Allocator / pointer + 已初始化前缀
  ├─ as_slice/as_mut_slice ── Deref/DerefMut ── slice indexing/hash/order/debug
  ├─ into_iter ── IntoIter remaining ── next/next_back/fold/try_fold/Drop
  ├─ drain ── Drain 区域 ── Splice（Drop 时消费 replace_with）
  ├─ extract_if ── ExtractIf 区域 + FnMut 状态（惰性 next，Drop 保留未扫描区）
  ├─ from_elem ── SpecFromElem ── IsZero 或 extend_with ── SetLenOnDrop
  ├─ extend/extend_from_slice ── SpecExtend ── 一般/TrustedLen/IntoIter/借用专门化
  ├─ extend_from_within ── 私有 ExtendFromWithinSpec（Clone / TrivialClone）
  └─ FromIterator ── SpecFromIter
         ├─ SpecFromIterNested ── Iterator / TrustedLen ── SpecExtend
         ├─ IntoIter 分配复用 ── fallback SpecExtend
         └─ InPlaceCollect ── 布局条件 / SourceIter / InPlaceIterable
                ├─ SpecInPlaceCollect + InPlaceDrop
                └─ IntoIter 剩余析构 + InPlaceDstDataSrcBufDrop + shrink
Cow 转换 ── Vec/as_slice/FromIterator；PartialEq 宏 ── 两侧 slice 比较
```

具体调用语法和调用点保存在每个条目的 `direct_calls`；这是完整的直接 call-expression 记录，不冒充已类型解析的动态调用图。操作符、deref coercion、隐式析构和内建 derive 的依赖还必须结合下列语义关系。

### `cow.rs`
- 委托/表示依赖：`alloc::borrow::Cow`, `Vec::as_slice`, `Vec::from_iter`。
- 观察关系：`cow_variant_contents`, `vec_contents`, `borrow_writeback`。
- 源码对应义务：Borrowed/Owned 变体及 'a 输入输出关系必须保留；From<Vec> 移动不克隆，From<&Vec>/切片/数组引用不分配。

### `drain.rs`
- 委托/表示依赖：`Vec::drain`, `core::slice::Iter`, `Vec::set_len`, `Vec::truncate`。
- 观察关系：`drain_regions`, `borrow_writeback`, `allocation_layout`。
- 源码对应义务：head、remaining、已移出区、tail 分区；返回 T 为移出值不是 &mut T；尾部复原依赖真实 Drop，不能将 borrow final 等同于析构；forget 可泄漏范围外元素。

### `extract_if.rs`
- 委托/表示依赖：`Vec::extract_if`, `slice::range`, `Vec::set_len`。
- 观察关系：`extract_regions`, `callback_state`, `borrow_writeback`。
- 源码对应义务：vec/idx/end/del/old_len/pred 与保留前缀、未扫描区和范围外尾部对应；谓词可修改 T/自身状态且按顺序执行；未消费元素在 Drop 中保留；panic 项不被移出。

### `in_place_collect.rs`
- 委托/表示依赖：`into_iter`, `in_place_drop`, `spec_from_iter_nested`, `SourceIter`, `InPlaceIterable`, `Allocator::shrink`。
- 观察关系：`in_place_regions`, `owned_remaining`, `allocation_layout`, `callback_state`。
- 源码对应义务：读取源/写入目标同分配；消费释放字节不少于写入字节；布局匹配或 shrink；未读区不可被覆盖；异常析构及 TrustedRandomAccessNoCoerce 的 NonDrop 前提不可省略。

### `in_place_drop.rs`
- 委托/表示依赖：`RawVec`, `in_place_collect`, `into_iter`。
- 观察关系：`in_place_regions`, `allocation_layout`。
- 源码对应义务：用 Src 布局释放分配、以 Dest 类型析构前缀；需与原地收集状态一致，不新增抽象生命周期事件系统。

### `into_iter.rs`
- 委托/表示依赖：`Vec::into_iter`, `RawVec`, `core::slice`, `in_place_collect`。
- 观察关系：`owned_remaining`, `allocation_layout`, `borrow_writeback`, `callback_state`。
- 源码对应义务：构造后 remaining 随 next/next_back/fold/try_fold 更新；ZST end 用字节距离编码长度；as_mut_slice 写回剩余区域；Clone 保留 allocator.clone；Drop 释放剩余元素及原分配。

### `is_zero.rs`
- 委托/表示依赖：`core::mem`, `SpecFromElem`。
- 观察关系：`zero_representation`。
- 源码对应义务：全零有效表示不是普遍零值定理；Option 布局/niche、ZST 与数组长度分支按源码适用；指针不实现 IsZero（provenance 注释）。

### `mod.rs`
- 委托/表示依赖：`RawVec`, `Allocator`, `core::slice`, `alloc::slice`, `into_iter`, `drain`, `splice`, `extract_if`, `spec_from_elem`, `spec_extend`, `spec_from_iter`, `set_len_on_drop`。
- 观察关系：`vec_contents`, `allocation_layout`, `borrow_writeback`, `callback_state`。
- 源码对应义务：Seq 对应已初始化前缀；len<=capacity、ZST/isize 限界；spare 与已初始化区不重叠；原始指针内容/有效期不能仅由地址推得；Clone/FnMut/Drop 不得增加 Copy/Eq/'static 假设。

### `partial_eq.rs`
- 委托/表示依赖：`core::cmp::PartialEq`, `core::slice`, `alloc::borrow::Cow`。
- 观察关系：`vec_contents`, `cow_variant_contents`, `element_comparison`。
- 源码对应义务：T: PartialEq<U> 不是 Eq；不能把两个 allocator 合一；源码注释中未启用的宏调用不产生 impl。每个实际 impl 的 eq 与 ne 都是本模块显式实现。

### `peek_mut.rs`
- 委托/表示依赖：`Vec::peek_mut`, `Vec::pop`, `slice::get_unchecked`。
- 观察关系：`borrow_writeback`。
- 源码对应义务：独占借用最后元素及非空构造关系；当前稳定目标中排除，不声称已覆盖。

### `set_len_on_drop.rs`
- 委托/表示依赖：`Vec::extend_with`, `Vec::extend_trusted`。
- 观察关系：`initialized_prefix`。
- 源码对应义务：只有实际已初始化的前缀可提交到 len；Clone/迭代 panic 时 guard 仍提交正确长度。

### `spec_extend.rs`
- 委托/表示依赖：`Vec::extend_desugared`, `Vec::extend_trusted`, `Vec::append_elements`, `into_iter`。
- 观察关系：`vec_contents`, `owned_remaining`, `callback_state`。
- 源码对应义务：各专门化共享元素顺序目标但适用界限不同；借用 Clone 与移动 T 分开；IntoIter 转移后必须不再析构已移入元素。

### `spec_from_elem.rs`
- 委托/表示依赖：`is_zero`, `Vec::extend_with`, `RawVec::with_capacity_zeroed_in`。
- 观察关系：`vec_contents`, `allocation_layout`, `callback_state`。
- 源码对应义务：from_elem/vec![e;n] 的委托依赖；Clone 次数/副作用与末项移动不可凭纯值模型抹去；零初始化须有表示关系。

### `spec_from_iter.rs`
- 委托/表示依赖：`spec_from_iter_nested`, `spec_extend`, `in_place_collect`, `into_iter`。
- 观察关系：`vec_contents`, `owned_remaining`, `allocation_layout`。
- 源码对应义务：分配复用不是稳定容量等式；一般路径与专门路径的顺序/所有权对应必须都证明。

### `spec_from_iter_nested.rs`
- 委托/表示依赖：`spec_extend`, `RawVec::MIN_NON_ZERO_CAP`, `Vec::with_capacity`。
- 观察关系：`vec_contents`, `callback_state`, `allocation_layout`。
- 源码对应义务：空迭代器、预取首元素、size_hint、精确上界和超 usize::MAX 的 panic 分支分开。

### `splice.rs`
- 委托/表示依赖：`drain`, `Vec::extend`, `Vec::from_iter`, `RawVec::reserve`。
- 观察关系：`drain_regions`, `replacement_iterator`, `callback_state`。
- 源码对应义务：replace_with 仅在 Drop 中消费；fill/move_tail 为私有 Drain 方法；不足/恰好/过量及临时 Vec 分支都须保留；泄漏时移除数量未规定。ExactSizeIterator::len 来自默认实现。

## 已定位的相邻语义依赖（不新增目标数）

- `alloc/src/raw_vec/mod.rs`：Vec/IntoIter 的分配、capacity、指针与释放表示；RawVec 不析构 T。
  - AST 定位：`RawVec` L73-76, `RawVecInner` L85-94, `new` L103-105, `with_capacity_in` L175-180, `grow_one` L186-189, `new_in` L199-203, `try_with_capacity_in` L208-213, `with_capacity_zeroed_in` L219-224, `into_box` L238-250, `from_raw_parts_in` L263-273, `from_nonnull_in` L282-289, `ptr` L295-297, `non_null` L300-302, `capacity` L308-310, `allocator` L314-316, `reserve` L339-342, `try_reserve` L345-352, `reserve_exact` L372-375, `try_reserve_exact` L378-385, `shrink_to_fit` L399-402, `try_shrink_to_fit` L415-417, `drop` L422-425；完整签名、bounds、文档位置见 JSON `dependency_sources`。
- `alloc/src/slice.rs`：Vec Clone/From 借用数据/Box 转移的委托及 Clone/TrivialClone 专门化。
  - AST 定位：`to_vec` L372-377, `to_vec_in` L396-461, `to_vec` L403-405, `to_vec` L410-441, `to_vec` L446-459, `into_vec` L480-486, `SpecCloneIntoVec` L808-810, `clone_into` L809-809, `clone_into` L814-825, `clone_into` L830-833, `clone_into` L845-847；完整签名、bounds、文档位置见 JSON `dependency_sources`。
- `core/src/slice/raw.rs`：原始指针到借用内容：单分配、对齐、初始化、长度界与共享/独占访问要求。
  - AST 定位：`from_raw_parts` L124-141, `from_raw_parts_mut` L179-196；完整签名、bounds、文档位置见 JSON `dependency_sources`。
- `core/src/slice/index.rs`：drain/extract_if/extend_from_within 的 RangeBounds 正规化与 panic 边界。
  - AST 定位：`range` L907-913, `into_slice_range` L1011-1038；完整签名、bounds、文档位置见 JSON `dependency_sources`。
- `alloc/src/borrow.rs`：Cow 变体与 Borrowed/Owned 内容及借用/移动关系。
  - AST 定位：`Cow` L169-180, `into_owned` L331-336, `deref` L349-354；完整签名、bounds、文档位置见 JSON `dependency_sources`。
- `alloc/src/boxed.rs`：Box<[T],A> 与 Vec<T,A> 的同分配所有权转换及 allocator 泛型。
  - AST 定位：`Box` L234-237, `into_raw_with_allocator` L1642-1652；完整签名、bounds、文档位置见 JSON `dependency_sources`。
- `core/src/alloc/mod.rs`：RawVec 与原地收集的 fitting layout、分配失败、grow/shrink 安全前提。
  - AST 定位：`Allocator` L113-376, `allocate` L140-140, `allocate_zeroed` L157-162, `deallocate` L173-173, `grow` L213-237, `grow_zeroed` L276-300, `shrink` L340-364；完整签名、bounds、文档位置见 JSON `dependency_sources`。
- `core/src/slice/cmp.rs`：Vec/切片/Cow 比较委托；异元素 PartialEq 与字典序观察，不改为 Eq。
  - AST 定位：`eq` L20-29, `cmp` L40-42, `partial_cmp` L61-63；完整签名、bounds、文档位置见 JSON `dependency_sources`。
- `core/src/hash/mod.rs`：Vec::hash 委托到对应切片的 Hash；保留 Hasher 状态和调用协议。
  - AST 定位：`hash` L933-936；完整签名、bounds、文档位置见 JSON `dependency_sources`。
- `core/src/fmt/mod.rs`：Vec::fmt 的切片格式化委托；Formatter 状态/错误不是纯字符串假设。
  - AST 定位：`fmt` L3122-3124；完整签名、bounds、文档位置见 JSON `dependency_sources`。

## 不可混淆的计数与排除决定

- `<Vec<T,A> as AsRef<Vec<T,A>>>::as_ref` 与 `<Vec<T,A> as AsRef<[T]>>::as_ref` 是两个身份；AsMut 同理。owner、trait 实参、impl 泛型和方法泛型均独立保存。
- 稳定 impl 中的 `Iterator::{advance_by,next_chunk,__iterator_get_unchecked}`、`DoubleEndedIterator::advance_back_by`、`ExactSizeIterator::is_empty`、`Extend::{extend_one,extend_reserve,extend_one_unchecked}` 由 trait 声明确定为不稳定；不可仅继承 impl 的 stable 标签。
- 相反 `Vec::push/push_mut` 的 `[const] Allocator + [const] Destruct`，以及稳定 `try_fold` 的 Try bound 不导致删除该稳定运行时 API。const 稳定性单独列出。
- `from_elem` 虽 `doc(hidden)` 仍是 stable public executable，自身没有 docstring；它是目录外 `alloc/src/macros.rs` 的 `vec![elem;n]` 委托入口。宏本身不是本目录新 API。
- `partial_eq.rs` 的所有实际宏调用（包括无 Vec owner 的 Cow/切片配对）展开；注释里的候选调用不计。私有 IsZero 宏也展开到排除行，元组递归不是按一行一个 impl 猜数。
- Splice 的 `derive(Debug)` 是稳定 executable fmt 条目，不可遗漏；清单只展开签名/必要 bounds，未凭空写一个用于证明的替代 body。
- `Eq`、`Send`、`Sync`、`FusedIterator`、`UnwindSafe` 等空 impl，及仅有关联常量的优化 trait impl，不是 executable 方法。Splice 的空 ExactSizeIterator impl 仍使默认 len 可用，另列 inherited_methods。
- `Iterator` 等 trait 未覆盖的默认方法按每个本地 impl 机械枚举，但实现源在 core，不加到本模块实现数。supertrait 方法沿原 trait 身份处理，不按多个 trait 重复镜像。
- `Into/From<T>/TryInto/TryFrom`、Borrow/BorrowMut、ToOwned、Any、Iterator->IntoIterator 与引用转发 blanket 用源声明族表示；不存在无限展开所有泛型实例的假计数。`From<!>` reservation impl 明确不可用。
- Vec 的 `Borrow<[T]>` / `BorrowMut<[T]>` 实现在相邻 alloc/slice.rs；只记模块外边界。deref 可见的 slice API、目录外集合转换/std trait impl 和 std::vec 重导出均非本目录所定义；没有产生 Slice campaign 输出。
- 私有 spec_*、in_place_*、SetLenOnDrop 与局部 Drop/panic guard 是源正确性依赖，不作为独立 public 目标，也不因排除而声称其证明可跳过。

## 机械检查

- vec 全文件集合 == mod.rs 模块声明集合 == 实质依赖分析集合。
- vec AST 零 ERROR/缺失节点；等长 parser-only 兼容保持原始字节/行号。
- 每个原始 function_item/function_signature_item 恰好分类一次（含嵌套 helper）。
- 所有 item macro 必须识别并展开；公开 PartialEq 每调用恰好 eq/ne 两项。
- canonical stable API 与候选 inventory_id 均无重复。
- AsRef/AsMut 两个目标、allocator/const bound、doc(hidden) from_elem、derive(Debug) 保留。
- 稳定 impl 中不稳定 trait 成员排除；try_fold 不因 Try bound 而排除。
- `--check` 重新从源码提取，逐字比较 JSON/TSV/源码段落；保留的 vstd 段落由 `scripts/inventory_vstd.py --check` 独立检查，不使用旧清单来构造新清单。
- source-tests 覆盖宏配对、反向 owner、双 allocator、稳定性继承、默认与空 impl、文档位置、cfg、泛型/生命周期及变更后重放。
- 这些检查只验证清单/源码抽取，既不是 Verus 源实现证明，也不是 spec-determin-tool 完整性检查。

<!-- BEGIN OFFICIAL VSTD COVERAGE -->

## Official pinned vstd views and coverage relations

Baseline: `release/0.2026.09.20.aef82ed` / `aef82eda71838deef4a8cd0260fda6c9504be9b9`; only `toolchains/upstream/source/vstd` is scanned. Source identities and domains are taken unchanged from `source_api.json` / `.tsv`. This section is appended by `scripts/inventory_vstd.py`; the source-inventory section above is not rewritten.

### Views first (definitions, limitations, constructor relations)

#### `vec_sequence`: official_opaque_view

Domain: Vec<T, A>, T unrestricted, A: Allocator.
View::V = Seq<T>; DeepView maps each element and separately requires T: DeepView. Ghost/allocator cfg has A; the non-ghost fallback is Global-only. The index-decreases, has_resolved and decreases-to-view axioms here explicitly use default-allocator Vec<T>, unlike the allocator-generic len axiom.
Required source/constructor relation: Relate the initialized prefix of buf/len to Seq, including ZST and length bounds. The opaque view does not expose capacity, allocation, addresses or allocator identity.
Definition references: `toolchains/upstream/source/vstd/std_specs/vec.rs:24-24`; `toolchains/upstream/source/vstd/view.rs:104-108`; `toolchains/upstream/source/vstd/view.rs:111-118`; `toolchains/upstream/source/vstd/view.rs:121-125`; `toolchains/upstream/source/vstd/view.rs:128-135`; `toolchains/upstream/source/vstd/view.rs:22-29`.
Constructor/relation references: `toolchains/upstream/source/vstd/std_specs/vec.rs:81-81`; `toolchains/upstream/source/vstd/std_specs/vec.rs:85-90`; `toolchains/upstream/source/vstd/std_specs/vec.rs:33-38`; `toolchains/upstream/source/vstd/std_specs/vec.rs:471-477`.
Depends on: none.

#### `slice_sequence`: official_opaque_view

Domain: [T], T unrestricted.
The Vec borrow constructors tie slice@ to the Vec sequence; mutable constructors give immediate equality and final(slice)@ == final(vec)@.
Required source/constructor relation: Preserve lawful writes and the initialized-region relation. Pointer metadata alone is not content; final is the borrow's final value, not evidence of Drop execution.
Definition references: `toolchains/upstream/source/vstd/slice.rs:13-17`; `toolchains/upstream/source/vstd/slice.rs:19-26`; `toolchains/upstream/source/vstd/view.rs:22-29`.
Constructor/relation references: `toolchains/upstream/source/vstd/slice.rs:83-86`; `toolchains/upstream/source/vstd/slice.rs:218-221`; `toolchains/upstream/source/vstd/std_specs/vec.rs:236-239`; `toolchains/upstream/source/vstd/std_specs/vec.rs:242-246`; `toolchains/upstream/source/vstd/std_specs/vec.rs:248-253`; `toolchains/upstream/source/vstd/std_specs/vec.rs:255-261`; `toolchains/upstream/source/vstd/std_specs/vec.rs:479-480`; `toolchains/upstream/source/vstd/std_specs/vec.rs:482-486`.
Depends on: `vec_sequence`.

#### `index_domain`: official_trait_and_concrete_models

Domain: I: SliceIndex<[T]>; mutable Vec content hook only for usize indexing syntax.
Vec index_req quantifies over slices with the same sequence; immutable index has an existential slice/call_ensures postcondition. usize plus six range SliceIndex models are explicit in std_specs/slice.rs.
Required source/constructor relation: Do not transfer the slice IndexMut postcondition through Vec's generic IndexMut without a source/delegation proof. The generic IndexMut trait only adds a precondition.
Definition references: `toolchains/upstream/source/vstd/std_specs/core.rs:47-60`; `toolchains/upstream/source/vstd/std_specs/core.rs:63-70`; `toolchains/upstream/source/vstd/slice.rs:119-168`; `toolchains/upstream/source/vstd/std_specs/vec.rs:178-182`.
Constructor/relation references: `toolchains/upstream/source/vstd/std_specs/vec.rs:184-190`; `toolchains/upstream/source/vstd/std_specs/vec.rs:53-61`; `toolchains/upstream/source/vstd/std_specs/vec.rs:67-78`; `toolchains/upstream/source/vstd/std_specs/slice.rs:330-336`; `toolchains/upstream/source/vstd/std_specs/slice.rs:338-344`; `toolchains/upstream/source/vstd/std_specs/range.rs:324-334`; `toolchains/upstream/source/vstd/std_specs/range.rs:472-478`; `toolchains/upstream/source/vstd/std_specs/range.rs:483-489`; `toolchains/upstream/source/vstd/std_specs/range.rs:493-495`.
Depends on: `vec_sequence`, `slice_sequence`.

#### `iterator_framework`: official_generic_prophetic_contract

Domain: Iterator / DoubleEndedIterator / ExactSizeIterator; no concrete representation implied.
remaining is the prophetic sequence of future yielded items. Transition laws are guarded by obeys_prophetic_iter_laws; will_return_none and an optional decrease metric are separate observations.
Required source/constructor relation: Establish the concrete iterator's law predicate and its constructor/state relation. An arbitrary guarded framework is not a view of a source representation.
Definition references: `toolchains/upstream/source/vstd/std_specs/iter.rs:12-243`; `toolchains/upstream/source/vstd/std_specs/iter.rs:247-286`; `toolchains/upstream/source/vstd/std_specs/iter.rs:290-300`; `toolchains/upstream/source/vstd/std_specs/iter.rs:359-382`.
Constructor/relation references: `toolchains/upstream/source/vstd/std_specs/iter.rs:35-54`; `toolchains/upstream/source/vstd/std_specs/iter.rs:260-279`; `toolchains/upstream/source/vstd/std_specs/iter.rs:297-299`.
Depends on: none.

#### `owned_iterator_state`: official_state_relative_spec_functions_not_View

Domain: IntoIter<T, A>, T unrestricted, A: Allocator.
remaining is prophetic; into_iter_elts(i) is an uninterpreted, non-prophetic observation of the iterator value/state i. peek/peek_back use that observation. obeys_prophetic_iter_laws is true for IntoIter; will_return_none and decrease remain uninterpreted.
Required source/constructor relation: Vec::into_iter establishes remaining(i0) == vec@ == into_iter_elts(i0) and decrease(i0) is Some. next/next_back change remaining, but give no equation for into_iter_elts(i1). Neither frozen-original contents nor elts(i1)==remaining(i1) is an invariant supplied by vstd. as_slice/as_mut_slice/Clone/Default need their own state connections.
Definition references: `toolchains/upstream/source/vstd/std_specs/vec.rs:352-352`; `toolchains/upstream/source/vstd/std_specs/vec.rs:356-356`; `toolchains/upstream/source/vstd/std_specs/vec.rs:358-374`; `toolchains/upstream/source/vstd/std_specs/vec.rs:376-385`; `toolchains/upstream/source/vstd/std_specs/iter.rs:12-243`; `toolchains/upstream/source/vstd/std_specs/iter.rs:247-286`.
Constructor/relation references: `toolchains/upstream/source/vstd/std_specs/vec.rs:393-401`; `toolchains/upstream/source/vstd/std_specs/iter.rs:35-54`; `toolchains/upstream/source/vstd/std_specs/iter.rs:260-279`; `toolchains/upstream/source/vstd/std_specs/iter.rs:359-382`.
Depends on: `vec_sequence`, `iterator_framework`.

#### `borrowed_iterator_state`: official_state_relative_spec_functions_not_View

Domain: core::slice::Iter<'a,T> and IterMut<'a,T>.
Iter remaining is Seq<&T>; constructor elts == remaining.unref(). IterMut remaining is Seq<&mut T>; slice::iter_mut relates each reference's initial/final value to the corresponding slice slot.
Required source/constructor relation: The shared Vec IntoIterator impl is directly assumed. &mut Vec IntoIterator is not: its source delegates through DerefMut to slice::iter_mut. Do not confuse that with the deref-visible method vec.iter_mut(), which is not a Vec-owned target.
Definition references: `toolchains/upstream/source/vstd/std_specs/slice.rs:403-403`; `toolchains/upstream/source/vstd/std_specs/slice.rs:407-407`; `toolchains/upstream/source/vstd/std_specs/slice.rs:409-425`; `toolchains/upstream/source/vstd/std_specs/slice.rs:448-448`; `toolchains/upstream/source/vstd/std_specs/slice.rs:452-465`.
Constructor/relation references: `toolchains/upstream/source/vstd/std_specs/vec.rs:403-409`; `toolchains/upstream/source/vstd/std_specs/slice.rs:427-432`; `toolchains/upstream/source/vstd/std_specs/slice.rs:434-440`; `toolchains/upstream/source/vstd/std_specs/slice.rs:468-482`.
Depends on: `slice_sequence`, `iterator_framework`.

#### `collection_constructor`: official_trait_specialization_with_opaque_input_observation

Domain: FromIterator<T> for Vec<T> (Global, exactly as in the source); input I: IntoIterator<Item=T>.
from_iter ensures result@ == into_iter_remaining(input). The supplied axiom relates this UF to remaining only for inputs that are themselves Iterator + IteratorSpec; it is not in group_iter_axioms.
Required source/constructor relation: For arbitrary IntoIterator inputs, do not silently replace into_iter_remaining(input) by remaining(input.into_iter()) or Vec input contents. collect's conditional trait contract is a separate route. No allocator-general FromIterator impl is present in the source target.
Definition references: `toolchains/upstream/source/vstd/std_specs/iter.rs:339-350`; `toolchains/upstream/source/vstd/std_specs/vec.rs:411-415`; `toolchains/upstream/source/vstd/std_specs/iter.rs:328-328`.
Constructor/relation references: `toolchains/upstream/source/vstd/std_specs/iter.rs:345-349`; `toolchains/upstream/source/vstd/std_specs/iter.rs:332-335`; `toolchains/upstream/source/vstd/std_specs/iter.rs:147-155`.
Depends on: `vec_sequence`, `iterator_framework`.

#### `clone_relation`: official_weak_relational_model

Domain: T: Clone, without Copy/Eq/DeepView/'static strengthening.
cloned(a,b) = call_ensures(T::clone, (&a,), b) || a == b. Generic Clone::clone has no postcondition; element equality and Clone/callback side-effect traces are not supplied.
Required source/constructor relation: Preserve the reflexive weak relation and allocator.clone requirements; do not upgrade it to element equality or erase stateful Clone behavior.
Definition references: `toolchains/upstream/source/vstd/std_specs/clone.rs:7-11`; `toolchains/upstream/source/vstd/pervasive.rs:416-418`; `toolchains/upstream/source/vstd/pervasive.rs:426-428`.
Constructor/relation references: `toolchains/upstream/source/vstd/std_specs/vec.rs:278-286`; `toolchains/upstream/source/vstd/std_specs/vec.rs:306-318`; `toolchains/upstream/source/vstd/std_specs/vec.rs:163-176`; `toolchains/upstream/source/vstd/std_specs/vec.rs:388-391`.
Depends on: `vec_sequence`.

#### `comparison_relation`: official_conditional_trait_model

Domain: T: PartialEq<U>; Vec operands may have distinct A1/A2.
Vec-to-Vec eq/ne use T::obeys_eq_spec and pointwise T::eq_spec. The explicit eq assume has no own ensures. Other Vec/Cow/slice/array pairings have only their generic trait contract, not this concrete model. The three law/view-equality proof helpers are Global-only and do not strengthen the A1/A2-generic method contracts.
Required source/constructor relation: Do not infer structural equality unconditionally, collapse allocators, or apply ne.default_ensures to the source's explicit ne implementations. Vec Ord/PartialOrd have no concrete comparison model here.
Definition references: `toolchains/upstream/source/vstd/std_specs/cmp.rs:11-27`; `toolchains/upstream/source/vstd/std_specs/vec.rs:335-344`; `toolchains/upstream/source/vstd/std_specs/slice.rs:385-396`.
Constructor/relation references: `toolchains/upstream/source/vstd/std_specs/vec.rs:329-333`; `toolchains/upstream/source/vstd/std_specs/cmp.rs:18-20`; `toolchains/upstream/source/vstd/std_specs/cmp.rs:22-26`; `toolchains/upstream/source/vstd/std_specs/slice.rs:379-383`; `toolchains/upstream/source/vstd/std_specs/vec.rs:417-425`; `toolchains/upstream/source/vstd/std_specs/vec.rs:427-439`; `toolchains/upstream/source/vstd/std_specs/vec.rs:441-458`.
Depends on: `vec_sequence`, `slice_sequence`.

#### `cow_slice_sequence`: official_view_with_narrower_type_domain

Domain: Cow<'a,[T]> View requires T: View + Clone; DeepView requires T: DeepView + Clone.
Both Borrowed and Owned branches map to the contained sequence; the sequence view alone forgets the variant. The enum type registration is not an API conversion specification.
Required source/constructor relation: Source Cow conversions require Clone / ToOwned, not T: View or DeepView. Preserve the full source type domain and variant/borrowing relation; do not add those extra bounds merely to use the official view.
Definition references: `toolchains/upstream/source/vstd/std_specs/borrow.rs:24-24`; `toolchains/upstream/source/vstd/std_specs/borrow.rs:80-89`; `toolchains/upstream/source/vstd/std_specs/borrow.rs:92-101`.
Constructor/relation references: none.
Depends on: `vec_sequence`, `slice_sequence`.

#### `array_box_string_adapters`: official_indirect_dependencies

Domain: arrays [T;N], Box<[T],A>::into_vec, str bytes.
Box into_vec has an A: Allocator signature; the literal View-for-Box impl in view.rs is default-allocator only, with borrowed/deref observations also available. str::as_bytes returns UTF-8 bytes, not char count.
Required source/constructor relation: These are different identities from Vec/Cow/Box From and array TryFrom. slice_to_vec<T:Copy> is a vstd wrapper, not a spec for source Clone-generic From<&[T]> or slice::to_vec.
Definition references: `toolchains/upstream/source/vstd/array.rs:15-21`; `toolchains/upstream/source/vstd/array.rs:11-13`; `toolchains/upstream/source/vstd/view.rs:41-48`; `toolchains/upstream/source/vstd/string.rs:69-73`.
Constructor/relation references: `toolchains/upstream/source/vstd/array.rs:115-121`; `toolchains/upstream/source/vstd/array.rs:123-126`; `toolchains/upstream/source/vstd/std_specs/smart_ptrs.rs:12-15`; `toolchains/upstream/source/vstd/std_specs/smart_ptrs.rs:17-20`; `toolchains/upstream/source/vstd/string.rs:125-128`.
Depends on: `vec_sequence`, `slice_sequence`.

#### `drain_regions`: missing_official_concrete_view

Domain: Drain<'a,T,A> with source lifetime and allocator domain intact.
No active Drain name, external type, constructor spec or concrete iterator-law specialization in this official vstd.
Required source/constructor relation: Connect Vec::drain to head/remaining/tail and moved-out T values; track tail restoration by real Drop separately from borrow final. forget may skip cleanup. Generic guarded Iterator laws do not establish this connection.
Definition references: `toolchains/upstream/source/vstd/std_specs/iter.rs:35-54`; `toolchains/upstream/source/vstd/std_specs/iter.rs:260-279`.
Constructor/relation references: `toolchains/upstream/source/vstd/std_specs/iter.rs:35-54`; `toolchains/upstream/source/vstd/std_specs/iter.rs:260-279`.
Depends on: `vec_sequence`, `slice_sequence`, `borrowed_iterator_state`.

#### `extract_regions`: missing_official_concrete_view

Domain: ExtractIf<'a,T,F,A>, F: FnMut(&mut T)->bool.
No active ExtractIf name, type/constructor spec or concrete iterator model.
Required source/constructor relation: Connect vec/idx/end/del/old_len/pred to retained, removed, unvisited and out-of-range regions; preserve mutable element/predicate state, order, panic and lazy Drop behavior.
Definition references: `toolchains/upstream/source/vstd/std_specs/iter.rs:35-54`; `toolchains/upstream/source/vstd/std_specs/core.rs:20-22`.
Constructor/relation references: `toolchains/upstream/source/vstd/std_specs/iter.rs:35-54`; `toolchains/upstream/source/vstd/std_specs/core.rs:20-22`.
Depends on: `vec_sequence`, `slice_sequence`.

#### `splice_regions`: missing_official_concrete_view

Domain: Splice<'a,I,A>, I: Iterator.
No active Splice name, type/constructor spec or concrete iterator model. ExactSizeIterator::len remains an inherited generic contract, not a new source-owned API.
Required source/constructor relation: Relate Drain regions and replace_with state at construction; replacement is consumed during Drop, including fill/move-tail/temporary-Vec paths. final does not prove Drop; forgotten Splice has weaker removal semantics.
Definition references: `toolchains/upstream/source/vstd/std_specs/iter.rs:35-54`; `toolchains/upstream/source/vstd/std_specs/iter.rs:260-279`.
Constructor/relation references: `toolchains/upstream/source/vstd/std_specs/iter.rs:35-54`; `toolchains/upstream/source/vstd/std_specs/iter.rs:260-279`.
Depends on: `drain_regions`, `collection_constructor`, `owned_iterator_state`.

#### `allocation_and_callbacks`: source_bridge_not_supplied_by_sequence_views

Domain: allocator, RawVec, initialized/spare regions, raw pointers, callbacks and destructors.
Type-level trait registration and Seq abstractions are not capacity/layout/ownership/lifecycle or callback-state specifications.
Required source/constructor relation: Retain private source specialization/guards as proof dependencies. No API acceptance, new view axiom, synthetic lifecycle machine or source rewrite is performed by this inventory.
Definition references: `toolchains/upstream/source/vstd/std_specs/core.rs:84-86`; `toolchains/upstream/source/vstd/std_specs/core.rs:13-17`; `toolchains/upstream/source/vstd/std_specs/core.rs:20-22`; `toolchains/upstream/source/vstd/std_specs/core.rs:94-96`.
Constructor/relation references: `toolchains/upstream/source/vstd/std_specs/manually_drop.rs:30-33`; `toolchains/upstream/source/vstd/std_specs/manually_drop.rs:47-52`.
Depends on: `vec_sequence`.

### Coverage classes (not correctness/completeness acceptance)

Exact counts signature bindings, including weak/conditional contracts; partial preserves the narrower call/type domain. Trait-only, indirect and none are not concrete API coverage. No API has been accepted by either proof track here.

| Source module | APIs | exact | partial | trait_only | indirect | none |
|---|---:|---:|---:|---:|---:|---:|
| `cow.rs` | 5 | 0 | 0 | 5 | 0 | 0 |
| `drain.rs` | 7 | 0 | 0 | 3 | 1 | 3 |
| `extract_if.rs` | 4 | 0 | 0 | 2 | 0 | 2 |
| `in_place_collect.rs` | 0 | 0 | 0 | 0 | 0 | 0 |
| `in_place_drop.rs` | 0 | 0 | 0 | 0 | 0 | 0 |
| `into_iter.rs` | 14 | 2 | 0 | 3 | 3 | 6 |
| `is_zero.rs` | 0 | 0 | 0 | 0 | 0 | 0 |
| `mod.rs` | 79 | 28 | 1 | 14 | 17 | 19 |
| `partial_eq.rs` | 24 | 2 | 0 | 22 | 0 | 0 |
| `peek_mut.rs` | 0 | 0 | 0 | 0 | 0 | 0 |
| `set_len_on_drop.rs` | 0 | 0 | 0 | 0 | 0 | 0 |
| `spec_extend.rs` | 0 | 0 | 0 | 0 | 0 | 0 |
| `spec_from_elem.rs` | 0 | 0 | 0 | 0 | 0 | 0 |
| `spec_from_iter.rs` | 0 | 0 | 0 | 0 | 0 | 0 |
| `spec_from_iter_nested.rs` | 0 | 0 | 0 | 0 | 0 | 0 |
| `splice.rs` | 5 | 0 | 0 | 3 | 1 | 1 |
| **Total** | **138** | **32** | **1** | **52** | **22** | **31** |

### Exact identities that must not be merged

| Canonical source identity | Classification | Official relation |
|---|---|---|
| `<alloc::vec::Vec<T, A> as core::convert::AsRef<alloc::vec::Vec<T, A>>>::as_ref` | `none`; no own spec | none (identity return is source behavior, not a vstd contract) |
| `<alloc::vec::Vec<T, A> as core::convert::AsMut<alloc::vec::Vec<T, A>>>::as_mut` | `none`; no own spec | none (identity return is source behavior, not a vstd contract) |
| `<alloc::vec::Vec<T, A> as core::convert::AsRef<[T]>>::as_ref` | `indirect`; no own spec | `toolchains/upstream/source/vstd/std_specs/vec.rs:248-253`; `toolchains/upstream/source/vstd/std_specs/vec.rs:236-239` |
| `<alloc::vec::Vec<T, A> as core::convert::AsMut<[T]>>::as_mut` | `indirect`; no own spec | `toolchains/upstream/source/vstd/std_specs/vec.rs:255-261`; `toolchains/upstream/source/vstd/std_specs/vec.rs:242-246` |

Immutable generic `Index<I>`: `toolchains/upstream/source/vstd/std_specs/vec.rs:184-190`, with `IndexSpecImpl` `toolchains/upstream/source/vstd/std_specs/vec.rs:178-182`; the `usize` hook `toolchains/upstream/source/vstd/std_specs/vec.rs:53-61` is not another API. Mutable `IndexMut<I>` has only the generic precondition `toolchains/upstream/source/vstd/std_specs/core.rs:66-69`; content/writeback is provided for `usize` operator syntax by `toolchains/upstream/source/vstd/std_specs/vec.rs:67-78`, not general I or explicit UFCS.

Do not strengthen `with_capacity`, `reserve`, or `try_reserve`: `toolchains/upstream/source/vstd/std_specs/vec.rs:115-118`, `toolchains/upstream/source/vstd/std_specs/vec.rs:125-131`, `toolchains/upstream/source/vstd/std_specs/vec.rs:133-139` only constrain sequence contents/emptiness; `try_reserve` leaves the Result variant unconstrained. `cloned` is reflexive call_ensures, not equality.

All 133 official vstd files are fingerprinted; 130 Rust files are lexically scanned with nested comments/strings excluded. 485 active assume declarations/templates are scanned (not a macro-expanded API count). Active external_fn_specification attributes: 0. The commented clone_from examples are inactive. All 30 Vec-file assume declarations are reconciled: 28 stable targets and the two excluded unstable constructors `new_in` / `with_capacity_in`; no duplicate external-spec claims.

The 164 excluded source candidates and 327 inherited instances remain outside the 138 source-owned rows. The inherited framework relations are copied/mapped from the existing input, not re-enumerated. Private spec_*/in_place_* modules still appear in the view dependency map with zero public targets.

Full literal generics, target, signature, requires/ensures/default_ensures and byte/line ranges are in `inventory/vstd_coverage.json` (`evidence`); the 138-row TSV is `inventory/vstd_coverage.tsv`. Submodule-to-view relations and source constructor/delegation edges precede or accompany every API. Supplemental binary probes live only in `inventory/vstd-tests`; they are clients of existing assumptions, not implementation or determinism proofs.

```sh
PYTHONDONTWRITEBYTECODE=1 python3 scripts/inventory_vstd.py --check
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s inventory/vstd-tests -p 'test_*.py'
PYTHONDONTWRITEBYTECODE=1 python3 inventory/vstd-tests/check_bindings.py
```

<!-- END OFFICIAL VSTD COVERAGE -->

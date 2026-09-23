---
title: "Vec 借用契约中的 View 同余与状态边界"
description: "固定官方 Verus/vstd 下的同状态逻辑蕴含、跨类型桥接和借用终态边界。"
---

## 适用范围

本页讨论官方 Verus `release/0.2026.09.20.aef82ed` 及其未修改 vstd 的逻辑模型。
被解释的 Vec 源码是 Rust 1.96，工具宿主是 Rust 1.98.1；
这里的逻辑事实不宣称两个 Rust 版本普遍等价，也不授予具体 API 独立确认。

## 同状态的值等式蕴含 View 等式

`toolchains/upstream/source/vstd/view.rs:10-29,103-108` 将 Vec 的 View 定义为
返回 `Seq<T>` 的 spec 函数，并让共享引用透明转发 View。
spec 函数满足逻辑等式的同余性，Vec 不需要额外的 `T: PartialEq`、
`Copy`、`Clone` 或 `View` 约束。

| 已有逻辑条件 | 同状态下的推论 |
|---|---|
| `result == vec` | `result@ == vec@` |
| `*result == *old(vec)` | `result@ == old(vec)@` |
| `*final(result) == *final(vec)` | `final(result)@ == final(vec)@` |

`tests/borrowed_clients.rs:11-39` 包含通用同余证明及保留原后置条件的客户端，
对应实际 Verus 输出位于
`proofs/correctness/vec/redundancy-engineer/contract-equivalence.log`。
这里使用的是规范逻辑值相等，不是 Rust `PartialEq` 或物理指针相等。
可变引用的表达式依靠官方 Verus 的借用和状态语义，
不能将其解释为源码中另有一个 `View for &mut A`。

## 不能由同余替代的关系

Vec 与 slice 的 View 是两个不同的函数；其内容关系依赖固定官方
`toolchains/upstream/source/vstd/std_specs/vec.rs:236-261` 的
`as_slice`、`as_mut_slice`、Deref 和 DerefMut 桥接。
同类型值等式的同余本身不证明跨类型内容相等。

初态等式与终态等式分别约束各自状态，不能推出
`final(vec)@ == old(vec)@`。调用者可以合法地经返回引用改变内容；
终态写回必须保留。整个借用区的 Seq 观察也不包含 Vec 的容量、分配器身份
或物理地址，更不等于对所有堆状态的建模。

Rust 实现和 docstring 的精确位置、源码到独立证明入口的有限对应及其尚待
独立判断的部分，见项目的 `issues/source-body-embedding.md`。

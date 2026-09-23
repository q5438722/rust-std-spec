# 当前 specdet 后端不建模返回可变引用

本记录属于 `specdet-limitation`，等待独立复核。它不是 Verus 限制，
也不是 Rust 标准库实现或文档缺陷。尚未公开提交；外部提交需另行授权。

受影响的规范身份是
`<Vec<T,A> as AsMut<Vec<T,A>>>::as_mut` 和
`<Vec<T,A> as AsMut<[T]>>::as_mut`。Rust 1.96 源实现分别位于
`library/alloc/src/vec/mod.rs:4281-4286,4295-4300`，
trait 文档位于 `library/core/src/convert/mod.rs:226-375`。
两者均返回原 `self`，slice 情形经原 `DerefMut` 强制转换。

本实验保留了完整 `T, A: Allocator` 以及接收者关联生命周期。
`specs/vec/borrowed.rs:20-34` 不冻结调用者：初始返回内容等于
`old(vec)@`，借用结束时 `final(result)@ == final(vec)@`；
返回 Vec 的情形现在仅显式保留对应的两条完整值等式，
这两个内容关系由它们推出，详见 [源码对应记录](source-body-embedding.md)。
两个源体正确性文件分别为
`proofs/correctness/vec/as_mut_vec.rs`、`as_mut_slice.rs`。
官方 Verus `0.2026.09.20.aef82ed` 和 Rust 1.98.1 对这两个函数体
在删减前后均各给出 `1 verified, 0 errors`。泛型调用者随后 push 或替换切片元素的
两个补充证明也通过，见 `tests/borrowed_clients.rs`、
`tests/closure-engineer/writeback.stdout`。本轮源体日志位于
`proofs/correctness/vec/closure-engineer/as_mut_vec.stdout.log` 和
`as_mut_slice.stdout.log`。这些结果不替代完整性证明。

实际调用的是
`/home/chentianyu/spec-determinism-tool/.venv/bin/specdet`，版本 0.3.0。
`toolchains/readiness/specdet-cli.txt` 保存了该 Python 环境加载的模块位置；
后端是 `/home/chentianyu/spec-determinism-tool/src/specdet/adapters/verus/backend.py`。
其 `_reject_mutable_return` 在 481–503 行检查返回类型，
`extract` 在 531 行调用这一检查，先于完整性问题的生成。

可以分别用保留的单目标输入重现：

```sh
bash scripts/with_baseline.sh /home/chentianyu/spec-determinism-tool/.venv/bin/specdet analyze \
  proofs/completeness/vec/as_mut_vec.rs --target as_mut \
  --verus "$PWD/toolchains/verus-x86-linux/verus" \
  --out proofs/completeness/vec/mutable-repros/as_mut_vec --json

bash scripts/with_baseline.sh /home/chentianyu/spec-determinism-tool/.venv/bin/specdet analyze \
  proofs/completeness/vec/as_mut_slice.rs --target as_mut \
  --verus "$PWD/toolchains/verus-x86-linux/verus" \
  --out proofs/completeness/vec/mutable-repros/as_mut_slice --json
```

这两个命令在首次生成时均实际运行，原始结果仍分别保存为
`proofs/completeness/vec/as_mut_vec.diagnostic.json` 和
`as_mut_slice.diagnostic.json`，共同的实际输出是：

```text
exit_code = 2
status = failed
verdict = not_evaluated
stage = extract
code = unsupported_mutable_return
message = Mutable-reference return values are not modeled by this backend
baseline = null
proofs = []
```

本轮规范聚合的实际运行
`proofs/completeness/vec/review-runs/engineer-analyze.json` 及真正重新执行的
`proofs/completeness/vec/review-replay-runs/engineer-replay.json`
对这两个目标给出同样诊断。两次总退出码均为 2；两个只读目标各自仍有
不可满足的原始查询和一个通过的完整性义务，不能因总退出码而抹去它们的结果。
单目标 `.rs` 是从当前规范逐字保留的输入声明，不是成功生成的完整性证明；
检查器在生成之前停止，所以没有这两个目标的原生查询。这里没有补造查询或成功记录。

期望是检查原签名及合法 old/final 写回关系的完整性；
观察到的是检查器明确拒绝该返回类型。不能删除写回关系、改成不可变引用、
收窄输入，或把引用转换成缺少内容关系的指针来绕过这一限制。
本轮没有修改 checker、Verus 或 vstd；若需要扩展建模，应作为另行授权的工具工作。

## 等价删减后的本轮重新执行

上面的 `closure-engineer`、`review-runs`、`review-replay-runs` 和两个
`.diagnostic.json` 是原契约的历史结果，全部保留。
本轮不依赖它们判断当前支持情况，而是重新运行两个当前目标：

| 当前记录 | 两个 AsMut 各自的结果 |
|---|---|
| `proofs/completeness/vec/redundancy-engineer/analyze.json` | `failed`、`not_evaluated`、`unsupported_mutable_return` |
| `proofs/completeness/vec/redundancy-engineer/replay.json` | 相同诊断，实际重新执行而非只读旧报告 |

两次均在提取阶段停止，`baseline = null`、`proofs = []`。
完整原始 JSON、stderr、退出码和命令均保存在对应目录；
同目录 `as_mut_vec.rs`、`as_mut_slice.rs` 是本轮声明的精确失败输入，
不是成功的完整性证明。
本轮正确性日志为
`proofs/correctness/vec/redundancy-engineer/as_mut_vec.log`、`as_mut_slice.log`；
终态关系没有删除，合法写回仍通过
`proofs/correctness/vec/redundancy-engineer/contract-equivalence.log` 中的客户端证明。
这两个 API 仍不计入双轨完成，限制尚待独立复核。

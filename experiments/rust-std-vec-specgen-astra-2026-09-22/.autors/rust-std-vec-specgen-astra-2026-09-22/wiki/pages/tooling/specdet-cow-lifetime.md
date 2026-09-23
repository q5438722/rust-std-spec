---
title: specdet 0.3.0 的 Cow 生命周期解析阻塞
description: 固定原生入口的生命周期实参分类错误与 Cow 观察支持边界，以及另行授权工具变化后的恢复条件。
kind: fact
audience: project
source: s-6a17c286/4566f129a548
created: 2026-09-22
confidence: high
---

固定 specdet 0.3.0 对本项目四个返回 `Cow<'a, [T]>` 的直接转换均报告 `Cannot parse source type: "'a"`。独立审阅实际执行 analyze 和 replay --reexecute，确认失败发生在观察构造之前；没有比较式、求解查询或完整性证明。

已定位的原因是 `extractor.py` 将生命周期节点放入 `return_type.type_args`，随后 `type_context.py` 把每项作为类型解析；独立解析对照复现了差别。这不是 Rust 类型检查失败：固定 Verus 下四个原始源体入口均重新编译成功，各验证一个义务。

## 固定原生入口调查已获独立确认

后续独立审阅确认，两种原生观察策略都先经过同一返回类型解析，透明别名展开也回到该路径。辅助解析器能够保留完整注解，但不能替代真实入口。现有 `CowObservation` 的 trait 实现未被扫描器登记，真实后端也未接入任意显式视图映射；修改保存的类型模型不能取得可信转译。

审阅者用固定工具的 Python 编译并实际运行了 `tests/cow-encoding/inspect_native_support.py`，退出码为 0；按 `proofs/completeness/cow/native-support/native-tests.command.json` 的原选择执行了 47 项测试，全部通过，原有 VAddr 解析警告保留。组件结果保留了原生命周期、`T: Clone` 和契约，但没有找到 Cow 的来源视图或已登记实现。这些检查不是新的 Rust 构建或 Cow 完整性证明，也没有实际运行解析修复后的 CLI。

在固定工具已实现的入口和本任务原签名域内，未找到保持 Borrowed/Owned 变体与完整有序序列的可用编码；这一结论不推广到所有 Rust 写法或未来工具。原生入口调查可以结束，四个 Cow 仍未完成双轨证明。项目内 `runtime-review-readiness.json` 已解除旧环境等待，执行能力不替代 API 语义或证明结果。

## 工具变化后的恢复条件

后续工具工作须另行明确授权，范围限于生命周期实参与类型实参的正确分类，以及从既有透明定义建立真实 Cow 变体和完整有序序列观察所必需的识别、转译与测试。当前 Vec 任务不修改或复制修补检查器，也不扩大可信基础；原候选、源体和旧失败记录继续保留。没有新编码或工具变化时，不再盲试别名或重复已知失败的全量重放。

工具变化经独立审阅后，先用原 `from_vec` 绑定运行真实 CLI，确认生成原生比较、查询及非零义务，再恢复四个现有目标的构建、行为与生命周期探针，以及 correctness 和 completeness 的受影响检查与独立重放。保留原签名、合法输入域和完整观察，不得删除生命周期、增加元素 trait 界限或退化为仅内容或长度比较。

独立执行使用 `run_review_command`，需要查询时以同一命令调用 `get_review_command`；输出和 TMPDIR 均转到 `{scratch}`，不写只读输入、不改比较目标。当前及后续独立审阅继续读取项目内 `review-criteria-temporary.txt`，保留本轮规格冗余检查。

证据：
- `issues/specdet-cow-lifetime-type.md`：失败诊断、提取与解析位置及未采用的绕过办法；该文件当时的“尚待独立确认”状态早于本次审阅结论。
- `proofs/completeness/cow/cow-engineer/analyze.json`
- `proofs/completeness/cow/cow-engineer/analysis-runs/20260922T113813Z-1aa027dfd4/`
- 任务 `4566f129a548` 的独立审阅结论：解析对照和双轨重执行确认；仍要求重新规划，不计双轨完成。

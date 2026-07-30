# Private complete-run archives

本目录只保存 private release assets 的 machine-readable metadata；原始归档不进入
Git history。当前七份资产发布在 private pre-release
[`raw-runs-v0.1-20260728`](https://github.com/adinczt-up/TabTS-SkillBench-pre/releases/tag/raw-runs-v0.1-20260728)。

## 当前资产

`index.json` 是唯一入口。每个 entry 指向 `manifests/<run_id>.json`，manifest 固定记录：

- `harness`、`model`、`repeat` 和 benchmark scope；
- release asset 的文件名、byte size 和 SHA-256；
- normalized trace、task metrics（如有）及 per-task results 的归档内路径；
- 可核查的 `trace_records` 和 `task_result_files` 数量；
- 本机原始归档名或拆包来源，不保存本机绝对路径。

当前上传的是已找回的七个完整单轮配置。每份均覆盖 Core400 的三个 conditions，共
`1,200` 条 normalized traces 和 `1,200` 份 `task_result.json`。这里的 `r01` 是
run repeat，不应解释成论文的 `Avg@3`。

## 文件命名

后续资产必须使用：

```text
<benchmark>__<harness>__<model>__rNN__raw.tar.gz
```

所有字段使用 lowercase kebab-case；`__` 只作为字段分隔符。示例：

```text
core400__codex__gpt-5.4-mini__r02__raw.tar.gz
```

`run_id` 与去掉 `.tar.gz` 后的 asset filename 保持一致。不要在文件名中写 provider
credential、endpoint、用户名或本机路径。

## 新增一份运行

1. 确认归档包含完整 normalized trace 和 per-task `task_result.json`。
2. 对 config、manifest 和 filename 做 credential scan；不得上传 `.env`、token、
   API key、cookie、private endpoint credential 或 SSH material。
3. 生成 SHA-256 和 byte size。
4. 复制一个现有 manifest，更新所有 identity、path、count 和 checksum 字段。
5. 将 manifest 加入 `index.json`，先运行 metadata validation：

   ```bash
   python tools/verify_private_run_assets.py
   ```

6. 下载或放置 release assets 后执行 full validation：

   ```bash
   python tools/verify_private_run_assets.py --assets-dir /path/to/assets
   ```

7. 将资产上传到对应 private release；Git commit 只包含 README、index、manifest 和
   validator，不提交大归档。

## 完整性与边界

- Validator 会核对 JSON contract、asset size、SHA-256、gzip/tar 可读性、required
  member，以及 trace/per-task 文件数量。
- `task_metrics_jsonl` 允许为 `null`：某些 legacy snapshot 保留完整 trace 和
  per-task results，但未在归档内物化汇总 metrics。该情况必须在 manifest 中显式记录。
- 原始响应和执行轨迹可能包含 benchmark 数据或模型输出，只能放 private release。
- Evidence-only export 必须排除 per-run `workspace/` 中的 dataset 副本、credential、
  local client state 和与 normalized trace 重复的调试日志；保留 normalized、reports、
  contracts、run metadata、events、prompt、final output 和 `task_result.json`。
- 不修改 legacy archive 的内部目录；统一性由 asset filename、manifest contract 和
  validator 提供，避免重写原始证据。

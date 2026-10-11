# Evidence index

- Current activation contract: `evidence/ecpa-contract-20261011/RESULT.json`
  (`manager-contract-mock-worker-non-performance`).
- Frozen real-NPU cell: `evidence/ISSUE59_ON_DEVICE_SAMPLING_CLOSURE_20260816.md`
  (`historical-real-npu-fresh-process-negative`).

The historical cell establishes scoped exactness and a negative fresh-process
performance result for Qwen2.5-14B. It does not establish a universal negative
for other architectures, workloads, warm-service regimes, or larger batches.
Current mock-worker checks validate activation and lifecycle behavior only and
do not replace or amplify the hardware result.

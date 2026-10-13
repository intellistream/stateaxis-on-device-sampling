# Issue 59 on-device sampling: frozen 3+3 result

This is the complete frozen StateAxis result bundle for the accepted R5
fresh-process cell. It contains the preregistration, six arm runs, raw request
records, activation and lifecycle telemetry, NPU snapshots, environment data,
and cleanup status. `SHA256SUMS` is repo-relative and covers every imported
file except itself.

Qwen2.5-14B exactness passed for all 48 measured requests. Median request
throughput changed from 16.9508 request/s OFF to 14.4669 request/s ON
(-14.654%). Median p95 request latency changed from 63.120 ms to 113.699 ms
(+80.131%), and peak HBM increased by 24 MiB. The repeated cost came from a
76.8--79.7 ms first-use ACLNN setup; steady sampling was about 0.356--0.359 ms.

This is a workload-scoped negative result for fresh-process execution. It does
not rule out warm-service, larger-batch, or other-model benefits.

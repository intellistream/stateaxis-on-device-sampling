# Issue #59 on-device sampling and logits-processor closure

> **Point-in-time report — not current repository status or a task
> assignment.** Current classification and defaults live in
> [`NATIVE_ENGINE_STATUS.md`](../../NATIVE_ENGINE_STATUS.md).

Issue #59 adds an identity-bound, default-off Qwen sampling path without
changing canonical greedy requests. Temperature, top-k, top-p, min-p,
presence/frequency/repetition penalties, deterministic categorical RNG,
logprobs and bounded beam orchestration are carried in the internal native
protocol. The C++ worker applies the processors and selection with ACLNN
operators and returns only the selected token and requested ranked prefix;
full-vocabulary logits are not copied to the host.

Sampling configuration and categorical RNG offset are continuation identity.
A sampled state cannot be attached to a greedy continuation or resumed with a
different configuration. Beam search uses generation-qualified temporary
forks, globally prunes cumulative scores and releases every unretained state.
The all-greedy batch retains the old frame and produces zero sampling timing or
transfer telemetry.

## Correctness and identity

The offline Rust reference and C++ implementation freeze the same SplitMix
draws and cover canonical defaults, invalid fields, penalties, filtering,
categorical selection, ranked logprobs, beam pruning, protocol round trips and
state cleanup. The official local image was
`quay.io/ascend/vllm-ascend:v0.23.0rc1-openeuler`, image ID
`sha256:f4c89c293e076453e9eef9edb5fb9669740dccbd3c48619a9f976d775fc29b81`.
Formal R5 used aggregate identity
`c0781f17cb4cf5fc5547ccef5c2f31341923582de763b7fd0ecf97baaebc9e41`,
the R4 Rust server SHA-256
`7e42e3e85f73d1df0ae2eb4dcd92a1019d2e9a0301044d07de5551e9a6621725`,
worker SHA-256
`ee4da1319d40596e950f455142f343db47df2d22ac27ef0aa4e277d49ad881ab`
and execution-artifact identity
`91fd0ed6dc24678f143188ca3980c2a2362e0c35cd10dfdf30347e1309a48be9`.

R1--R3 are retained negative diagnostic evidence. The official BF16 oracle
gave tokens 11 and 320 equal logits of 16.875, while the real worker's frozen
upstream row produced 16.75 and 16.875. A bounded one-line worker trace proved
that this was a one-ULP upstream BF16 difference, not a sampler sort error.
Final correctness therefore still requires exact selected tokens, exact RNG
offsets and the exact ranked token set; ordering may differ only inside an
official-reference exact-logit tie group. The logprob tolerance is the
analytically frozen `0.125 / 0.8 = 0.15625`, not a tolerance chosen from the
native output. R4 passed correctness, but its performance summary is rejected
because candidate timing included extra beam checks. R5 moved those checks
outside the eight-request measured interval without changing binary, model,
oracle or workload identity.

## Real-NPU result

Dynamic two-snapshot admission selected physical NPU3. Control and candidate
each ran three fresh processes in counterbalanced order. All 48 measured
requests, all categorical decisions, both repeated multistep beam checks per
candidate run and every lifecycle check passed. Candidate telemetry reported
eight sampling calls and 1,376 bytes per run (172 bytes/request); control
reported zero calls and zero bytes.

| metric | control | candidate |
|---|---:|---:|
| runs | 3 | 3 |
| request/s median | 16.9508 | 14.4669 |
| request/s CV | 1.170% | 0.517% |
| request latency p50 median | 57.797 ms | 58.328 ms |
| request latency p95 median | 63.120 ms | 113.699 ms |
| peak HBM | 53,533 MiB | 53,557 MiB |
| device sampling p50 median | disabled | 0.359 ms |
| device sampling p95 median | disabled | 50.927 ms |
| transfer bytes, three runs | 0 | 4,128 |

Candidate request-latency p50 was 0.917% higher, within the frozen 1% median
guard, but fresh-process throughput was 14.654% lower and p95 latency was
80.131% higher. The reason is repeatable first-use ACLNN setup: the first
sampling call in each process took 76.801--79.728 ms, while later calls had
per-run medians of 0.356--0.359 ms and a worst per-run steady p95 of 0.364 ms.
HBM increased by 24 MiB.

The result is **functionally accepted for the narrow explicit Qwen path but
negative for fresh-process cold performance**. Sampling remains default-off.
This does not establish a speedup, a model-generic sampler, or any performance
comparison with vLLM/vLLM-HUST. Cleanup removed only the experiment container;
NPU3 returned to AICore zero and baseline HBM. Raw requests, identities,
per-arm logs, HBM samples, summary and cleanup status are under
`results/issue59-on-device-sampling-20260816-r5-3plus3/`; earlier failed and
superseded attempts remain under their original Issue #59 result directories.

# stateaxis-on-device-sampling

Extension ID: `org.vllm-hust.stateaxis-on-device-sampling`

Experimental, default-off authority for StateAxis categorical and bounded beam
sampling. The Extension Manager/ECPA verifies the research digest and supplies
the only activation payload; without it, StateAxis rejects explicit non-greedy
sampling while preserving the canonical greedy path.

The admitted contract keeps logits processors and token selection on device,
returns only the selected token and a bounded ranked prefix, forbids a full
vocabulary host copy, and binds sampling configuration plus RNG offset into
continuation identity. Beam width is capped at 8 and returned logprobs at 20.

## Evidence boundary

Historical Qwen2.5-14B real-NPU evidence passed exactness over 48 measured
requests, but the fresh-process matched cell regressed throughput by 14.654%
and p95 latency by 80.131%. Steady device sampling took roughly 0.356--0.359 ms;
first use took 76.8--79.7 ms. This is a scoped negative result, not a universal
claim about other models or workloads, so the MOD remains experimental and
performance-unqualified.

Current ECPA evidence covers digest binding, default-off refusal, ON effect
counters, continuation identity, bounded beam cleanup, and Manager launch
composition. See `EVIDENCE.md`.

```bash
python -m pip install -e '.[test]'
pytest -q
VLLM_HUST_EXT_CONFIG=evidence/ecpa-contract-20261011/manager-config.json \
  vllm-hust-ext extension check org.vllm-hust.stateaxis-on-device-sampling
```

Maintainer: Shuhao Zhang (Tony), directly responsible; no advisor is declared.

# stateaxis-on-device-sampling

Extension ID: `org.vllm-hust.stateaxis-on-device-sampling`

On-device categorical/beam sampling, penalties, logprobs and deterministic RNG.

This repository is the independent MOD boundary for StateAxis issues [#59](https://github.com/Qixin-Gaoke/stateaxis/issues/59).
It is deliberately `import_only`, default-off, and cannot be enabled. The split does
not inherit correctness, device, performance, or publication qualification from the
aggregate StateAxis repository.

## Evidence boundary

Status: **negative**.

Correctness passed and steady-state sampling was about 0.36 ms, but fresh-process first-call cost caused a 14.654% throughput regression.

The copied evidence and its SHA-256 are recorded in `PROVENANCE.json`. Negative,
failed, and inconclusive results are retained. Microbenchmarks and component results
must not be restated as online end-to-end gains.

## Install and inspect

```bash
python -m pip install .
vllm-hust-ext extension inspect org.vllm-hust.stateaxis-on-device-sampling
vllm-hust-ext extension check org.vllm-hust.stateaxis-on-device-sampling
```

Discovery does not enable the MOD. A future active revision must extract an
independently reviewable implementation, declare exclusive resources where needed,
and pass exactness, lifecycle, release, failure-recovery, and matched real-online
gates.

## Validate

```bash
python -m pip install -e '.[test]'
pytest -q
```

Maintainer: Shuhao Zhang (Tony), directly responsible; no advisor is declared.

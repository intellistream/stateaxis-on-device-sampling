import hashlib
import json
from pathlib import Path

from vllm_hust_ext.manifest import activation_blocker, load_manifest

import stateaxis_on_device_sampling

ROOT = Path(__file__).resolve().parents[1]


def test_active_manifest_is_hash_bound() -> None:
    path = Path(stateaxis_on_device_sampling.__file__).with_name(
        "vllm-hust-extension-v0.3.json"
    )
    manifest = load_manifest(path)
    assert manifest.bundle_id == stateaxis_on_device_sampling.MOD_ID
    assert manifest.schema_version == "0.3-experimental"
    assert activation_blocker(manifest) is None
    raw = json.loads(path.read_text())
    digest = hashlib.sha256((ROOT / "RESEARCH_MANIFEST.json").read_bytes()).hexdigest()
    binding = raw["activation"]["additional_config"]["stateaxis_mod"]
    assert binding["manifest_sha256"] == digest


def test_contract_is_complete_and_fail_closed() -> None:
    config = stateaxis_on_device_sampling.on_device_sampling()
    assert config.enabled and config.explicit_non_greedy_only
    assert config.categorical and config.beam and config.processors_on_device
    assert config.selected_token_and_ranked_prefix_only
    assert config.forbid_full_vocabulary_host_copy
    assert config.sampling_config_identity_bound and config.rng_offset_identity_bound
    assert config.max_beam_width == 8 and config.max_return_logprobs == 20
    assert config.fail_closed


def test_manifest_owns_exclusive_sampling_resources() -> None:
    raw = json.loads(
        Path(stateaxis_on_device_sampling.__file__)
        .with_name("vllm-hust-extension-v0.3.json")
        .read_text()
    )
    resources = {claim["resource"] for claim in raw["resource_claims"]}
    assert resources == {
        "stateaxis.device.sampling",
        "stateaxis.protocol.sampling-extension",
    }

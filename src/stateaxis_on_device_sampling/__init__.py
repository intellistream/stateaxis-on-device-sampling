"""Pinned StateAxis device-sampling activation contract."""

from dataclasses import dataclass

MOD_ID = "org.vllm-hust.stateaxis-on-device-sampling"


@dataclass(frozen=True, slots=True)
class OnDeviceSamplingConfig:
    enabled: bool = True
    explicit_non_greedy_only: bool = True
    categorical: bool = True
    beam: bool = True
    processors_on_device: bool = True
    selected_token_and_ranked_prefix_only: bool = True
    forbid_full_vocabulary_host_copy: bool = True
    sampling_config_identity_bound: bool = True
    rng_offset_identity_bound: bool = True
    max_beam_width: int = 8
    max_return_logprobs: int = 20
    fail_closed: bool = True

    def __post_init__(self) -> None:
        flags = (
            self.enabled,
            self.explicit_non_greedy_only,
            self.categorical,
            self.beam,
            self.processors_on_device,
            self.selected_token_and_ranked_prefix_only,
            self.forbid_full_vocabulary_host_copy,
            self.sampling_config_identity_bound,
            self.rng_offset_identity_bound,
            self.fail_closed,
        )
        if not all(flags) or self.max_beam_width != 8 or self.max_return_logprobs != 20:
            raise ValueError(
                "on-device-sampling 0.2.0 requires the complete bounded contract"
            )


def on_device_sampling() -> OnDeviceSamplingConfig:
    return OnDeviceSamplingConfig()


__all__ = ["MOD_ID", "OnDeviceSamplingConfig", "on_device_sampling"]

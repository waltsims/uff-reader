import numpy as np
from uff import ReceiveSetup


def test_receive_setup_channel_mapping():
    reference_ch_map = [
        [1, 2, 3, 4],
        [2, 3, 4, 5],
        [3, 4, 5, 6],
    ]
    reference_ch_map_np = np.array(reference_ch_map)

    probe = 0
    time_offset = 0
    sampling_freq = 1e6
    r_setup_1 = ReceiveSetup(probe, time_offset, reference_ch_map, sampling_freq)
    r_setup_2 = ReceiveSetup(probe, time_offset, reference_ch_map_np, sampling_freq)

    assert r_setup_1.channel_mapping == r_setup_2.channel_mapping

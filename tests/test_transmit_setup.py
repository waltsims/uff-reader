import numpy as np
from uff import TransmitSetup


def test_transmit_setup_channel_mapping():
    reference_ch_map = [
        [1, 2, 3, 4],
        [2, 3, 4, 5],
        [3, 4, 5, 6],
    ]
    reference_ch_map_np = np.array(reference_ch_map)

    probe = 0
    transmit_waves = [None, None, None]
    t_setup_1 = TransmitSetup(probe, transmit_waves, reference_ch_map)
    t_setup_2 = TransmitSetup(probe, transmit_waves, reference_ch_map_np)

    assert t_setup_1.channel_mapping == t_setup_2.channel_mapping

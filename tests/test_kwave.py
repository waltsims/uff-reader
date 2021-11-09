from src.uff import *
from datetime import datetime
from uff.utils import *


def load_kwave_output(filepath):
    n_elem = 32
    Nx, Ny, Nz = 128, 128, 16
    elem_width = 1
    elem_spacing = 0
    elem_length = 12
    elem_pitch = elem_width + elem_spacing
    transducer_width = n_elem * elem_width + (n_elem - 1) * elem_spacing
    dt = 1.9481e-08     # in seconds

    elem_x = 1e-3 * elem_pitch * np.linspace(-n_elem // 2, n_elem//2) - (elem_width // 2)
    elem_y = np.zeros(n_elem)
    elem_z = np.zeros(n_elem)

    source_strength = 1e6
    tone_burst_freq = 1.5e6
    tone_burst_cycles = 1

    eg = ElementGeometry(Perimeter([Position(1.0, 1.0, 1.0)]))
    # ir = ImpulseResponse(0, 10, [1, 1, 1], '[m]')

    elements = []
    for elem_idx in range(n_elem):
        T = Translation(float(elem_x[elem_idx]), float(elem_y[elem_idx]), float(elem_z[elem_idx]))
        R = Rotation(0.0, 0.0, 0.0)
        elem_transform = Transform(T, R)
        elem = Element(elem_transform, eg)
        elements.append(elem)



    probe_T = Translation(1.0, float(Ny // 2 - transducer_width // 2), float(Nz // 2 - elem_length // 2))
    probe_R = Rotation(0.0, 0.0, 0.0)
    probe_transform = Transform(probe_T, probe_R)

    probe = Probe(
        number_elements=np.int32(n_elem),
        pitch=1.0 + 1e-8,
        element_height=12.0,
        element_width=1.0,
        element=elements,
        transform=probe_transform,
        element_geometry=[eg]
    )

    dt_string = datetime.now().isoformat()



    transmit_waves = [TransmitWave(
        wave=1,
        time_zero_reference_point=TimeZeroReferencePoint(0.0, 0.0, 0.0)
    )]


    transmit_setup = TransmitSetup(
        probe=1,
        transmit_waves=transmit_waves,
        channel_mapping=np.array([[i + 1 for i in range(n_elem)]]),
        sampling_frequency=1/dt
    )

    receive_setup = ReceiveSetup(
        probe=1,
        time_offset=100 * dt,
        channel_mapping=np.array([[i + 1 for i in range(n_elem)]]),
        sampling_frequency=1/dt
    )

    us_event = Event(
        transmit_setup=transmit_setup,
        receive_setup=receive_setup
    )

    seq = [TimedEvent(
        event=1,
        time_offset=0.0,
    )]

    unique_waves = [Wave(
        origin=Origin(
            position=Position(),
            rotation=Rotation()
        ),
        wave_type=WaveType.PLANE,
        aperture=Aperture(
            origin=Position(),
            fixed_size=0.0,
            f_number=1.0,
            window='rectwin'
        ),
        excitation=1
    )]

    unique_events = [us_event]

    unique_excitations = [Excitation(
        pulse_shape='sinusoidal',
        waveform=np.ones(10),  # => np.delay_mask
        sampling_frequency=1/dt
    )]

    test_dict = load_dict_from_hdf5(filepath)

    data = test_dict['p']
    data_new = np.empty((data.shape[:2]) + (n_elem, ))

    for elem in range(n_elem):
        s_index, e_index = elem * n_elem, (elem + 1) * n_elem
        data_new[:, :, elem] = data[:, :, s_index:e_index].sum()

    assert data_new.shape[-1] == n_elem

    channel_data = ChannelData(
        probes=[probe],
        sound_speed=1540.0,
        local_time=dt_string,
        country_code='DE',
        repetition_rate=(1 / tone_burst_freq),
        authors="Some random guy",
        description="Lorem ipsum si amet ... as always ;)",
        system="Whatever system it is ...",
        data=data_new,
        sequence=seq,
        unique_waves=unique_waves,
        unique_events=unique_events,
        unique_excitations=unique_excitations
    )

    uff = UFF()
    uff.channel_data = channel_data
    version = {
        'major': 0, 'minor': 3, 'patch': 0
    }
    return uff, version

def test_kwave_io():
    # Load kWave output
    data_folder = 'data'
    kwave_output_path = 'kwave_output.h5'
    kwave_uff, version = load_kwave_output(os.path.join(data_folder, kwave_output_path))

    # Save kWave output in .uff format
    kwave_uff.save('kwave_out.uff', version)

    # Load save .uff file
    uff_dict = load_uff_dict('kwave_out.uff')

    # Check version correctness
    version = uff_dict['version']
    assert is_version_compatible(version, (0, 3, 0))

    # Save back loaded .uff file
    uff_loaded = UFF.deserialize(uff_dict)
    uff_loaded.save('kwave_out_duplicate.uff', version)

    # Check equality of both files
    verify_correctness('kwave_out.uff', 'kwave_out_duplicate.uff')

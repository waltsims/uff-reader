import numpy as np
import h5py
from src.uff import *
import inspect

from datetime import datetime

from uff.utils import load_dict_from_hdf5

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

eg = ElementGeometry(Perimeter([Position(1, 1, 1)]))
# ir = ImpulseResponse(0, 10, [1, 1, 1], '[m]')

elements = []
for elem_idx in range(n_elem):
    T = Translation(elem_x[elem_idx], elem_y[elem_idx], elem_z[elem_idx])
    R = Rotation(0, 0, 0)
    elem_transform = Transform(T, R)
    elem = Element(elem_transform, eg)
    elements.append(elem)



probe_T = Translation(1, Ny // 2 - transducer_width // 2, Nz // 2 - elem_length // 2)
probe_R = Rotation(0, 0, 0)
probe_transform = Transform(probe_T, probe_R)

probe = Probe(
    number_elements=32,
    pitch=1,
    element_height=12,
    element_width=1,
    element=elements,
    transform=probe_transform,
    element_geometry=eg
)

dt_string = datetime.now().isoformat()



transmit_waves = [TransmitWave(
    wave=1,
    time_zero_reference_point=TimeZeroReferencePoint(0, 0, 0)
)]


transmit_setup = TransmitSetup(
    probe=1,
    transmit_waves=transmit_waves,
    channel_mapping=[[i for i in range(n_elem)]],
    sampling_frequency=1/dt
)

receive_setup = ReceiveSetup(
    probe=1,
    time_offset=-100 * dt,
    channel_mapping=[[i for i in range(n_elem)]],
    sampling_frequency=1/dt
)

us_event = Event(
    transmit_setup=transmit_setup,
    receive_setup=receive_setup
)

seq = TimedEvent(
    event=us_event,
    time_offset=0,
)

unique_waves = [Wave(
    origin=Origin(
        position=Position(),
        rotation=Rotation()
    ),
    wave_type=WaveType.PLANE,
    aperture=Aperture(
        position=Position(),
        fixed_size=0,
        f_number=1.0,
        window='rectwin'
    ),
    excitation=1
)]

unique_events = [us_event]

unique_excitations = [Excitation(
    pulse_shape='sinusoidal',
    waveform=np.ones(10).tolist(),  # => np.delay_mask
    sampling_frequency=1/dt
)]

filepath = '/private/var/folders/wd/pzn3h1fn37s6gbt12tyj50gw0000gn/T/example_output.h5'
uff_h5 = h5py.File(filepath, 'r')
test_dict = load_dict_from_hdf5(filepath)

channel_data = ChannelData(
    probes=[probe],
    sound_speed=1540,
    local_time=dt_string,
    country_code='DE',
    repetition_rate=(1 / tone_burst_freq),
    authors="Some random guy",
    description="Lorem ipsum si amet ... as always ;)",
    system="Whatever system it is ...",
    data=test_dict['p'],
    sequence=seq,
    unique_waves=unique_waves,
    unique_events=unique_events,
    unique_excitations=unique_excitations
)

uff = UFF()
uff.channel_data = channel_data
uff.save('kwave_out.uff')

print('ok!')

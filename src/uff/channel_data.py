from typing import ClassVar, List, Optional

from attrs import define
from numpy.typing import NDArray

from uff.probe import Probe
from uff.wave import Wave
from uff.event import Event
from uff.timed_event import TimedEvent
from uff.excitation import Excitation


@define
class ChannelData:
    """
    UFF class that contains all the information needed to store and later process channel data.

    Notes:

    The parameter authors identifies the authors of the data; description describes the acquisition scheme,
    motivation and application; local_time and country_code identify the time and place the data were acquired;
    system describes the hardware used in the acquisition; sound_speed contains the reference speed of sound that was
    used in the system to produce the transmitted waves; and repetition_rate is the sequence repetition rate,
    also referred to as framerate in some scenarios.

    The object uff.channel_data contains all the probes used in the acquisition, a list of the unique_waves that have
    been transmitted, and a list of the unique_events that form the sequence. The sequence is specified as an array
    of uff.timed_events, each member containing a reference to an event, and the time_offset since the beginning of
    the current repetition, also known as frame.

    The HDF5 dataset data contains the channel data, organized as a matrix of dimensions (HDF5 notation), :

    [frames x events x channels x samples]

    where samples is the number of temporal samples acquired by the system, channels is the number of active
    channels, unique_events is the number of events in the sequence (not unique events), and repetitions is the
    number of times the described sequence was repeated. Notice that "HDF5 uses C storage conventions, assuming that
    the last listed dimension is the fastest-changing dimension and the first-listed dimension is the slowest
    changing." (https://support.hdfgroup.org/HDF5/doc1.6/UG/12_Dataspaces.html). This means that by accessing the
    data with MATLAB's HDF5 API or Python's h5py the dimension order will be:

    [samples x channels x events x frames]

    This proposal has the limitation of requiring that all event acquisitions have the same number of time samples
    and active channels

    Attributes:
    authors: (Optional) string with the authors of the data
    description: (Optional) string describing the data
    local_time: (Optional) string defining the time the dataset was acquired following ISO 8601
    country_code: (Optional) string defining the country, following ISO 3166-1
    system: (Optional) string defining the system used to acquired the dataset
    repetition_rate: (Optional) Inverse of the time delay between consecutive repetitions of the whole
        sequence, often known as framerate
    data: dataset of dimensions [frames x events x channels x samples] in HDF5
    probes: List of the probes used to transmit/recive the sequence
    unique_waves: List of the unique waves (or beams) used in the sequence
    unique_events: List of the unique transmit/receive events used in the sequence
    unique_excitations: List of the unique excitations used in the sequence
    sequence: List of the times_events that describe the sequence
    sound_speed: Reference sound speed for Tx and Rx events [m/s]
    """

    _str_name: ClassVar = "channel_data"

    # def serialize(self):
    # serialized = super().serialize()

    # data = serialized.pop('data')
    # if data.dtype == complex:
    # serialized['data_imag'] = data.imag
    # serialized['data_real'] = data.real

    # return serialized

    # @classmethod
    # def deserialize(cls: object, data: dict):
    # if 'data_imag' in data:
    # assert 'data_real' in data

    # if 'data_imag' in data and 'data_real' in data:
    # data['data'] = data.pop('data_real') + 1j * data.pop('data_imag')
    # elif 'data_real' in data:
    # data['data'] = data.pop('data_real')
    # else:
    # raise KeyError(f'Channel data not found in {object}')

    # return super().deserialize(data)

    # @staticmethod
    # def deserialize(data: dict):
    #     set_attrs, remaining_attrs = self.assign_primitives(data)
    #     print(set_attrs)
    #     print('=' * 20)
    #     print(remaining_attrs)

    data: NDArray  # could be complex or real
    probes: List[Probe]
    unique_waves: List[Wave]
    unique_events: List[Event]
    unique_excitations: List[Excitation]
    sequence: TimedEvent
    sound_speed: float
    authors: str = ""
    description: str = ""
    local_time: str = ""
    country_code: str = ""
    system: str = ""
    repetition_rate: Optional[float] = None

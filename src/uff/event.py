from typing import ClassVar

from attrs import define

from uff.receive_setup import ReceiveSetup
from uff.transmit_setup import TransmitSetup


@define
class Event:
    """
    UFF class to describe an unique ultrasound event, composed by a single transmit and receive setup

    Attributes
    ==========
    transmit_setup: Description of the transmit event (probe/channels, waves, excitations, etc.).
        If more than one probe is used in reception, this is a list of setups.
    receive_setup: Description of the transmit event (probe/channels, waves, excitations, etc.).
        If more than one probe is used in reception, this is a list of setups.

    """

    # TODO: why is this named "unique_events" and not "event"?
    _str_name: ClassVar = "unique_events"

    transmit_setup: TransmitSetup
    receive_setup: ReceiveSetup

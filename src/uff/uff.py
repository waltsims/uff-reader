import copy
import uff
import h5py


# TODO: best to instatiate with dictionary, since h5py also creates dictionary of data from h5 file...
class UFF:

    # TODO: @classmethod for from file construction
    def __init__(self):
        self.channel_data = None
        self.event = None
        self.timed_event = None
        self.transmit_setup = None
        self.receive_setup = None
        self.transmit_wave = None
        self.excitation = None
        self.wave = None
        self.aperture = None
        self.probe = None
        self.element = None
        self.element_geometry = None
        self.impulse_response = None
        self.perimeter = None
        self.transform = None
        self.rotation = None
        self.translation = None
        self.version = None

    def __copy__(self):
        obj = type(self).__new__(self.__class__)
        obj.__dict__.update(self.__dict__)
        return obj

    def __deepcopy__(self, memodict={}):
        pass

    @staticmethod
    def check_version(uff_h5):
        if uff_h5['version']:
            # read uff version
            file_version = uff_h5['version/major'], uff_h5['version/minor'], uff_h5['version/patch']
            package_version = uff.__version_info__
            if file_version == package_version:
                raise ValueError(
                    f"The file version given ({'.'.join(str(i) for i in file_version)})does not have a matching version. Version must be {uff.__version__}")
        else:
            raise Exception("Not a valid uff file. UFF version field is missing")

    def load(self, data_path):
        # get uff version number
        uff_h5 = h5py.File(data_path)

        self.check_version(uff_h5)

        # Default group for the parent object.
        classname = 'uff.channel_data'

        if classname in uff_h5.keys():
            self.timed_event = 0

            uff_h5[classname]
            # TODO: search subsequent keys and match to objects
            # TODO: if object exists, create it.

            # TODO: should objects be created with dictionaries of agruments.. yes **dict

            pass

    pass


def save(self, data_path, root_name):
    # Saves UFF object to disk

    # TODO: check if file already exists at path

    # TODO: prompt to overwrite previously written file

    # TODO: figure out how to only save channel data for now since that is what the standard defines.

    # TODO: set default "root_name" if one is not passed (name of object) (uff.channel.data)

    # TODO: only read hdf5. screw urls and databases
    # TODO: still check if url is passed.... ugh

    # TODO: write version number

    # TODO: start the (non-recursive) writing process.

    pass

    @property
    def ll_defined(self):
        ll_defined = True;
        if self.ll_open_fun is None:
            ll_defined = False
        return ll_defined

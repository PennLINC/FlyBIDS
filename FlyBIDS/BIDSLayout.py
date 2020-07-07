import flywheel
import pandas as pd
from tqdm import tqdm
from pprint import pprint
from .utils import *


class FlyBIDSLayout:
    """Layout class representing an entire BIDS dataset on Flywheel. Can be used
    for quickly inspecting BIDS data in a project.

    Parameters
    ----------
    project : str
        The label of the project on Flywheel.

    subjects : str or list, optional
        List of subject labels to filter query by.

    subjects : str or list, optional
        List of session labels to filter query by.

    api_key: str
        User's API key on Flywheel

    Examples
    --------
    > from FlyBIDS import FlyBIDSLayout
    > fbl = FlyBIDSLayout('GRMPY_822831', subjects=['11364', '86486'])
    > print(fbl)
    > as_df = fbl.to_df()
    > fbl.get_files(RepetitionTime=3)
    > fbl.get_metadata('EchoTime', filename='sub-014613_ses-002236_task-emotionid_bold.nii.gz'
    """

    __bids_files = []

    def __init__(self, project, subjects=None, sessions=None, api_key=None):
        """Initialize BIDSLayout."""

        print("Building FlyBIDSLayout. This step may take a few moments...")

        if api_key:
            client = flywheel.Client(api_key)
        else:
            client = flywheel.Client()

        if isinstance(subjects, str):
            subjects = [subjects]

        if isinstance(sessions, str):
            sessions = [sessions]

        self.subjects = dict()
        self.sessions = dict()
        project = client.projects.find_first('label={}'.format(project))
        self.project = project.label

        for sub in tqdm(project.subjects(), desc="Parsing Subjects"):

            subject_has_bids = False

            if subjects is not None and sub.label not in subjects:
                continue

            for sess in sub.sessions():

                session_has_bids = False

                if sessions is not None and sess.label not in sessions:
                    continue

                for acq in sess.acquisitions():

                    acq = client.get(acq.id)

                    for f in acq.files:

                        if f.type != 'nifti':
                            continue

                        if (get_nested(f, 'info', 'BIDS', 'Filename')
                            is not None and
                            not get_nested(f, 'info', 'BIDS', 'ignore')
                            ):

                            info_out = f.info
                            info_out['id'] = acq.id
                            info_out['BIDS']['id'] = acq.id

                            self.__bids_files.append(info_out)
                            subject_has_bids = True
                            session_has_bids = True

                if session_has_bids:
                    self.sessions[sess.id] = sess.label

            if subject_has_bids:
                self.subjects[sub.id] = sub.label


    def __repr__(self):
        """Provide a tidy summary of key properties."""
        n_subjects = len(set(self.subjects.keys()))

        n_sessions = len(set(self.sessions.keys()))

        #n_runs = len()

        s = ("FlyBIDS Layout: Project '{}' | Subjects: {} | Sessions: {}"
            .format(self.project, n_subjects, n_sessions))
        return s


    def to_df(self):
        """
        Return a parseable Pandas DataFrame of the BIDS layout
        """

        target_files =self.__bids_files

        dicts = [x['BIDS'] for x in target_files]
        df = pd.DataFrame(dicts)
        df['subject'] = (df['Filename'].apply(
            lambda x: extract(x, '(?<=sub-)[a-zA-Z0-9]*(?=_)'))
            )

        df['session'] = (df['Filename'].apply(
            lambda x: extract(x, '(?<=ses-)[a-zA-Z0-9]*(?=_)'))
            )

        return df.drop('IntendedFor', axis=1, inplace=False).drop_duplicates()

    def get_metadata(self, fields, filename=None, **kwargs):

        """Return a list of metadata properties for a NIfTI file. These metadata
        are those typically found in the NIfTI header.

        Parameters
        ----------
        fields: list or str
            Metadata fields to return.

        filename: list or str, optional
            Exact file(s) to retrieve metadata from.

        kwargs : dict, optional
            Any optional key/values to filter the files. For example
            to return metadata for only subjects with a baseline session,
            use the filter `session='BASELINE'`.

        Returns
        -------
        dict
            Keys are metadata parameters and values are the unique values from the file(s).
        """

        if isinstance(fields, str):
            fields = [fields]

        if isinstance(filename, str):
            filename = [filename]

        available_fields = []
        for y in self.__bids_files:
            available_fields.extend(list(y.keys()))

        available_fields = list(set(available_fields))

        for x in fields:
            if x not in available_fields:
                raise RuntimeError('{} not a valid NIfTI metadata field!'.format(x))

        if filename:

            target_files = []

            for fi in filename:

                for x in self.__bids_files:

                    if get_nested(x, 'BIDS', 'Filename'):
                        target_files.append(x)

            if not target_files:
                raise RuntimeError("{} file not found!".format(filename))

        else:

            target_files = self.__bids_files


        metadata = {}

        for field in fields:

            metadata[field] = []

            for target in target_files:

                metadata[field].append(get_nested(target, field))

            metadata[field] = list(set(metadata[field]))

        return metadata


    def get_files(self, **kwargs):

        """
        Return a list of filenames that match metadata
        """

        output_files = []

        for f in self.__bids_files:

            for key, val in kwargs.items():
                if f.get(key, None) == val:
                    output_files.append(f['BIDS']['Filename'])
                    break

        return output_files

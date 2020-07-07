# FlyBIDS

Quickly build and inspect Flywheel BIDS data.

# Installation

- Development version:
Clone this repo and install the package with `pip`

```
git clone https://github.com/PennLINC/FlyBIDS.git
cd FlyBIDS
pip install -e .
```

- Stable Releases:

Download from Pip:

```
pip install FlyBIDS
```

# Examples
```python
>>> from FlyBIDS.BIDSLayout import FlyBIDSLayout
>>> fbl = FlyBIDSLayout('gear_testing', subjects=['sub-1832999514', 'sub-2216595430'])
>>> print(fbl)
FlyBIDS Layout: Project 'gear_testing' | Subjects: 2 | Sessions: 3
>>> as_df = fbl.to_df()
>>> print(as_df)
template                                           Filename  \
0          anat_file                 sub-1832999514_ses-PNC1_T1w.nii.gz
1          func_file  sub-1832999514_ses-PNC1_task-rest_acq-singleba...
2          anat_file                 sub-1832999514_ses-PNC2_T1w.nii.gz
3   acquisition_file          sub-1832999514_ses-PNC2_task-idemo.nii.gz
:       :       :       :       :         :         :           :
12         NaN   False  5ebee86c4425360a219e6670   NaN  NaN  NaN  2216595430
13        bold   False  5ebee86e4425360a219e6672  rest       NaN  2216595430
14         NaN   False  5ebee8714425360a219e6673   NaN  NaN  NaN  2216595430
15   phasediff   False  5ebee87244253609f99e681a   NaN  NaN       2216595430
>>>
['sub-1832999514_ses-PNC1_task-rest_acq-singleband_bold.nii.gz',
 'sub-1832999514_ses-PNC2_task-idemo.nii.gz',
 'sub-1832999514_ses-PNC2_task-rest_acq-singleband_bold.nii.gz',
 'sub-1832999514_ses-PNC2_task-frac2back.nii.gz',
 'sub-2216595430_ses-PNC1_task-frac2back_run-02.nii.gz',
 'sub-2216595430_ses-PNC1_task-frac2back_run-01.nii.gz',
 'sub-2216595430_ses-PNC1_task-rest_acq-singleband_bold.nii.gz',
 'sub-2216595430_ses-PNC1_task-idemo.nii.gz']

>>> fbl.get_metadata('EchoTime', filename='sub-1832999514_ses-PNC1_task-rest_acq-singleband_bold.nii.gz')
{'EchoTime': [0.032, 0.00351, 0.00269, 0.00527, 0.00667]}
```

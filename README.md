# FlyBIDS

Quickly build and inspect Flywheel BIDS data.

# Examples
```python
> from FlyBIDS.BIDSLayout import FlyBIDSLayout
> fbl = FlyBIDSLayout('GRMPY_822831', subjects=['11364', '86486'])
> print(fbl)
> as_df = fbl.to_df()
> fbl.get_files(RepetitionTime=3)
> fbl.get_metadata('EchoTime', filename='sub-014613_ses-002236_task-emotionid_bold.nii.gz')
```

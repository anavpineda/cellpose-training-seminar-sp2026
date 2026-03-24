Cellpose model trained on Zebrafish neuromasts, specifically the membrane and nucleus channels.


Set up the cellpose environment here: https://github.com/mouseland/cellpose#
  You may get a numpy error, which I fixed using pip install "numpy==1.26.4" jrfij

**Download trained model here: ** https://drive.google.com/file/d/1P4lgsB6mKCQ1hvb_GFW_qbVotln9VUHZ/view?usp=drive_link

**Download a test neuromast here: **
                        ------ Needs GPU to predict ------
  nuclei: https://drive.google.com/file/d/1YCRVzxHqz2ViDSI6CQtFLIZ9K3pPjg_y/view?usp=sharing
  membrane: https://drive.google.com/file/d/1H_-01sid1x58ges-V87-CBAIb1KoytNC/view?usp=sharing
**Run the second cell of /cellpose_model/testing_and_overlap.ipynb
**
         ------ If you'd like to see an expample without running on GPU ------
**Download the manually segmented and model predicted segmentation of that neuromast here:**
  manual: https://drive.google.com/file/d/1XIgEIb1QhNrwwk3tYW9xObO3oWLUYrAr/view?usp=sharing
  predicted: https://drive.google.com/file/d/1kABqekNIkmt5P-otGzrvLdd4uhqIIMFT/view?usp=sharing
**Run the first cell of /cellpose_model/testing_and_overlap.ipynb
**


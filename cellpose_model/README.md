Cellpose Training and Testing

- train_test.py trains the data and tests it to get model losses. Expects a training folder and a testing folder.
- An entire folder can be tested on using the trained mode in testing_folder.py
- You can visualize the process in visualizing_testing_and_overlap.ipynb
  - **Note:** When on MacBook, if you try to use Apple's GPU, there will be a clash between Cellpose and Mac, so you will have to use CPU unless you're on a Windows machine.

- **Download a test neuromast** (requires GPU):
  - nuclei: [link](https://drive.google.com/file/d/1YCRVzxHqz2ViDSI6CQtFLIZ9K3pPjg_y/view?usp=sharing)
  - membrane: [link](https://drive.google.com/file/d/1H_-01sid1x58ges-V87-CBAIb1KoytNC/view?usp=sharing)
- Run the second cell of `/cellpose_model/testing_and_overlap.ipynb`

- **Check overlap of example that's already been run**:
  - manual segmentation: [link](https://drive.google.com/file/d/1XIgEIb1QhNrwwk3tYW9xObO3oWLUYrAr/view?usp=sharing)
  - predicted segmentation: [link](https://drive.google.com/file/d/1AoA3PhYiHSoNXs5bipKtYwzDoBPh0cLK/view?usp=sharing)
- Run the first cell of `/cellpose_model/testing_and_overlap.ipynb`

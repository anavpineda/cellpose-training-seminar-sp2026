"""Train cellpose model using user data; code from https://cellpose.readthedocs.io/en/latest/train.html"""

from cellpose import io, models, train
io.logger_setup()

train_dir = "./Slices/train/"
test_dir  = "./Slices/test/"
save_dir = "./Fine_Tune/"

output = io.load_train_test_data(train_dir, test_dir,
                                mask_filter="_masks", look_one_level_down=False)
images, labels, image_names, test_images, test_labels, image_names_test = output

model = models.CellposeModel(gpu=True)

model_path, train_losses, test_losses = train.train_seg(model.net,
                            train_data=images, train_labels=labels,
                            test_data=test_images, test_labels=test_labels,
                            weight_decay=0.1, learning_rate=1e-5,
                            n_epochs=300,
                            model_name="neuromast_cellpose_trained_model",
                            save_path=save_dir)from cellpose import io, models, train

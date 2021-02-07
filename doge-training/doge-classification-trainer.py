from imageai.Classification.Custom import ClassificationModelTrainer
import tensorflow as tf
import os
# This will disable the gpu
# os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
print("Num GPUs Available: ", len(tf.config.experimental.list_physical_devices('GPU')))
model_trainer = ClassificationModelTrainer()
model_trainer.setModelTypeAsDenseNet121()
model_trainer.setDataDirectory("E:\memelon\doge-training\doge-classification")
model_trainer.trainModel(num_objects=3, num_experiments=10, enhance_data=False, batch_size=16, show_network_summary=True)
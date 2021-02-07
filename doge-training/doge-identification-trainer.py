import glob
import tensorflow as tf
from imageai.Detection.Custom import DetectionModelTrainer
import os

# This will force tensorflow to run on the cpu
# os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

# Limit GPU memory usage
# gpus = tf.config.experimental.list_physical_devices('GPU')
# tf.config.experimental.set_memory_growth(gpus[0], True)
# tf.config.experimental.set_virtual_device_configuration(
#     gpus[0],
#     [tf.config.experimental.VirtualDeviceConfiguration(memory_limit=3000)])

# Limit cpu usage
# tf.config.threading.set_inter_op_parallelism_threads(4)

execution_path = os.getcwd()
data_path = os.path.join(execution_path, "doge-identification/")
models_path = os.path.join(execution_path, "doge-identification/models/")



print("Num GPUs Available: ", len(tf.config.experimental.list_physical_devices('GPU')))
trainer = DetectionModelTrainer()
trainer.setModelTypeAsYOLOv3()
trainer.setDataDirectory(data_directory=data_path)
trainer.setTrainConfig(object_names_array=["doge"], batch_size=16, num_experiments=10)
trainer.trainModel()
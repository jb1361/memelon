import os
import glob
from imageai.Detection.Custom import DetectionModelTrainer

execution_path = os.getcwd()
models_path = os.path.join(execution_path, "doge-identification/models/")
data_path = os.path.join(execution_path, "doge-identification/")
# This will force tensorflow to run on the cpu
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

list_of_files = glob.glob(models_path + "*.h5")
latest_model_path = max(list_of_files, key=os.path.getctime)
path, newest_model = os.path.split(latest_model_path)
print("Newest Model: ", newest_model)

trainer = DetectionModelTrainer()
trainer.setModelTypeAsYOLOv3()
trainer.setDataDirectory(data_directory=data_path)
metrics = trainer.evaluateModel(
    model_path=latest_model_path,
    json_path=os.path.join(execution_path, "doge-identification/json/detection_config.json"),
    iou_threshold=0.5,
    object_threshold=0.3,
    nms_threshold=0.5)


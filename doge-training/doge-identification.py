from imageai.Detection.Custom import CustomObjectDetection
import os
import glob

execution_path = os.getcwd()
models_path = os.path.join(execution_path, "doge-identification/models/")
testing_path = os.path.join(execution_path, "doge-identification/identification-testing/")

# This will force tensorflow to run on the cpu
# os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

# Remove previous results
files_in_results_folder = glob.glob(testing_path + "results/*.*")
for f in files_in_results_folder:
    os.remove(f)

list_of_files = glob.glob(models_path + "*.h5")
latest_model_path = max(list_of_files, key=os.path.getctime)
path, newest_model = os.path.split(latest_model_path)
print("Newest Model: ", newest_model)

detector = CustomObjectDetection()
detector.setModelTypeAsYOLOv3()
# Change newest_model to a specific model if needed
detector.setModelPath(os.path.join(execution_path, os.path.join(models_path + newest_model)))
detector.setJsonPath(os.path.join(execution_path, "doge-identification/json/detection_config.json"))
detector.loadModel()

for x in glob.glob(testing_path + 'images/*.jpg', recursive=True):
    head, tail = os.path.split(x)
    detections = detector.detectObjectsFromImage(input_image=x,
                                                 output_image_path=testing_path + "results/detected-" + tail,
                                                 minimum_percentage_probability=20,
                                                 display_percentage_probability=True,
                                                 display_object_name=True)
    if len(detections) == 0:
        os.remove(testing_path + "results/detected-" + tail)
    for detection in detections:
        print(detection["name"], " : ", detection["percentage_probability"], " : ", detection["box_points"])

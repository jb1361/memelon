from imageai.Classification.Custom import CustomImageClassification
import os

execution_path = os.getcwd()

prediction = CustomImageClassification()
prediction.setModelTypeAsMobileNetV2()
prediction.setModelPath(os.path.join(execution_path, "doges/models/model_ex-001_acc-0.991876.h5"))
prediction.setJsonPath(os.path.join(execution_path, "doges/json/model_class.json"))
prediction.loadModel(num_objects=2)

predictions, probabilities = prediction.classifyImage(
    os.path.join(execution_path, "doges/tesla/resized_203.jpg"), result_count=5)

for eachPrediction, eachProbability in zip(predictions, probabilities):
    print(str(eachPrediction) + " : " + str(eachProbability))
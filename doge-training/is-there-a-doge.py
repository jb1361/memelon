from imageai.Classification.Custom import CustomImageClassification
import os

execution_path = os.getcwd()

prediction = CustomImageClassification()
prediction.setModelTypeAsDenseNet121()
prediction.setModelPath(os.path.join(execution_path, "doges/models/254-254-did-not-detect-doge.h5"))
prediction.setJsonPath(os.path.join(execution_path, "doges/json/model_class.json"))
prediction.loadModel(num_objects=3)

predictions, probabilities = prediction.classifyImage(
    os.path.join(execution_path, "doges/model-test-images/resized_355.jpg"), result_count=5)

for eachPrediction, eachProbability in zip(predictions, probabilities):
    print(str(eachPrediction) + " : " + str(eachProbability))

from roboflow import Roboflow
rf = Roboflow(api_key="IDb2X2qwfoHmjEljfIOb")
project = rf.workspace().project("classificationbee-cat-dog-monkey-yn7fw")
model = project.version(3).model

# infer on a local image
print(model.predict("/Users/berkanyuce/Desktop/cat.jpg", confidence=40, overlap=30).json())

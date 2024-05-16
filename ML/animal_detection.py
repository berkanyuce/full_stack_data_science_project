from roboflow import Roboflow
rf = Roboflow(api_key="***") # API is hidden
project = rf.workspace().project("classificationbee-cat-dog-monkey-yn7fw")
model = project.version(1).model

# infer on a local image
print(model.predict("/Users/berkanyuce/Desktop/monkey.jpg", confidence=40, overlap=30).json())

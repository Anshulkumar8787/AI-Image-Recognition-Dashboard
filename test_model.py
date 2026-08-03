import tensorflow as tf
from tensorflow.keras.applications import MobileNetV2

print("=" * 50)
print("TensorFlow Version:", tf.__version__)
print("=" * 50)

print("Loading MobileNetV2...")

model = MobileNetV2(weights="imagenet")

print("✅ MobileNetV2 loaded successfully!")

print("=" * 50)
print("Model Input Shape:", model.input_shape)
print("Model Output Shape:", model.output_shape)
print("=" * 50)
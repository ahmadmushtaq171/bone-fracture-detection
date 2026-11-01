"""Model loading and inference.

Facts taken from the training notebook:
  * input  : RGB image resized to 224x224, RAW pixel values 0-255
             (the model has a Rescaling(1/127.5, offset=-1) layer built in, so we must NOT rescale again)
  * output : ONE sigmoid unit = P(class index 1) = P("not fractured")
  * classes: ["fractured", "not fractured"]  (alphabetical, from class_names.json)
"""
import json
import os

os.environ.setdefault("KERAS_BACKEND", "tensorflow")
os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "2")

import numpy as np
import streamlit as st
from PIL import Image, ImageOps

import config


@st.cache_data
def class_names():
    with open(config.CLASS_NAMES_PATH) as f:
        return json.load(f)


def _rebuild_architecture():
    """Same architecture as the Colab notebook, used only if load_model() fails."""
    import keras
    from keras import layers

    base = keras.applications.MobileNetV2(
        input_shape=(config.IMG_SIZE, config.IMG_SIZE, 3), include_top=False, weights=None
    )
    return keras.Sequential(
        [
            layers.Input((config.IMG_SIZE, config.IMG_SIZE, 3)),
            layers.RandomFlip("horizontal"),
            layers.RandomRotation(0.08),
            layers.Rescaling(1 / 127.5, offset=-1),
            base,
            layers.GlobalAveragePooling2D(),
            layers.Dropout(0.3),
            layers.Dense(1, activation="sigmoid"),
        ]
    )


@st.cache_resource(show_spinner="Loading the deep-learning model…")
def load_model():
    import keras

    if not config.MODEL_PATH.exists():
        raise FileNotFoundError(f"Model file not found at {config.MODEL_PATH}")
    try:
        return keras.models.load_model(config.MODEL_PATH, compile=False)
    except Exception:
        model = _rebuild_architecture()
        model.load_weights(config.MODEL_PATH)  # Keras 3 can read weights straight from a .keras file
        return model


def preprocess(img: Image.Image) -> np.ndarray:
    import tensorflow as tf

    img = ImageOps.exif_transpose(img).convert("RGB")
    arr = np.asarray(img, dtype="float32")
    # tf.image.resize (bilinear) is exactly what image_dataset_from_directory used during training
    arr = tf.image.resize(arr, (config.IMG_SIZE, config.IMG_SIZE)).numpy()
    return arr[None, ...]


def predict(img: Image.Image) -> dict:
    model = load_model()
    names = class_names()
    p_second = float(model.predict(preprocess(img), verbose=0)[0][0])  # P(names[1]) = P("not fractured")
    probs = {names[0]: 1.0 - p_second, names[1]: p_second}
    idx = int(p_second > 0.5)
    conf = probs[names[idx]]
    return {
        "label": names[idx],
        "is_fractured": names[idx] == "fractured",
        "confidence": conf,
        "p_fractured": probs["fractured"],
        "probs": probs,
        "inconclusive": conf < config.LOW_CONFIDENCE,
    }


def model_status() -> dict:
    exists = config.MODEL_PATH.exists()
    return {"exists": exists, "size_mb": round(config.MODEL_PATH.stat().st_size / 1e6, 1) if exists else 0}

import numpy as np

from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.applications.mobilenet_v2 import (
    preprocess_input,
    decode_predictions
)
from tensorflow.keras.preprocessing import image


# Load pretrained model only once
model = MobileNetV2(weights="imagenet")


# -------------------------------
# Category Mapping
# -------------------------------

CATEGORY_MAP = {

    # DOGS
    "golden_retriever": ("🐶 Dog", "Golden Retriever"),
    "Labrador_retriever": ("🐶 Dog", "Labrador Retriever"),
    "German_shepherd": ("🐶 Dog", "German Shepherd"),
    "malinois": ("🐶 Dog", "Belgian Malinois"),
    "beagle": ("🐶 Dog", "Beagle"),
    "pug": ("🐶 Dog", "Pug"),
    "boxer": ("🐶 Dog", "Boxer"),
    "husky": ("🐶 Dog", "Husky"),

    # CATS
    "tabby": ("🐱 Cat", "Tabby"),
    "Persian_cat": ("🐱 Cat", "Persian Cat"),
    "Siamese_cat": ("🐱 Cat", "Siamese Cat"),
    "Egyptian_cat": ("🐱 Cat", "Egyptian Cat"),
    "tiger_cat": ("🐱 Cat", "Tiger Cat"),

    # APPLES
    "Granny_Smith": ("🍎 Apple", "Granny Smith"),

    # BANANA
    "banana": ("🍌 Banana", "Banana"),

    # ORANGE
    "orange": ("🍊 Orange", "Orange"),

    # POMEGRANATE
    "pomegranate": ("🍎 Pomegranate", "Pomegranate"),

    # CAR
    "sports_car": ("🚗 Car", "Sports Car"),
    "convertible": ("🚗 Car", "Convertible"),
    "jeep": ("🚙 SUV", "Jeep"),
    "minivan": ("🚐 Van", "Minivan"),

    # BOTTLE
    "water_bottle": ("🍼 Bottle", "Water Bottle"),
    "wine_bottle": ("🍾 Bottle", "Wine Bottle"),

    # BIRD
    "parrot": ("🐦 Bird", "Parrot"),
    "macaw": ("🐦 Bird", "Macaw"),
    "peacock": ("🐦 Bird", "Peacock"),

    # LAPTOP
    "laptop": ("💻 Laptop", "Laptop"),

    # PHONE
    "cellular_telephone": ("📱 Mobile Phone", "Phone"),
}


def predict_image(img_path):

    img = image.load_img(
        img_path,
        target_size=(224, 224)
    )

    img_array = image.img_to_array(img)

    img_array = np.expand_dims(
        img_array,
        axis=0
    )

    img_array = preprocess_input(img_array)

    predictions = model.predict(
        img_array,
        verbose=0
    )

    decoded = decode_predictions(
        predictions,
        top=5
    )[0]

    top_prediction = decoded[0]

    imagenet_name = top_prediction[1]

    confidence = round(
        top_prediction[2] * 100,
        2
    )

    if imagenet_name in CATEGORY_MAP:

        category, detail = CATEGORY_MAP[imagenet_name]

    else:

        category = imagenet_name.replace(
            "_",
            " "
        ).title()

        detail = category

    top5 = []

    for item in decoded:

        top5.append({
            "label": item[1].replace("_", " ").title(),
            "confidence": round(item[2] * 100, 2)
        })

    return {

        "category": category,

        "detail": detail,

        "confidence": confidence,

        "top5": top5
    }
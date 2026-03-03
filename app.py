from io import BytesIO

import streamlit as st
from PIL import Image
from transformers import pipeline


CAR_MAKES = [
    "Toyota",
    "Volkswagen",
    "Ford",
    "Honda",
    "Chevrolet",
    "Nissan",
    "Hyundai",
    "Kia",
    "Mercedes-Benz",
    "BMW",
    "Audi",
    "Peugeot",
    "Renault",
    "Skoda",
    "Volvo",
    "Mazda",
    "Subaru",
    "Lexus",
    "Porsche",
    "Ferrari",
]


def build_labels(car_makes: list[str]) -> list[str]:
    return [f"a photo of a {make} car" for make in car_makes]


@st.cache_resource(show_spinner=False)
def load_classifier():
    return pipeline(
        task="zero-shot-image-classification",
        model="openai/clip-vit-base-patch32",
    )


def predict_car_make(image: Image.Image, top_k: int = 5):
    classifier = load_classifier()
    labels = build_labels(CAR_MAKES)
    raw_predictions = classifier(image, candidate_labels=labels)

    top_predictions = []
    for result in raw_predictions[:top_k]:
        prompt_label = result["label"]
        confidence = result["score"]
        clean_label = prompt_label.replace("a photo of a ", "").replace(" car", "")
        top_predictions.append({"make": clean_label, "score": confidence})

    return top_predictions


def main():
    st.set_page_config(page_title="Car Make Guesser", page_icon="🚗", layout="centered")
    st.title("🚗 Car Make Guesser")
    st.write("Upload a car photo and I will guess the make.")

    uploaded_file = st.file_uploader(
        "Upload an image",
        type=["jpg", "jpeg", "png", "webp"],
        help="Best results come from a clear photo where the full car is visible.",
    )

    if uploaded_file is None:
        st.info("Upload a car image to start.")
        return

    image_bytes = uploaded_file.read()
    image = Image.open(BytesIO(image_bytes)).convert("RGB")

    st.image(image, caption="Uploaded image", use_container_width=True)

    if st.button("Guess car make", type="primary"):
        with st.spinner("Analyzing the image..."):
            predictions = predict_car_make(image)

        best_guess = predictions[0]
        st.success(
            f"Best guess: **{best_guess['make']}** ({best_guess['score'] * 100:.1f}% confidence)"
        )

        st.subheader("Top predictions")
        for prediction in predictions:
            st.write(f"- {prediction['make']}: {prediction['score'] * 100:.1f}%")

        st.caption(
            "This is an AI guess and may be wrong, especially with poor image quality or uncommon models."
        )


if __name__ == "__main__":
    main()

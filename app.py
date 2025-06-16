import streamlit as st
from PIL import Image
from rembg import remove
import io

# Title
st.set_page_config(page_title="Car Background Replacer", layout="centered")
st.title("🚗 AI Car Background Replacer")

# Upload car image
uploaded_file = st.file_uploader("Upload a car image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    input_image = Image.open(uploaded_file).convert("RGB")
    st.image(input_image, caption="Original Image", use_column_width=True)

    # Background removal
    with st.spinner("Removing background..."):
        removed = remove(uploaded_file.read())
        car_img = Image.open(io.BytesIO(removed)).convert("RGBA")
        st.image(car_img, caption="Car with background removed", use_column_width=True)

    # Upload background
    bg_file = st.file_uploader("Upload a new background", type=["jpg", "jpeg", "png"])

    if bg_file:
        bg_img = Image.open(bg_file).convert("RGBA").resize(car_img.size)
        final = Image.alpha_composite(bg_img, car_img)
        st.image(final, caption="Final image with new background", use_column_width=True)

        # Download button
        img_bytes = io.BytesIO()
        final.save(img_bytes, format='PNG')
        st.download_button("Download Result", data=img_bytes.getvalue(), file_name="car_with_new_bg.png", mime="image/png")

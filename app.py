import streamlit as st
from PIL import Image
from rembg import remove
from io import BytesIO

# Title
st.set_page_config(page_title="Car Background Replacer", layout="centered")
st.title("🚗 AI Car Background Replacer")

# Upload car image
uploaded_file = st.file_uploader("Upload a car image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    # Read file ONCE and reuse everywhere
    image_bytes = uploaded_file.getvalue()

    try:
        # Show original image
        input_image = Image.open(BytesIO(image_bytes)).convert("RGB")
        st.image(input_image, caption="Original Image", use_container_width=True)

        # Remove background
        with st.spinner("Removing background..."):
            result = remove(image_bytes)
            car_img = Image.open(BytesIO(result)).convert("RGBA")
            st.image(car_img, caption="Car with background removed", use_container_width=True)

        # Upload new background
        bg_file = st.file_uploader("Upload a new background", type=["jpg", "jpeg", "png"])
        if bg_file:
            bg_img = Image.open(bg_file).convert("RGBA").resize(car_img.size)
            final = Image.alpha_composite(bg_img, car_img)
            st.image(final, caption="Final image with new background", use_container_width=True)

            # Download result
            output_buffer = BytesIO()
            final.save(output_buffer, format="PNG")
            st.download_button(
                label="📥 Download Result",
                data=output_buffer.getvalue(),
                file_name="car_with_new_bg.png",
                mime="image/png"
            )
    except Exception as e:
        st.error(f"Something went wrong: {e}")


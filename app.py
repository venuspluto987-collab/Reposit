import streamlit as st
from PIL import Image, ImageFilter
import io

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="AI Image Tool", layout="centered")

st.title("✨ AI Image Tool")
st.caption("Background Change • Image Enhance")

# =========================
# SIDEBAR
# =========================
st.sidebar.title("⚙️ Controls")

uploaded_file = st.sidebar.file_uploader(
    "📤 Upload Image", type=["png", "jpg", "jpeg"]
)

feature = st.sidebar.radio(
    "Choose Feature",
    ["🎨 Background Change", "✨ Enhance Image"]
)

# =========================
# MAIN
# =========================
if uploaded_file:
    image = Image.open(uploaded_file).convert("RGBA")
    image.thumbnail((600, 600))

    st.image(image, caption="Original Image", use_column_width=True)

    # =========================
    # 🎨 BACKGROUND CHANGE
    # =========================
    if feature == "🎨 Background Change":
        st.subheader("🎨 Change Background")

        color = st.color_picker("Pick Background Color", "#00ffaa")

        if st.button("🚀 Apply Background"):
            with st.spinner("Removing background..."):
                from rembg import remove  # lazy load

                cutout = remove(image)
                bg = Image.new("RGBA", cutout.size, color)
                result = Image.alpha_composite(bg, cutout)

            st.image(result, caption="Background Changed", use_column_width=True)

            buf = io.BytesIO()
            result.save(buf, format="PNG")

            st.download_button(
                "📥 Download Image",
                buf.getvalue(),
                "background_changed.png"
            )

    # =========================
    # ✨ IMAGE ENHANCER
    # =========================
    elif feature == "✨ Enhance Image":
        st.subheader("✨ Enhance / Sharpen Image")

        strength = st.slider("Sharpness Level", 1, 5, 2)

        if st.button("🚀 Enhance"):
            with st.spinner("Enhancing image..."):
                result = image

                for _ in range(strength):
                    result = result.filter(ImageFilter.SHARPEN)

            st.image(result, caption="Enhanced Image", use_column_width=True)

            buf = io.BytesIO()
            result.save(buf, format="PNG")

            st.download_button(
                "📥 Download Image",
                buf.getvalue(),
                "enhanced.png"
            )

else:
    st.info("👈 Upload an image from sidebar to start")
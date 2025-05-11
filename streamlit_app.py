import streamlit as st
import os
from zipfile import ZipFile
from moviepy.editor import VideoFileClip, ImageClip, concatenate_videoclips

st.set_page_config(page_title="Travel Reel Builder", layout="centered")

st.title("📸 Travel Highlight Reel Creator")

uploaded_zip = st.file_uploader("Upload a ZIP of your photos/videos", type="zip")

if uploaded_zip:
    with st.spinner("Extracting your files..."):
        os.makedirs("temp_media", exist_ok=True)
        with ZipFile(uploaded_zip, 'r') as zip_ref:
            zip_ref.extractall("temp_media")

        media_files = sorted([
            os.path.join("temp_media", f)
            for f in os.listdir("temp_media")
            if f.lower().endswith(('.jpg', '.jpeg', '.png', '.mp4'))
        ])

    if media_files:
        st.success(f"Found {len(media_files)} media files!")

        if st.button("🎬 Build Highlight Reel"):
            clips = []
            total_duration = 0
            for file in media_files:
                try:
                    if file.lower().endswith(('.jpg', '.jpeg', '.png')):
                        clip = ImageClip(file).set_duration(2)
                    else:
                        clip = VideoFileClip(file)
                        if clip.duration > 10:
                            clip = clip.subclip(0, 10)
                    total_duration += clip.duration
                    if total_duration > 120:
                        break
                    clips.append(clip)
                except Exception as e:
                    st.error(f"Error with {file}: {e}")

            if clips:
                final = concatenate_videoclips(clips, method="compose")
                output_path = "travel_reel.mp4"
                final.write_videofile(output_path, fps=24)
                st.video(output_path)
                with open(output_path, "rb") as f:
                    st.download_button("⬇️ Download Reel", f, file_name="travel_reel.mp4")
            else:
                st.error("No usable media files found.")

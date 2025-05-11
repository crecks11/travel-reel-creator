import os
from moviepy.editor import ImageClip, VideoFileClip, concatenate_videoclips

def build_highlight_reel(media_files, output_path, max_video_length=120, image_duration=2):
    clips = []
    total_duration = 0

    for path in media_files:
        try:
            if path.lower().endswith(('.jpg', '.jpeg', '.png')):
                clip = ImageClip(path).set_duration(image_duration)
            elif path.lower().endswith('.mp4'):
                clip = VideoFileClip(path)
                if clip.duration > 10:
                    clip = clip.subclip(0, 10)
            else:
                continue

            total_duration += clip.duration
            if total_duration > max_video_length:
                print("⚠️  Stopping at 2 min limit.")
                break

            clips.append(clip)

        except Exception as e:
            print(f"❌ Error with {path}: {e}")

    if not clips:
        return None

    final = concatenate_videoclips(clips, method="compose")
    final.write_videofile(output_path, fps=24)
    return output_path

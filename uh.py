import cv2
import subprocess
import os

# Input video path
input_path = "./static/videos/zipping_rollout_1080x1080_2x-9231.mp4"

# Automatically generate reshaped and web-playable paths
base_name, ext = os.path.splitext(input_path)
reshaped_path = f"{base_name}_reshaped.avi"
web_path = f"{base_name}_1080x720_web.mp4"

# Open the input video
cap = cv2.VideoCapture(input_path)
if not cap.isOpened():
    raise Exception("Error opening video file")

# Get original video properties
orig_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
orig_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS)
fourcc = cv2.VideoWriter_fourcc(*'XVID')  # intermediate codec

# Desired output size
new_width = 1080
new_height = 720

# Create VideoWriter for intermediate video
out = cv2.VideoWriter(reshaped_path, fourcc, fps, (new_width, new_height))

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Resize (reshape) frame to 1080x720
    reshaped_frame = cv2.resize(frame, (new_width, new_height))
    
    # Write frame
    out.write(reshaped_frame)

# Release resources
cap.release()
out.release()
cv2.destroyAllWindows()

print(f"Reshaped video saved to {reshaped_path}")

# --- Call FFmpeg to encode for web playback ---
ffmpeg_cmd = [
    "ffmpeg",
    "-y",  # overwrite if exists
    "-i", reshaped_path,
    "-c:v", "libx264",
    "-pix_fmt", "yuv420p",
    "-preset", "fast",
    "-crf", "23",
    "-c:a", "aac",
    web_path
]

subprocess.run(ffmpeg_cmd, check=True)
print(f"Web-playable video saved to {web_path}")

# Optional: remove intermediate file
os.remove(reshaped_path)

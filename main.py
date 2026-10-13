import cv2
import numpy as np
import os
import random

# ============================================
# MAA DURGA JI - 50 SECOND DRAWING ANIMATION
# Original Style: Random Square Reveal
# ============================================

INPUT_FILE = "maa_durga_reference.jpeg"

OUTPUT_IMAGE = "Maa_Durga_Final.png"
OUTPUT_VIDEO = "Maa_Durga_Drawing_50s.mp4"

DURATION = 50
FPS = 30

VIDEO_WIDTH = 720
VIDEO_HEIGHT = 1280

WINDOW_NAME = "Maa Durga Ji - 50 Second Drawing"


def main():

    # 1. Load the reference image
    if not os.path.isfile(INPUT_FILE):
        print(f"ERROR: Image not found: {INPUT_FILE}")
        print("Keep the image in the same folder as main.py.")
        return

    original = cv2.imread(INPUT_FILE)

    if original is None:
        print("ERROR: Unable to read the image.")
        return

    print("Preparing Maa Durga Ji artwork...")

    # 2. Fit the complete image without cropping
    h, w = original.shape[:2]

    scale = min(
        VIDEO_WIDTH / w,
        VIDEO_HEIGHT / h
    )

    new_w = int(w * scale)
    new_h = int(h * scale)

    resized = cv2.resize(
        original,
        (new_w, new_h),
        interpolation=cv2.INTER_LANCZOS4
    )

    artwork = np.full(
        (VIDEO_HEIGHT, VIDEO_WIDTH, 3),
        255,
        dtype=np.uint8
    )

    x_offset = (VIDEO_WIDTH - new_w) // 2
    y_offset = (VIDEO_HEIGHT - new_h) // 2

    artwork[
        y_offset:y_offset + new_h,
        x_offset:x_offset + new_w
    ] = resized

    # Save complete image
    cv2.imwrite(OUTPUT_IMAGE, artwork)

    # 3. Create random square reveal order
    tile_width = 12
    tile_height = 12

    tiles = []

    for y in range(0, VIDEO_HEIGHT, tile_height):
        for x in range(0, VIDEO_WIDTH, tile_width):
            tiles.append((x, y))

    random.Random(42).shuffle(tiles)

    total_tiles = len(tiles)
    total_frames = DURATION * FPS

    # 4. Create MP4 video
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")

    video = cv2.VideoWriter(
        OUTPUT_VIDEO,
        fourcc,
        FPS,
        (VIDEO_WIDTH, VIDEO_HEIGHT)
    )

    if not video.isOpened():
        print("ERROR: Could not create video.")
        return

    # White starting canvas
    canvas = np.full_like(artwork, 255)

    # 5. Display the complete animation in a manageable window
    cv2.namedWindow(
        WINDOW_NAME,
        cv2.WINDOW_NORMAL
    )

    cv2.resizeWindow(
        WINDOW_NAME,
        540,
        760
    )

    print("Animation started!")
    print("Duration: 50 seconds")
    print("Press ESC to stop.")

    tile_index = 0

    try:

        # 6. Animate squares progressively
        for frame_number in range(total_frames):

            target_tiles = int(
                ((frame_number + 1) / total_frames)
                * total_tiles
            )

            while tile_index < target_tiles:

                x, y = tiles[tile_index]

                x2 = min(
                    x + tile_width,
                    VIDEO_WIDTH
                )

                y2 = min(
                    y + tile_height,
                    VIDEO_HEIGHT
                )

                # Reveal original image pixels
                canvas[y:y2, x:x2] = artwork[y:y2, x:x2]

                tile_index += 1

            # Show progress in the window title
            progress = int(
                (frame_number + 1) / total_frames * 100
            )

            cv2.setWindowTitle(
                WINDOW_NAME,
                f"Maa Durga Ji Drawing - {progress}%"
            )

            # Save clean animation frame
            video.write(canvas)

            # Display the complete canvas scaled to the window
            cv2.imshow(
                WINDOW_NAME,
                canvas
            )

            key = cv2.waitKey(1) & 0xFF

            if key == 27:
                print("Animation stopped.")
                break

            if frame_number % FPS == 0:
                print(
                    f"Progress: {progress}% | "
                    f"{frame_number // FPS}/{DURATION} seconds"
                )

    finally:
        video.release()
        cv2.destroyAllWindows()

    print("\n====================================")
    print("Maa Durga Ji animation saved!")
    print("====================================")
    print("Final PNG:", os.path.abspath(OUTPUT_IMAGE))
    print("Drawing video:", os.path.abspath(OUTPUT_VIDEO))
    print("====================================")


if __name__ == "__main__":
    main()
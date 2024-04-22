import cv2
import numpy as np
import random

def compute_SAD(block1, block2):
    return np.sum(np.abs(block1 - block2))

def block_matching(frame1, frame2, block_size, search_radius):
    height, width = frame1.shape
    motion_vectors = np.zeros(((height // block_size), (width // block_size), 2))

    for i in range(0, height, block_size):
        for j in range(0, width, block_size):
            reference_block = frame1[i:i + block_size, j:j + block_size]
            min_SAD = float('inf')
            best_match = (0, 0)

            for dx in range(-search_radius, search_radius + 1):
                for dy in range(-search_radius, search_radius + 1):
                    x_offset = i + dx
                    y_offset = j + dy

                    if 0 <= x_offset <= height - block_size and 0 <= y_offset <= width - block_size:
                        candidate_block = frame2[x_offset:x_offset + block_size, y_offset:y_offset + block_size]
                        sad = compute_SAD(reference_block, candidate_block)
                        if sad < min_SAD:
                            min_SAD = sad
                            best_match = (dx, dy)

            motion_vectors[i // block_size, j // block_size] = best_match

    return motion_vectors

def extract_frames(video_path, random_frame):
    cap = cv2.VideoCapture(video_path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    # Ensure the random frame is such that a next frame exists
    if random_frame >= total_frames - 1:
        random_frame = total_frames - 2

    cap.set(cv2.CAP_PROP_POS_FRAMES, random_frame)
    ret, frame1 = cap.read()
    ret, frame2 = cap.read()
    cap.release()

    if ret:
        frame1_gray = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
        frame2_gray = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
        return frame1_gray, frame2_gray
    else:
        raise Exception("Failed to extract frames")

# Load video and choose a random frame
video_path = 'output.avi'
cap = cv2.VideoCapture(video_path)
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
random_frame = random.randint(0, total_frames - 2)  # Ensuring there is a next frame
frame1, frame2 = extract_frames(video_path, random_frame)

# Set parameters
block_size = 8
search_radius = 4

# Compute motion vectors
motion_vectors = block_matching(frame1, frame2, block_size, search_radius)
print("Motion Vectors:")
print(motion_vectors)
import cv2
import numpy as np
import random
import matplotlib.pyplot as plt

def compute_SAD(block1, block2):
    return np.sum(np.abs(block1 - block2))

def block_matching(frame1, frame2, block_size, search_radius):
    height, width = frame1.shape
    motion_vectors = np.zeros(((height // block_size), (width // block_size), 2))

    for i in range(0, height, block_size):
        for j in range(0, width, block_size):
            reference_block = frame1[i:i + block_size, j:j + block_size]
            min_SAD = float('inf')
            best_match = (0, 0)

            for dx in range(-search_radius, search_radius + 1):
                for dy in range(-search_radius, search_radius + 1):
                    x_offset = i + dx
                    y_offset = j + dy

                    if 0 <= x_offset <= height - block_size and 0 <= y_offset <= width - block_size:
                        candidate_block = frame2[x_offset:x_offset + block_size, y_offset:y_offset + block_size]
                        sad = compute_SAD(reference_block, candidate_block)
                        if sad < min_SAD:
                            min_SAD = sad
                            best_match = (dx, dy)

            motion_vectors[i // block_size, j // block_size] = best_match

    return motion_vectors

def extract_frames(video_path, random_frame):
    cap = cv2.VideoCapture(video_path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    if random_frame >= total_frames - 1:
        random_frame = total_frames - 2

    cap.set(cv2.CAP_PROP_POS_FRAMES, random_frame)
    ret, frame1 = cap.read()
    ret, frame2 = cap.read()
    cap.release()

    if ret:
        frame1_gray = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
        frame2_gray = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
        return frame1_gray, frame2_gray
    else:
        raise Exception("Failed to extract frames")

# Load video and choose a random frame
video_path = 'output.avi'
cap = cv2.VideoCapture(video_path)
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
random_frame = random.randint(0, total_frames - 2)
frame1, frame2 = extract_frames(video_path, random_frame)

# Set parameters
block_size = 8
search_radius = 4

# Compute motion vectors
motion_vectors = block_matching(frame1, frame2, block_size, search_radius)

# Plotting the results
fig, axs = plt.subplots(1, 2, figsize=(10, 5))
axs[0].imshow(frame1, cmap='gray')
axs[0].set_title('Frame 1')
axs[1].imshow(frame2, cmap='gray')
axs[1].set_title('Frame 2')

# Plot motion vectors on Frame 1
for i in range(motion_vectors.shape[0]):
    for j in range(motion_vectors.shape[1]):
        start_point = (j * block_size + block_size // 2, i * block_size + block_size // 2)
        end_point = (start_point[0] + int(motion_vectors[i, j, 0]), start_point[1] + int(motion_vectors[i, j, 1]))
        axs[0].arrow(start_point[0], start_point[1], motion_vectors[i, j, 0], motion_vectors[i, j, 1], head_width=3, head_length=5, fc='red', ec='red')

plt.show()

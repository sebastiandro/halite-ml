import cv2
import numpy as np

for i in range(2, 400):
    d = np.load(f"./game_play/{i}.npy")
    cv2.imshow("", cv2.resize(d, (0, 0), fx=30, fy=30))
    cv2.waitKey(25)

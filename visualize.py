import cv2
import pandas as pd


def plot_calibration_point(image, u, v, point_id="0", radius=10, color=(0, 188, 255)):
    # (u, v)に円をかく
    img = cv2.circle(image, (u, v), radius, color=color, thickness=3)
    img = cv2.putText(img, point_id, (u + 20, v), cv2.FONT_HERSHEY_SIMPLEX, 5, color, 5)
    return img


def plot_calibration_points(read_image_path: str, write_image_path: str, points: pd.DataFrame, radius=10, color=(0, 188, 255)):
    img = cv2.imread(read_image_path)
    for row in points.itertuples():
        img = plot_calibration_point(img, row[1], row[2], str(row[0] + 1), radius, color)

    cv2.imwrite(write_image_path, img)


if __name__ == "__main__":
    # img = cv2.imread("images/1.JPG")
    # img = plot_calibration_point(img, 512, 512, radius=10)
    # cv2.imwrite("images/1_plotted.JPG", img)

    points = pd.read_csv("points.csv")
    plot_calibration_points("images/1.JPG", "images/1_plotted.JPG", points)


import cv2
import pandas as pd


def plot_calibration_point(image, u, v, point_id="0", radius=10, color=(0, 188, 255)):
    # (u, v)に円をかく
    img = cv2.circle(image, (u, v), radius, color=color, thickness=3)
    textsize = cv2.getTextSize(point_id, cv2.FONT_HERSHEY_SIMPLEX, 5, 5)[0]
    # print("text row: {}, text col: {}".format(textsize[0], textsize[1]))

    if u + 20 + textsize[0] > img.shape[1] or v - textsize[1] < 0:
        # 画像外に数字が飛び出る場合
        # print("{}: Over".format(point_id))
        if u - 80 - textsize[1] < 0:
            # 右下にプロット
            img = cv2.putText(img, point_id, (u + 20, v + textsize[0] - 70), cv2.FONT_HERSHEY_SIMPLEX, 5, color, 5)
        elif v + textsize[0] - 30 > img.shape[0]:
            # 左上にプロット
            img = cv2.putText(img, point_id, (u - 80 - textsize[1], v), cv2.FONT_HERSHEY_SIMPLEX, 5, color, 5)
        else:
            # 左下にプロット
            img = cv2.putText(img, point_id, (u - 80 - textsize[1], v + textsize[0] - 30), cv2.FONT_HERSHEY_SIMPLEX, 5, color, 5)

    else:
        # 基本的には点の右上に数字をプロット
        img = cv2.putText(img, point_id, (u + 20, v), cv2.FONT_HERSHEY_SIMPLEX, 5, color, 5)
    return img


def plot_calibration_points(read_image_path: str, write_image_path: str, points: pd.DataFrame, radius=10, color=(0, 188, 255)):
    img = cv2.imread(read_image_path)
    for row in points.itertuples():
        img = plot_calibration_point(img, row[1], row[2], str(row[0] + 1), radius, color)

    cv2.imwrite(write_image_path, img)


if __name__ == "__main__":
    # img = cv2.imread("data/1.JPG")
    # img = plot_calibration_point(img, 512, 512, radius=10)
    # cv2.imwrite("data/1_plotted.JPG", img)

    points = pd.read_csv("points_3.csv")
    plot_calibration_points("data/3.JPG", "data/3_plotted.JPG", points)


import cv2
import seaborn as sns
import pandas as pd


def plot_calibration_point(image, u, v, point_id="0", radius=10, color=(156, 157, 154)):
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
            img = cv2.putText(img, point_id, (u - 80 - textsize[1], v + textsize[0] - 30), cv2.FONT_HERSHEY_SIMPLEX, 5,
                              color, 5)

    else:
        # 基本的には点の右上に数字をプロット
        img = cv2.putText(img, point_id, (u + 20, v), cv2.FONT_HERSHEY_SIMPLEX, 5, color, 5)
    return img


def plot_calibration_points(read_image_path: str, write_image_path: str, points: pd.DataFrame, radius=10,
                            color=(242, 236, 167)):
    img = cv2.imread(read_image_path)
    for row in points.itertuples():
        img = plot_calibration_point(img, row[1], row[2], str(row[0] + 1), radius, color)

    cv2.imwrite(write_image_path, img)


# 3D 可視化に用いる
class SeabornColorPalette:
    palette_names = [
        "viridis",
        "plasma",
        "inferno",
        "magma",

        "Greys",
        "Purples",
        "Blues",
        "Greens",
        "Oranges",
        "Reds",
        "YlOrBr",
        "YlOrRd",
        "OrRd",
        "PuRd",
        "RdPu",
        "BuPu",
        "GnBu",
        "PuBu",
        "YlGnBu",
        "PuBuGn",
        "BuGn",
        "YlGn",

        "binary",
        "gist_yarg",
        "gist_gray",
        "gray",
        "bone",
        "pink",
        "spring",
        "summer",
        "autumn",
        "winter",
        "cool",
        "Wistia",
        "hot",
        "afmhot",
        "gist_heat",
        "copper",

        "PiYG",
        "PRGn",
        "BrBG",
        "PuOr",
        "RdGy",
        "RdBu",
        "RdYlBu",
        "RdYlGn",
        "Spectral",
        "coolwarm",
        "bwr",
        "seismic",

        "Pastel1",
        "Pastel2",
        "Paired",
        "Accent",
        "Dark2",
        "Set1",
        "Set2",
        "Set3",
        "tab10",
        "tab20",
        "tab20b",
        "tab20c",

        "flag",
        "prism",
        "ocean",
        "gist_earth",
        "terrain",
        "gist_stern",
        "gnuplot",
        "gnuplot2",
        "CMRmap",
        "cubehelix",
        "brg",
        "hsv",
        "gist_rainbow",
        "rainbow",
        # "jet",
        "nipy_spectral",
        "gist_ncar"
    ]


    @classmethod
    def to_plotly_rgb(cls, colorpalette, num_color):
        palette = sns.color_palette(colorpalette, num_color)
        rgb = ['rgb({},{},{})'.format(*[int(x * 256) for x in rgb])
               for rgb in palette]
        return rgb


if __name__ == "__main__":
    points = pd.read_csv("points.csv")
    plot_calibration_points("sample/IMG_4047.JPG", "sample/IMG_4047_plotted.JPG", points)

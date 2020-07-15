import numpy as np
import pandas as pd


class Camera:
    def __init__(self, point_for_calibration: pd.DataFrame):
        """
        Camera:
            Class to calibrate the camera from the image.

        :argument
            point_for_calibration: DataFrame, pairs of point on the image and 3D point, for the calibration.
            Example:
                |  u  |  v  |  X  |  Y  |  Z  |
                | 128 | 324 | 3.0 | 5.0 | 0.0 |
        """
        self.point_for_calibration = point_for_calibration
        self.num_points = len(self.point_for_calibration)

        # 校正点が満たす連立1次方程式の行列とベクトル
        self.array = None
        self.vector = None
        # 透視投影行列
        self.perspective_projection_matrix = None

    # 行列Aとベクトルbを生成
    def __generate_array_and_vector(self):
        if self.array is None or self.vector is None:
            array_ = []
            vector_ = []
            for row in self.point_for_calibration.itertuples():
                # 画像上の点u, vと3次元座標x, y, zを取得
                u = row[1]
                v = row[2]
                x = row[3]
                y = row[4]
                z = row[5]

                # 2つの式を立てる
                array_row_1 = [x, y, z, 1, 0, 0, 0, 0, -1 * u * x, -1 * u * y, -1 * u * z]
                array_row_2 = [0, 0, 0, 0, x, y, z, 1, -1 * v * x, -1 * v * y, -1 * v * z]

                array_ += [array_row_1]
                array_ += [array_row_2]

                # ベクトルb
                vector_ += [u]
                vector_ += [v]

            array = np.array(array_, np.float64)
            vector = np.array(vector_, np.float64)

            self.array = array
            self.vector = vector

    # カメラの校正
    def calibrate(self):
        # 行列Aとベクトルbを生成する
        self.__generate_array_and_vector()
        # A^T Aを求める
        try:
            a_t_a = np.dot(self.array.T, self.array)
            print("A^T*A")
            print(a_t_a)
        except ValueError:
            print("ValueError A^T*A")

        # A^T bを求める
        try:
            a_t_b = np.dot(self.array.T, self.vector)
            print("A^T*b")
            print(a_t_b)
        except ValueError:
            print("ValueError A^T*b")

        # 連立1次方程式を解く
        x = np.linalg.solve(a_t_a, a_t_b)
        print(x)

        # 透視投影行列
        p = [[x[0], x[1], x[2], x[3]],
             [x[4], x[5], x[6], x[7]],
             [x[8], x[9], x[10], 1]]
        self.perspective_projection_matrix = np.array(p, np.float64)


if __name__ == "__main__":
    points = pd.read_csv("points_1.csv")
    c1 = Camera(points)
    c1.calibrate()
    print(c1.perspective_projection_matrix)

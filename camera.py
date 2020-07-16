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
        self.__flatten_p = None

        # 再投影点
        self.points_of_reprojection = None

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
    def calibrate(self, verbose=0):
        print("Calibrate camera...")
        # 行列Aとベクトルbを生成する
        self.__generate_array_and_vector()
        if verbose > 0:
            print("A = ")
            print(self.array)
            print("b = ")
            print(self.vector)

        # A^T Aを求める
        try:
            a_t_a = np.dot(self.array.T, self.array)
            if verbose > 0:
                print("A^T*A = ")
                print(a_t_a)
        except ValueError:
            print("ValueError A^T*A")

        # A^T bを求める
        try:
            a_t_b = np.dot(self.array.T, self.vector)
            if verbose > 0:
                print("A^T*b = ")
                print(a_t_b)
        except ValueError:
            print("ValueError A^T*b")

        # 連立1次方程式を解く
        x = np.linalg.solve(a_t_a, a_t_b)
        if verbose > 0:
            print("x = ")
            print(x)

        # 透視投影行列
        p = [[x[0], x[1], x[2], x[3]],
             [x[4], x[5], x[6], x[7]],
             [x[8], x[9], x[10], 1]]
        self.perspective_projection_matrix = np.array(p, np.float64)
        # 透視投影行列(flatten)
        self.__flatten_p = x

        print("Perspective Projection Matrix")
        print(self.perspective_projection_matrix)

    # 3D -> 2D
    def perspective_project(self, x, y, z):
        if self.__flatten_p is None or self.perspective_projection_matrix is None:
            print("Not calibrated.")
            return

        # 透視投影行列(flatten)
        p = self.__flatten_p

        lambda_ = p[8] * x + p[9] * y + p[10] * z + 1.0
        u = (p[0] * x + p[1] * y + p[2] * z + p[3]) / lambda_
        v = (p[4] * x + p[5] * y + p[6] * z + p[7]) / lambda_
        return u, v

    # 校正点を再投影する
    def re_project(self):
        if self.__flatten_p is None or self.perspective_projection_matrix is None:
            print("Not calibrated.")
            return

        reprojected_u = []
        reprojected_v = []
        # 再投影する
        for row in self.point_for_calibration.itertuples():
            u_, v_ = self.perspective_project(row[3], row[4], row[5])
            reprojected_u += [u_]
            reprojected_v += [v_]

        reprojected = pd.DataFrame({"u": reprojected_u,
                                    "v": reprojected_v,
                                    "x": self.point_for_calibration["x"],
                                    "y": self.point_for_calibration["y"],
                                    "z": self.point_for_calibration["z"]})

        # 画像点をintにキャストする
        reprojected["u"] = reprojected["u"].astype(int)
        reprojected["v"] = reprojected["v"].astype(int)

        self.points_of_reprojection = reprojected

    # 再投影誤差
    def re_projection_error(self):
        errors = []
        for row_true, row_pred in zip(self.point_for_calibration.itertuples(), self.points_of_reprojection.itertuples()):
            # 校正点と投影点の距離を求める
            error = np.sqrt((row_true[1] - row_pred[1]) ** 2 + (row_true[2] - row_pred[2]) ** 2)
            errors += [error]
        
        return np.average(errors)

    # sklearn-like
    def fit(self, verbose=0):
        self.calibrate(verbose)

    def predict(self, x, y, z):
        self.predict(x, y, z)


if __name__ == "__main__":
    points = pd.read_csv("points/points_1.csv")
    c1 = Camera(points)
    c1.calibrate()

    c1.re_project()
    print("Re-projection Error = ", c1.re_projection_error())

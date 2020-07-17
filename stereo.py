import numpy as np
import pandas as pd
from camera import Camera


class Stereo:
    def __init__(self, camera1: Camera, camera2: Camera, points: pd.DataFrame):
        """
            Stereo:
                Class to .
            :argument
                camera1: camera.Camera, the calibrated camera with the image.
                camera2: camera.Camera, the calibrated camera with the image (different image than camera1).
                points: corresponding image points on camera1 and camera2.
                Example:
                    |  u1  |  v1  |  u2  |  v2  |
                    | 128  | 324  | 256  |  398 |
            """
        self.camera1 = camera1
        self.camera2 = camera2
        self.points = points

        self.points_of_objects = None

    # 行列Aとベクトルbを生成 (対応点ごと)
    def __generate_array_and_vector(self, u1, v1, u2, v2):
        array_ = []
        vector_ = []

        p1 = np.ravel(self.camera1.perspective_projection_matrix)
        p2 = np.ravel(self.camera2.perspective_projection_matrix)

        # camera1に対する式
        array_ += [[p1[0] - u1 * p1[8], p1[1] - u1 * p1[9], p1[2] - u1 * p1[10]]]
        array_ += [[p1[4] - v1 * p1[8], p1[5] - v1 * p1[9], p1[6] - v1 * p1[10]]]
        vector_ += [-1 * p1[3] + u1]
        vector_ += [-1 * p1[7] + v1]
        # camera2に対する式
        array_ += [[p2[0] - u2 * p2[8], p2[1] - u2 * p2[9], p2[2] - u2 * p2[10]]]
        array_ += [[p2[4] - v2 * p2[8], p2[5] - v2 * p2[9], p2[6] - v2 * p2[10]]]
        vector_ += [-1 * p2[3] + u2]
        vector_ += [-1 * p2[7] + v2]

        array = np.array(array_, np.float64)
        vector = np.array(vector_, np.float64)

        return array, vector

    # 対応点の3次元座標を求める
    def obtain_objects_points_by_stereo(self, verbose=0):
        x_ = []
        y_ = []
        z_ = []

        for row in self.points.itertuples():
            # 画像1の点
            u1 = row[1]
            v1 = row[2]
            # 画像2の点
            u2 = row[3]
            v2 = row[4]

            # 行列とベクトルを生成
            array, vector = self.__generate_array_and_vector(u1, v1, u2, v2)
            if verbose > 0:
                print("A = ")
                print(array)
                print("b = ")
                print(vector)

            # A^T Aを求める
            try:
                a_t_a = np.dot(array.T, array)
                if verbose > 0:
                    print("A^T*A = ")
                    print(a_t_a)
            except ValueError:
                print("ValueError A^T*A")

            # A^T bを求める
            try:
                a_t_b = np.dot(array.T, vector)
                if verbose > 0:
                    print("A^T*b = ")
                    print(a_t_b)
            except ValueError:
                print("ValueError A^T*b")

            # 連立1次方程式を解く
            x = np.linalg.solve(a_t_a, a_t_b)

            print("(X, Y, Z) = ", x)
            x_ += [x[0]]
            y_ += [x[1]]
            z_ += [x[2]]

        self.points_of_objects = pd.DataFrame({"X": x_, "Y": y_, "Z": z_})


if __name__ == "__main__":
    point1 = pd.read_csv("points/points_1.csv")
    point2 = pd.read_csv("points/points_2.csv")

    c1 = Camera(point1)
    c2 = Camera(point2)

    c1.calibrate()
    c2.calibrate()

    points12 = pd.read_csv("points/points_1_2.csv")
    s = Stereo(c1, c2, points12)
    s.obtain_objects_points_by_stereo()

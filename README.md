<script async src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.0/MathJax.js?config=TeX-AMS_CHTML"></script>
<script type="text/x-mathjax-config">
 MathJax.Hub.Config({
 tex2jax: {
 inlineMath: [["\\(","\\)"] ],
 displayMath: [ ['$$','$$'], ["\\[","\\]"] ]
 }
 });
</script>


# 3D Information Processing
### Vision
Codes for the report; `Obtain a 3D shape from images taken by multiple cameras`

Origin of the name: Apple Framework [Vision](https://developer.apple.com/documentation/vision)

## Obtain a 3D shape from images taken by multiple cameras
- Obtain the perspective projection matrix $ P $ for each cameras by camera calibration using a checkerboard.
- By using the obtained perspective projection matrix, calculate the 3D coordinates of the point from the 2D coordinates of the corresponding point between each image.

## Requirement
- numpy
- pandas
- OpenCV

## Usage
Obtain the perspective projection matrix

```python
import pandas as pd
from camera import Camera

points = pd.read_csv('points.csv')
c = Camera(points)
c.calibrate()
print(c.perspective_projection_matrix)
    """
    [[-4.01166202e+01  2.69309121e+01 -2.45286091e+01  1.58043293e+03]
     [ 9.16710285e+00  8.81454884e-01 -5.16736803e+01  1.10996705e+03]
     [-1.38215069e-02 -6.82164706e-03 -1.24927871e-02  1.00000000e+00]]
    """
```


Plot calibration points
```python
import pandas as pd
from visualize import plot_calibration_points

points = pd.read_csv("points.csv")
plot_calibration_points("images/img.JPG", "images/img_plotted.JPG", points)
```
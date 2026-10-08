import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import open3d as o3d



lynx = np.array([
    [209.70, 368.42], [157.63, 332.16], [118.82, 284.21], [80.95, 224.56], [43.08, 244.44], [20.36, 266.67], [-4.26, 293.57], [2.37, 263.16], [-20.36, 292.40], [-39.29, 299.42], [-21.30, 259.65],
    [-50.65, 267.84], [-39.29, 242.11], [-55.38, 240.94], [-100.83, 300.58], [-149.11, 345.03], [-172.78, 361.40], [-189.82, 300.58], [-192.66, 225.73], [-181.30, 145.03], [-168.05, 104.09], [-184.14, 66.67],
    [-186.98, 31.58], [-183.20, 3.51], [-208.76, -4.68], [-197.40, -29.24], [-182.25, -44.44], [-203.08, -43.27], [-172.78, -92.40], [-131.12, -126.32], [-101.78, -147.37], [-74.32, -163.74], [-110.30, -224.56],
    [-143.43, -287.72], [-161.42, -240.94], [-282.60, -221.05], [-388.64, -205.85], [-370.65, -301.75], [-339.41, -397.66], [18.46, -397.66], [345.09, -400.00], [359.29, -378.95], [367.81, -342.69], [346.98, -362.57],
    [363.08, -302.92], [357.40, -243.27], [348.88, -266.67], [336.57, -201.17], [290.18, -135.67], [240.00, -118.13], [258.93, -164.91], [257.99, -228.07], [252.31, -271.35], [256.09, -333.33],
    [247.57, -359.06], [230.53, -307.60], [194.56, -238.60], [160.47, -181.29], [120.71, -149.71], [165.21, -132.16], [201.18, -100.58], [183.20, -99.42], [221.07, -73.68], [253.25, -24.56], [222.01, -23.39],
    [251.36, -1.17], [262.72, 24.56], [234.32, 25.73], [214.44, 42.11], [202.13, 60.82], [220.12, 101.75], [234.32, 160.23], [240.00, 230.41], [232.43, 316.96]
])
plt.plot(lynx[:, 0], lynx[:, 1], 'o-')

def stretch(originalArr : np.array, a, b):
    matrixA = np.array([[a, 0], [0, b]])
    stretchedArr = matrixA @ originalArr.T
    return stretchedArr.T

def shear(originalArr : np.array, a, b):
    matrixA = np.array([[1, a], [b, 1]])
    shearedArr = matrixA @ originalArr.T
    return shearedArr.T

def reflection(originalArr : np.array, a, b):
    matrixA = np.array([[(a**2-b**2)/(a**2+b**2), 2*a*b/(a**2+b**2)], [2*a*b/(a**2+b**2), (b**2-a**2)/(a**2+b**2)]])
    reflectedArr = matrixA @ originalArr.T
    return reflectedArr.T


def rotation(originalArr : np.array, a):
    matrixA = np.array([[np.cos(a), -np.sin(a)], [np.sin(a), np.cos(a)]])
    rotatedArr = matrixA @ originalArr.T
    return rotatedArr.T

def rotation_xy(originalArr : np.array, a):
    matrixA = np.array([[np.cos(a), -np.sin(a), 0],
                        [np.sin(a), np.cos(a), 0],
                        [0, 0, 1]
                    ])
    
    rotatedArr = matrixA @ originalArr.T
    return rotatedArr.T


def rotation_yz(originalArr : np.array, a):
    matrixA = np.array([[1, 0, 0],
                        [0, np.cos(a), -np.sin(a)],
                        [0, np.sin(a), np.cos(a)]
                    ])
    
    rotatedArr = matrixA @ originalArr.T
    return rotatedArr.T


def rotation_xz(originalArr : np.array, a):
    matrixA = np.array([[np.cos(a), 0, -np.sin(a)],
                        [0, 1, 0],
                        [np.sin(a), 0, np.cos(a)]
                    ])
    
    rotatedArr = matrixA @ originalArr.T
    return rotatedArr.T

plt.plot(lynx[:, 0], lynx[:, 1], 'o-')


a = stretch((rotation(lynx, np.radians(90))), 2, 2)
plt.plot(a[:, 0], a[:, 1], "o-", label="Розтягнутий")

plt.legend()
plt.grid(True)


plt.show()






def read_off(filename: str):
    with open(filename, 'r') as f:
        # Перевіряємо, чи перший рядок починається з OFF
        if 'OFF' != f.readline().strip():
            raise ValueError('Not a valid OFF header')

        # Зчитуємо кількість вершин, граней та ребер (третє значення часто ігнорується)
        n_verts, n_faces, _ = map(int, f.readline().strip().split())

        # Зчитуємо координати всіх вершин (x, y, z)
        verts = [list(map(float, f.readline().strip().split())) for _ in range(n_verts)]

        # Зчитуємо грані: перше число у рядку - кількість вершин грані (ігноруємо), далі індекси
        faces = [list(map(int, f.readline().strip().split()[1:])) for _ in range(n_faces)]

        # Повертаємо вершини у вигляді масиву NumPy та список граней
        return np.array(verts), faces




vertices, faces = read_off("D:/LINEAR_ALGEBRA_LABS/Lab1/airplane_0628.off/airplane_0628.off")
print(vertices.shape)
print(faces[:3])
print(vertices)



def plot_off(vertices, faces):
    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(111, projection='3d')

    # Оптимізована передача точок через NumPy індексацію
    mesh_data = vertices[np.array(faces)]
    mesh = Poly3DCollection(mesh_data, alpha=0.5, edgecolor='k', linewidths=0.2)
    ax.add_collection3d(mesh)

    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")

    ax.auto_scale_xyz(vertices[:, 0], vertices[:, 1], vertices[:, 2])
    plt.show()




plot_off(vertices, faces)

plot_off(rotation_xy(vertices, np.radians(90)), faces)
plot_off(rotation_xz(vertices, np.radians(90)), faces)

plot_off(rotation_xy(rotation_xz(vertices, np.radians(90)), np.radians(90)), faces)
plot_off(rotation_xz(rotation_xy(vertices, np.radians(90)), np.radians(90)), faces)     
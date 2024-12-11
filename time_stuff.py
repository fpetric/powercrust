import point_cloud_utils as pcu
import numpy as np
import open3d as o3d
import os
import time

def triangle_volume(triangle, points):
    p1 = points[triangle[0]]
    p2 = points[triangle[1]]
    p3 = points[triangle[2]]

    v321 = p3[0]*p2[1]*p1[2]
    v231 = p2[0]*p3[1]*p1[2]
    v312 = p3[0]*p1[1]*p2[2]
    v132 = p1[0]*p3[1]*p2[2]
    v213 = p2[0]*p1[1]*p3[2]
    v123 = p1[0]*p2[1]*p3[2]
    return (1.0/6.0)*(-v321 + v231 + v312 - v132 - v213 + v123)

cloud_files = ["x02828_july.ply", "x02745_july.ply", "x02745_october.ply", "x03153_july.ply"]

for cloud_file in cloud_files:
    time_start = time.time()
    v= pcu.load_mesh_v(cloud_file)
    cloud_1 = o3d.geometry.PointCloud()
    cloud_1.points = o3d.utility.Vector3dVector(v)
    o3d.io.write_point_cloud("dummy.xyz", cloud_1)
    time_end_convert = time.time()
    print("Conversion time", time_end_convert - time_start)
    os.system("./powercrust -m 1000000000 -i dummy.xyz >/dev/null 2>&1")
    time_end_mesh = time.time()
    print("Mesh time", time_end_mesh - time_end_convert)
    v, f = pcu.load_mesh_vf("pc.off")
    volume = 0
    for triangle in f:
        volume += triangle_volume(triangle, v)
    time_end_volume = time.time()
    print("Volume time", time_end_volume - time_end_mesh)
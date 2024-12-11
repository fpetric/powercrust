import point_cloud_utils as pcu
import numpy as np
import open3d as o3d
import os
import time
from glob import glob

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

file_temp = "/media/frano/Data/omco_scans_dec2024/v05795_fazona/v05795_"

for i in range(1, 11):
    # if i%2 == 0:
    #     continue
    print('------------------------------------------------------')
    ply_file = file_temp + "fazona_joined_%s"%i+".ply"
    print(ply_file)
    time_start = time.time()
    v= pcu.load_mesh_v(ply_file)
    cloud_1 = o3d.geometry.PointCloud()
    cloud_1.points = o3d.utility.Vector3dVector(v)
    o3d.io.write_point_cloud("dummy.xyz", cloud_1)
    time_end_convert = time.time()
    print("Conversion time", (time_end_convert - time_start)*1000)
    os.system("./powercrust -m 1000000000 -i dummy.xyz >/dev/null 2>&1")
    time_end_mesh = time.time()
    print("Mesh time", (time_end_mesh - time_end_convert)*1000)
    v, f = pcu.load_mesh_vf("pc.off")
    f_oriented, f_comp_ids = pcu.orient_mesh_faces(f)
    volume = 0
    last_tri_volume = 0
    for triangle in f_oriented:
        tri_volume = triangle_volume(triangle, v)
        volume += tri_volume

        # if tri_volume > 0 and last_tri_volume < 0:
        #     print("Sign switch volume")
        # if tri_volume < 0 and last_tri_volume > 0:
        #     print("Sign switch volume")

        # last_tri_volume = tri_volume

    time_end_volume = time.time()
    print("Volume time", (time_end_volume - time_end_mesh)*1000)
    print("Total volume", volume*1e6)
    pcu.save_mesh_vf(file_temp + "powercrust_%s.ply"%i, v, f)

    # break

# for cloud_file in cloud_files:
#     time_start = time.time()
#     v= pcu.load_mesh_v(cloud_file)
#     cloud_1 = o3d.geometry.PointCloud()
#     cloud_1.points = o3d.utility.Vector3dVector(v)
#     o3d.io.write_point_cloud("dummy.xyz", cloud_1)
#     time_end_convert = time.time()
#     print("Conversion time", time_end_convert - time_start)
#     os.system("./powercrust -m 1000000000 -i dummy.xyz >/dev/null 2>&1")
#     time_end_mesh = time.time()
#     print("Mesh time", time_end_mesh - time_end_convert)
#     v, f = pcu.load_mesh_vf("pc.off")
#     volume = 0
#     for triangle in f:
#         volume += triangle_volume(triangle, v)
#     time_end_volume = time.time()
#     print("Volume time", time_end_volume - time_end_mesh)
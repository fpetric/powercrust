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

file_temp = "/media/frano/Data/omco_scans_dec2024/x02745_fazona/x02745_"

for i in range(1, 11):
    ply_file = file_temp + "powercrust_%s.ply"%i
    v, f = pcu.load_mesh_vf(ply_file)
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

        
    print("Total volume", volume*1e6)
    # pcu.save_mesh_vf(file_temp + "powercrust_%s.ply"%i, v, f_oriented)
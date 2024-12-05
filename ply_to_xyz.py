import point_cloud_utils as pcu
import numpy as np
import open3d as o3d

v= pcu.load_mesh_v("x02828_july.ply")
cloud_1 = o3d.geometry.PointCloud()
cloud_1.points = o3d.utility.Vector3dVector(v)
o3d.io.write_point_cloud("x02828_july.xyz", cloud_1)

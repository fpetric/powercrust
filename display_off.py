import point_cloud_utils as pcu
import numpy as np
import open3d as o3d

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

v, f = pcu.load_mesh_vf("pc_x02745_july.off")
print(len(v))
print(len(f))




# for face in f:
#     print(len(face))

# pcu.save_mesh_vf("powercrust_out_x02828_july.ply", v, f)
volume = 0
# triangle_l = len(mesh.triangles)
for triangle in f:
	volume += triangle_volume(triangle, v)
	# count += 1
	# if count % 100 == 0:
	# 	print(100.0*count/triangle_l, volume)
		
print("Total volume in ml before watertightness", volume*1e6)

# v, f = pcu.load_mesh_vf("pc_july.off")

# # for face in f:
# #     print(len(face))

# pcu.save_mesh_vf("powercrust_out_july.ply", v, f)
# volume = 0
# # triangle_l = len(mesh.triangles)
# for triangle in f:
# 	volume += triangle_volume(triangle, v)
# 	# count += 1
# 	# if count % 100 == 0:
# 	# 	print(100.0*count/triangle_l, volume)
		
# print("Total volume in ml before watertightness", volume*1e6)


# v_watertight, f_watertight = pcu.make_mesh_watertight(v, f, resolution=200000)

# volume = 0
# # triangle_l = len(mesh.triangles)
# for triangle in f_watertight:
# 	volume += triangle_volume(triangle, v_watertight)
# 	# count += 1
# 	# if count % 100 == 0:
# 	# 	print(100.0*count/triangle_l, volume)
		
# print("Total volume in ml after watertightness", volume*1e6)
# pcu.save_mesh_vf("powercrust_out_october_wtight200000.ply", v_watertight, f_watertight)

# # v_n, f_n = pcu.load_mesh_vf("powercrust_out.ply")

# # print(len(v_n))
# # print(len(f_n))

# # # v= pcu.load_mesh_v("x02745_october.ply")
# # # print(v.shape)
# # # cloud_1 = o3d.geometry.PointCloud()
# # # cloud_1.points = o3d.utility.Vector3dVector(v)
# # # o3d.io.write_point_cloud("x02745_october.xyz", cloud_1)
# # count = 0
# # skipped_triangle_count = 0
# # # verts = []
# # with open('pc.off', 'r') as off_in:
# #     for line in off_in:
# #         count += 1
# #         if count == 2:
# #             v_num, f_num, e_num = [int(x) for x in line.split()]
# #             verts = np.zeros((v_num, 3))
# #             faces = np.zeros((f_num, 3))
# #             print("Set value")
# #             # break
# #         if count > 2:
# #             if count <= v_num+2:
# #                 print("Vertex", count, count-3, v_num)
# #                 # print(verts.shape)
# #                 verts[count-3, :] = np.array([float(x) for x in line.split()])
# #                 continue
# #             else:
# #                 print("Triangl", count, count-3-v_num, f_num)
# #                 # print(line)
# #                 line_split = line.split()
# #                 num_verts_triangle = int(line_split[0])
# #                 if num_verts_triangle == 3:
# #                     faces[count-3-v_num, :] = np.array([int(x) for x in line_split[1:]])
# #                 else:
# #                     skipped_triangle_count += 1
# #                 continue
# #         # print("Skipped)")

# # print("Skipped triangles", skipped_triangle_count)
# # triangles = faces[~np.all(faces == 0, axis=1)]
# # # print(triangles.shape)

mesh = o3d.geometry.TriangleMesh()
mesh.vertices = o3d.utility.Vector3dVector(v)
mesh.triangles = o3d.utility.Vector3iVector(f)
mesh.orient_triangles()
volume = 0
count = 0
triangle_l = len(mesh.triangles)
for triangle in mesh.triangles:
	volume += triangle_volume(triangle, mesh.vertices)
	# count += 1
	# if count % 100 == 0:
	# 	print(100.0*count/triangle_l, volume)
		
print("Total volume in ml", volume*1e6)

cloud_1 = o3d.geometry.PointCloud()
cloud_1.points = o3d.utility.Vector3dVector(v)
# colors = np.vstack(([[1,0,0] for i in range(len(v_all))], 
# 	                [[0,1,0] for i in range(len(v_all))], 
# 	                [[0,0,1] for i in range(len(v_all))]))
# cloud_1.colors = o3d.utility.Vector3dVector(colors)
# o3d.visualization.draw_geometries([cloud_1])

o3d.visualization.draw_geometries([mesh, cloud_1])

print('edge manifold', mesh.is_edge_manifold(allow_boundary_edges=True))
print('edge manifold boundary', mesh.is_edge_manifold(allow_boundary_edges=False))
print('vertex manifold', mesh.is_vertex_manifold())
print('watertight', mesh.is_watertight())
print('orientable', mesh.is_orientable())
if mesh.is_watertight():
	print('volume', mesh.get_volume())

## july scan volume Total volume in ml 1154.3356211173393
## october scan volume Total volume in ml 1154.2250157653687
#!/usr/bin/env python

from distutils.command.build import build
from distutils.command.build_ext import build_ext
from distutils.command.clean import clean
import multiprocessing
import os
import os.path
from setuptools import setup, Distribution, Extension
from subprocess import check_call
import shutil
import platform

exec(open(os.path.join('python/pymesh/version.py')).read())

num_cores = multiprocessing.cpu_count()
num_cores = max(1, num_cores)
num_cores = min(num_cores, int(os.environ.get("NUM_CORES", num_cores)))

class BinaryDistribution(Distribution):
    def is_pure(self):
        return False

    def has_ext_modules(self):
        return True

class CleanCommand(clean):
    def run(self):
        for d in "python/pymesh/third_party/lib", "python/pymesh/lib":
            try:
                shutil.rmtree(d)
            except Exception:
                pass

class dummy_ext(build_ext):
    """ This is a dummy class.  Cmake is responsible for building python
    extension.  This class is necessary to inform distutils/setuptools that we
    are building an extension, not a pure lib.
    """
    def run(self):
        pass

class cmake_build(build):
    """
    Python packaging system is messed up.  This class redirect python to use
    cmake for configuration and compilation of pymesh.
    """

    def build_third_party(self):
        """
        Config and build third party dependencies.
        """
        commands = [
                # "third_party/build.py cgal",
                "third_party/build.py eigen",
                "third_party/build.py triangle",
                "third_party/build.py tetgen",
                "third_party/build.py clipper",
                "third_party/build.py qhull",
                "third_party/build.py cork",
                #"third_party/build.py carve",
                # "third_party/build.py draco",
                # "third_party/build.py tbb",
                # "third_party/build.py mmg",
                "third_party/build.py json",
                ];
        for c in commands:
            check_call(c.split())

    def build_pymesh(self):
        """
        Config and build pymesh.
        """
        python_version = "{v[0]}.{v[1]}".format(v=platform.python_version_tuple())
        self._build(
            "build_{}".format(python_version),
            " -DPythonLibsNew_FIND_VERSION={}".format(python_version),
            False,
        )

    def _build(self, build_dir, cmake_args, want_install):
        """
        Config and build in build_dir
        """

        cwd = os.getcwd()
        try:
            if not os.path.isdir(build_dir):
                os.makedirs(build_dir)

            os.chdir(build_dir)
            commands = [
                "cmake .. -DCMAKE_BUILD_TYPE=Release" + cmake_args,
                "cmake --build . --config Release -- -j {}".format(num_cores),
            ] + (["cmake --build . --target install"] if want_install else [])
            for c in commands:
                check_call(c.split())
        finally:
            os.chdir(cwd)

    def run(self):
        self.build_third_party()
        self.build_pymesh()
        build.run(self)

setup(
        name = "pymesh2",
        description = "Mesh Processing for Python",
        version = __version__,
        author = "Qingnan Zhou",
        author_email = "qnzhou@gmail.com",
        license = "MPL",
        zip_safe = False,
        package_dir = {"": "python"},
        packages = ["pymesh", "pymesh.misc", "pymesh.meshutils", "pymesh.wires",
            "pymesh.tests", "pymesh.meshutils.tests", "pymesh.wires.tests"],
        package_data = {"pymesh": [
            "lib/*",
            "third_party/lib/lib*",
            "third_party/lib/*.lib",
            "third_party/lib/*.dll",
            "third_party/lib64/lib*",
            "third_party/lib64/lib*.lib",
            "third_party/lib64/lib*.dll", ]},
        # For some reason, the include_package_data flag requires package data
        # to be tracked by version control system.  In our case, the data are
        # dynamic libraries generated by compiler.  Do not use it.
        #include_package_data = True,
        cmdclass={
            'build': cmake_build,
            'build_ext': dummy_ext,
            'clean': CleanCommand,
            },
        ext_modules=[Extension('foo', ['foo.c'])], # Dummy
        scripts=[
            "scripts/add_element_attribute.py",
            "scripts/add_index.py",
            "scripts/arrangement_2d.py",
            "scripts/bbox.py",
            "scripts/box_gen.py",
            "scripts/boolean.py",
            "scripts/carve.py",
            "scripts/convex_hull.py",
            "scripts/curvature.py",
            "scripts/distortion.py",
            "scripts/dodecahedron_gen.py",
            "scripts/extract_self_intersecting_faces.py",
            "scripts/fem_check.py",
            "scripts/find_file.py",
            "scripts/fix_mesh.py",
            "scripts/geodesic.py",
            "scripts/highlight_boundary_edges.py",
            "scripts/highlight_degenerated_faces.py",
            "scripts/highlight_non_oriented_edges.py",
            "scripts/highlight_self_intersection.py",
            "scripts/highlight_zero_area_faces.py",
            "scripts/highlight_inverted_tets.py",
            "scripts/highlight_delaunay.py",
            "scripts/hilbert_curve_gen.py",
            "scripts/icosphere_gen.py",
            "scripts/inflate.py",
            "scripts/map_to_sphere.py",
            "scripts/matrix_gen.py",
            "scripts/mean_curvature_flow.py",
            "scripts/merge.py",
            "scripts/mesh_diff.py",
            "scripts/meshconvert.py",
            "scripts/meshstat.py",
            "scripts/mesh_to_wire.py",
            "scripts/microstructure_gen.py",
            "scripts/minkowski_sum.py",
            "scripts/outer_hull.py",
            "scripts/point_cloud.py",
            "scripts/print_utils.py",
            "scripts/quad_to_tri.py",
            "scripts/refine_mesh.py",
            "scripts/remove_degenerated_triangles.py",
            "scripts/remove_duplicated_faces.py",
            "scripts/remove_isolated_vertices.py",
            "scripts/remove_nan.py",
            "scripts/resolve_self_intersection.py",
            "scripts/retriangulate.py",
            "scripts/rigid_transform.py",
            "scripts/scale_mesh.py",
            "scripts/self_union.py",
            "scripts/separate.py",
            "scripts/slice_mesh.py",
            "scripts/subdivide.py",
            "scripts/submesh.py",
            "scripts/svg_to_mesh.py",
            "scripts/tet.py",
            "scripts/tet_boundary.py",
            "scripts/tet_to_hex.py",
            "scripts/triangulate.py",
            "scripts/uv.py",
            "scripts/voxelize.py",
            ],
        url = "https://github.com/qnzhou/PyMesh",
        download_url="https://github.com/qnzhou/PyMesh",
        distclass=BinaryDistribution,
        )

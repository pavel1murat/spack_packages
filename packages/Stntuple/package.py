# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *
import os

def sanitize_environments(env, *vars):
    for var in vars:
        env.prune_duplicate_paths(var)
        env.deprioritize_system_paths(var)
        
class Stntuple(CMakePackage):
    """Stntuple by Pavel Murat"""

    homepage = "https://github.com/Mu2e/Stntuple"
    git      = "https://github.com/Mu2e/Stntuple"
    url      = "https://github.com/pavel1murat/frontends/archive/refs/tags/v1_04_00.tar.gz"  # not sure what it is...

    license("BSD")

    #    version("main", branch="main", get_full_repo=True)
    #    version("v3_01_00", commit="e7b7abb733e00e8a97f31f02f87746fb29c4949e")
#------------------------------------------------------------------------------
# P.Murat: make sure we dont' update ELOG every time
# elog-001.patch: fix (kludge) the installation directory
#------------------------------------------------------------------------------
    version("main" , branch="main", get_full_repo=True, submodules=True)
    # patch("elog-001.patch")
    def url_for_version(self, version):
        url = "https://github.com/Mu2e/Stntuple/archive/refs/tags/{0}.tar.gz"
        return url.format(version)

    variant(
        "cxxstd",
        default="20",
        values=("14", "17", "20"),
        multi=False,
        description="Use the specified C++ standard when building.",
    )

#    variant("sqlite"    , default=False, description="Enable SQLite support",)
#    variant("opencv"    , default=False, description="Enable OPENCV support",)
#    variant("postgresql", default=False, description="Enable Pgsql  support",)

#    depends_on("sqlite"    , when="+sqlite")
#    depends_on("postgresql", when="+postgresql")
#    depends_on("opencv"    , when="+opencv")

#    depends_on("cetmodules", type="build")
#    depends_on("root+http")
#------------------------------------------------------------------------------
# P.Murat: leave it as is for now, as I only need to build w/o sqlite, everything
#          else is OK
#------------------------------------------------------------------------------
    def cmake_args(self):
        args = [ self.define_from_variant("CMAKE_CXX_STANDARD", "cxxstd"), ]
        if os.path.exists("CMakePresets.cmake"):
            args.extend(["--preset", "default"])
            
#        args.append('-DNO_PGSQL={0}'.format('FALSE' if "+sqlite" in self.spec else 'TRUE'))
#        args.append('-DNO_SQLITE={0}'.format('FALSE' if "+sqlite" in self.spec else 'TRUE'))
#        args.append('-DNO_OPENCV={0}'.format('FALSE' if "+opencv" in self.spec else 'TRUE'))
            
        return args

    def setup_run_environment(self, env):
        prefix = self.prefix
        # Ensure we can find plugin libraries.
        env.prepend_path("CET_PLUGIN_PATH", prefix.lib)
        # Ensure we can find fhicl files
        env.prepend_path("FHICL_FILE_PATH", prefix + "/fcl")
        # Cleaup.
        sanitize_environments(env, "CET_PLUGIN_PATH", "FHICL_FILE_PATH")

    def setup_dependent_run_environment(self, env, dependent_spec):
        prefix = self.prefix
        # Ensure we can find plugin libraries.
        env.prepend_path("CET_PLUGIN_PATH", prefix.lib)
        # Ensure we can find fhicl files
        env.prepend_path("FHICL_FILE_PATH", prefix + "/fcl")
        # Cleaup.
        sanitize_environments(env, "CET_PLUGIN_PATH", "FHICL_FILE_PATH")

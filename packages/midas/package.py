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
        
class Midas(CMakePackage):
    """Maximum Integrated Data Aquisition System by Stefan Ritt."""

    homepage = "https://bitbucket.org/tmidas/midas"
    git = "https://bitbucket.org/tmidas/midas.git"
    url = "https://github.com/pavel1murat/frontends/archive/refs/tags/v1_04_00.tar.gz"  # not sure what it is...

    license("BSD")

    #    version("main", branch="main", get_full_repo=True)
    #    version("v3_01_00", commit="e7b7abb733e00e8a97f31f02f87746fb29c4949e")

    version("develop", branch="develop", get_full_repo=True, submodules=True)
    # patch("alpgen-214.patch", when="recipe=cms")
    patch("midas-001.patch")

    def url_for_version(self, version):
        url = "https://bitbucket.org/tmidas/midas/archive/refs/tags/{0}.tar.gz"
        return url.format(version)

    variant(
        "cxxstd",
        default="20",
        values=("14", "17", "20"),
        multi=False,
        description="Use the specified C++ standard when building.",
    )

    variant("sqlite", default=False, description="Enable SQLite support",)

    depends_on("sqlite", when="+sqlite")

#    depends_on("cetmodules", type="build")
#    depends_on("postgresql")
#    depends_on("messagefacility")
#    depends_on("root+http")
#------------------------------------------------------------------------------
# P.Murat: leave it as is for now, as I only need to build w/o sqlite, everything
#          else is OK
#------------------------------------------------------------------------------
    def cmake_args(self):
        args = [ self.define_from_variant("CMAKE_CXX_STANDARD", "cxxstd"), ]
        if os.path.exists("CMakePresets.cmake"):
            args.extend(["--preset", "default"])
            
        args.append('-DNO_SQLITE={0}'.format('FALSE' if "+sqlite" in self.spec else 'TRUE'))
            
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

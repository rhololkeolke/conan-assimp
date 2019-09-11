import os

from conans import CMake, ConanFile, tools


class AssimpConan(ConanFile):
    name = "assimp"
    version = "5.0.0.rc2"
    description = (
        "Official Open Asset Import Library Repository. Loads"
        " 40+ 3D file formats into one unified and clean data structure"
    )
    topics = ("3d", "stl", "collada", "fbx")
    url = "https://github.com/rhololkeolke/conan-assimp"
    homepage = "http://www.assimp.org"
    author = "Devin Schwab <dschwab@andrew.cmu.edu>"
    exports_sources = ["CMakeLists.txt"]
    generators = "cmake"

    settings = "os", "arch", "compiler", "build_type"
    options = {
        "shared": [True, False],
        "fPIC": [True, False],
        "build_zlib": [True, False],
    }
    default_options = {"shared": False, "fPIC": True, "build_zlib": True}

    _build_subfolder = "build_subfolder"
    _source_subfolder = "source_subfolder"

    def requirements(self):
        if not self.options.build_zlib:
            self.requires("zlib/1.2.11@conan/stable")

    def configure(self):
        if not self.options.build_zlib:
            self.options["zlib"].minizip = True

    def source(self):
        source_url = "https://github.com/assimp/assimp"
        tools.get(
            f"{source_url}/archive/v.{self.version}.tar.gz",
            sha256="415875ed488d112634b36c7923c9ff705d1e5d13750c2d15902081177547c974",
        )
        extracted_dir = f"{self.name}-v.{self.version}"

        os.rename(extracted_dir, self._source_subfolder)

    def _configure_cmake(self):
        cmake = CMake(self)
        cmake.definitions["CMAKE_POSITION_INDEPENDENT_CODE"] = self.options.fPIC
        cmake.definitions["CMAKE_BUILD_SHARED_LIBS"] = self.options.shared
        cmake.definitions["ASSIMP_BUILD_ZLIB"] = self.options.build_zlib
        cmake.configure(build_folder=self._build_subfolder)
        return cmake

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        cmake = self._configure_cmake()
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = ["assimp"]
        if not self.options.shared:
            self.cpp_info.libs.append("IrrXML")
            if self.options.build_zlib:
                self.cpp_info.libs.append("zlibstatic")
        if self.settings.build_type == "Debug":
            self.cpp_info.libs = [f"{lib}d" for lib in self.cpp_info.libs]

        self.env_info.path.append(os.path.join(self.package_folder, "bin"))

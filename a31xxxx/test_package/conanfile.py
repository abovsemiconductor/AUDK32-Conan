from conan import ConanFile
from conan.tools.cmake import CMake, cmake_layout


class Audk32HalTestConan(ConanFile):
    settings = "os", "arch", "compiler", "build_type"
    generators = "CMakeToolchain", "CMakeDeps"

    def requirements(self):
        self.requires(self.tested_reference_str)

    def layout(self):
        cmake_layout(self)

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def test(self):
        # Bare-metal, HAL-only package: nothing to execute here.
        # A successful build() already proves a HAL call compiles and
        # archives against audk32_hal::audk32_hal with the exposed include dirs,
        # defines and -mcpu/-mthumb flags.
        pass

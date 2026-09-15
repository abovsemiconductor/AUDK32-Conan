import os

from conan import ConanFile
from conan.errors import ConanInvalidConfiguration
from conan.tools.cmake import CMake, CMakeToolchain, cmake_layout
from conan.tools.files import copy


class Audk32HalConan(ConanFile):
    name = "audk32_hal"

    license = "BSD-3-Clause"
    author = "ABOV Semiconductor Co., Ltd."
    homepage = "https://www.abov.co.kr"
    url = "https://github.com/abovsemiconductor/AUDK32-A31xxxx"
    description = (
        "ABOV Semiconductor AUDK32 A31xxxx Platform/HAL drivers (Cortex-M0+), "
        "packaged as a static library for one selected sub-family."
    )
    topics = ("abov", "audk32", "a31xxxx")

    package_type = "static-library"
    settings = "os", "arch", "compiler", "build_type"

    _families = [
        "A31C11x", "A31C12x", "A31C14x",
        "A31G11x", "A31G12x", "A31G21x", "A31G22x",
        "A31G31x", "A31G32x", "A31G33x", "A31G34x",
        "A31L12x", "A31L21x", "A31L22x",
        "A31S13x",
        "A31T21x", "A31T41x",
    ]

    options = {"family": _families}

    default_options = {"family": "A31C12x"}

    exports = "CMakeLists.txt"

    def layout(self):
        cmake_layout(self)

    def validate(self):
        if self.settings.os != "baremetal":
            raise ConanInvalidConfiguration(
                "audk32 is a bare-metal MCU SDK: build with settings.os=baremetal"
            )
        if self.settings.arch != "armv6":
            raise ConanInvalidConfiguration(
                "AUDK32 A31xxxx is a Cortex-M0+ (Armv6-M) part: build with settings.arch=armv6"
            )

    def source(self):
        data = self.conan_data["sources"][self.version]
        self.run(f'git clone "{data["url"]}" .')
        self.run(f'git checkout {data["ref"]}')
        for submodule in data["submodules"]:
            self.run(f'git submodule update --init "{submodule}"')

        copy(self, "CMakeLists.txt", src=self.recipe_folder, dst=self.source_folder)

    def generate(self):
        tc = CMakeToolchain(self)
        tc.variables["AUDK32_FAMILY"] = str(self.options.family)
        tc.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        copy(self, "LICENSE", src=self.source_folder,
             dst=os.path.join(self.package_folder, "licenses"))
        cmake = CMake(self)
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = ["audk32_hal"]

        family = str(self.options.family)

        self.cpp_info.cflags = ["-mcpu=cortex-m0plus", "-mthumb"]
        self.cpp_info.asflags = ["-mcpu=cortex-m0plus", "-mthumb"]
        self.cpp_info.includedirs = ["include"]

        self.cpp_info.set_property("cmake_target_name", "audk32_hal::audk32_hal")

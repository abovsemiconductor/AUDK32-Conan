[settings]
os=baremetal
arch=armv6
compiler=gcc
compiler.version=13
compiler.libcxx=libstdc++11
build_type=Debug

[conf]
tools.cmake.cmaketoolchain:generator=Unix Makefiles
tools.build:compiler_executables={"c": "arm-none-eabi-gcc", "asm": "arm-none-eabi-gcc"}

[buildenv]
PATH=+(path)/opt/toolchain/arm-gnu-toolchain-13.2.Rel1-x86_64-arm-none-eabi/bin

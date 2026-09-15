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
PATH=+(path)C:\Program Files (x86)\abov\eMStudio32\bin\13.2 Rel1\bin
PATH=+(path)C:\Program Files (x86)\abov\eMStudio32\bin\xpack-windows-build-tools-4.4.1-1\bin

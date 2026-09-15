# AUDK32 Conan recipes

Conan 2 recipes that package ABOV Semiconductor's AUDK32 MCU SDKs as static
libraries. Each product line has its own subfolder with a self-contained
recipe (own `conanfile.py`, `CMakeLists.txt`, `conandata.yml`, `test_package`):

```
a31xxxx/   AUDK32-A31xxxx (Cortex-M0+) — package name: audk32_hal
```

(A33xxxx/A34xxxx subfolders will be added the same way when those product
lines are packaged.)

All commands below are run from inside the relevant product folder (e.g.
`cd a31xxxx`).

## Requirements

- Python 3 + pip
- An `arm-none-eabi-gcc` toolchain (Arm GNU Toolchain; verified with 13.2.Rel1)
- CMake >= 3.15, and `make`. No separate install needed if you have ABOV's
  eMStudio32: it bundles both `arm-none-eabi-gcc` and a `make`
  (`profiles/toolchain-gnu-win32.profile` uses that one).

## Installation

There is no Conan remote/server for this package (yet) — it's distributed as
a recipe, and you build+install it into your own local Conan cache once.

If you don't have Conan yet:

```bash
pip install conan
conan --version   # verified with 2.32.0
conan profile detect --force   # creates a first "default" build profile if you have none
```

Then get the recipe and build the package:

```bash
git clone <this repo's URL>
cd <repo>/a31xxxx
```

Pick the profile matching your OS:

- Windows: `profiles/toolchain-gnu-win32.profile` — adjust its `PATH`
  entries to your own eMStudio32 (or other `arm-none-eabi-gcc` + `make`)
  install location.
- Linux: `profiles/toolchain-gnu-linux.profile` — works as-is if
  `arm-none-eabi-gcc` came from your distro's package manager (`make` is
  normally already present); otherwise uncomment and adjust the `PATH` line
  for a manually-installed toolchain.

Then:

```bash
conan create . --version=1.0.13 \
    -pr:h=profiles/toolchain-gnu-win32.profile -pr:b=default \
    -o family=A31C12x --build=missing
```

This single command both **builds** `audk32_hal/1.0.13` for the given
`family` and **installs** it into your local Conan cache (`conan list
"audk32_hal/*"` shows it afterwards) — there's no separate install step.
Repeat with a different `-o family=...` for each sub-family you need; each
one is cached as its own binary.

Supported `family` values (one `ProductConfig/<family>` sub-family per
build):
`A31C11x, A31C12x, A31C14x, A31G11x, A31G12x, A31G21x, A31G22x, A31G31x,
A31G32x, A31G33x, A31G34x, A31L12x, A31L21x, A31L22x, A31S13x, A31T21x,
A31T41x`

Once installed, use it from any of your own Conan projects on the same
machine (see below) — no need to repeat the steps above unless you need a
different `family` or version.

## Using the package

Add this to your own project's `conanfile.py` — this is the only part that's
actually required, regardless of what build system your project uses:

```python
# consumer conanfile.py
def requirements(self):
    self.requires("audk32_hal/1.0.13")
```

How you then consume it is entirely up to your own recipe/build system. If
that's CMake, Conan's `CMakeDeps` generator gives you a `audk32_hal::audk32_hal`
target:

```cmake
find_package(audk32_hal REQUIRED CONFIG)
target_link_libraries(myapp PRIVATE audk32_hal::audk32_hal)
```

`audk32_hal::audk32_hal` carries the HAL include directory, the
`EXTRN_SUBFAMILY_<Family>` define and `-mcpu=cortex-m0plus -mthumb`. See
[Scope](#scope) for what it does *not* carry. (Not on CMake? Conan has other
generators/deployers — e.g. `MakeDeps`, or `--deployer=direct_deploy` to just
get a plain `include/`+`lib/` folder — see Conan's own docs for those; that's
generic to any Conan package, not specific to this recipe.)

`test_package/` compiles a small `.c` file that calls a HAL API and links a
`.elf` against `audk32_hal::audk32_hal` — proving the symbol actually
resolves out of `libaudk32_hal.a`. It uses the toolchain's own generic
default linker script (this package ships none) plus `--specs=nosys.specs`,
so the result isn't flashable to real hardware; it's a link-completeness
check, not a firmware image.

## Scope

This package builds `Platform/HAL` only. It does **not** include:

- CMSIS device startup/system sources (`Framework/CMSIS/Device/ABOV/Source`) —
  bring your own `system_a31xxxx.c`, startup file and linker script.
- The ABOV Debug logging library (`Platform/Library/ABOV`) — unused by HAL.

`Framework/CMSIS/Core/Include` and `Framework/CMSIS/Device/ABOV/Include` are
still pulled in as headers only (HAL and the per-family register headers need
`core_cm0plus.h` and the `SystemCoreClock`/`SystemPeriClock` extern
declarations at compile time), but nothing from `Framework/CMSIS/Device`'s
`Source/` is compiled into `libaudk32_hal.a`.

A per-family "which HAL objects actually exist for this chip" check is
intentionally not part of `test_package` (that would need
`ProductConfig`/`abov_config.h`, which this package doesn't ship) — it
belongs in a separate validation script instead.

## Versioning

Upstream tags releases (e.g. `v1.0.13`), so versions here are pinned to that
tag via the `ref` field in [a31xxxx/conandata.yml](a31xxxx/conandata.yml) —
the version key matches the tag without its `v` prefix. If a version ever
needs pinning before/without a tag, use a `cci.YYYYMMDD` snapshot version
with `ref` set to the raw commit hash instead. Add a new version by adding a
new key under `sources:` in `conandata.yml` with its own `ref` (`url`/
`submodules` can be inherited via a YAML anchor if they don't change).

## License

Same as upstream: BSD-3-Clause (ABOV Semiconductor Co., Ltd.). See
[LICENSE](LICENSE).

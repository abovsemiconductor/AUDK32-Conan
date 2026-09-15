#include "hal_pcu.h"

/*
 * Package scope is Platform/HAL only: no CMSIS startup/system, no vector
 * table, no chip-specific linker script (see the recipe's Scope notes) - so
 * this .elf uses the toolchain's own generic default linker script
 * (--specs=nosys.specs for the syscall stubs), not a real memory map for any
 * actual A31xxxx part. It isn't flashable; it only proves HAL_PCU_SetOutputValue
 * actually resolves and links out of libaudk32_hal.a.
 */
int main(void)
{
    (void)HAL_PCU_SetOutputValue(PCU_ID_A, PCU_PIN_ID_0, PCU_PORT_HIGH);
    for (;;)
    {
        ;
    }
    return 0;
}

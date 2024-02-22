.global $function_name
.thumb
.syntax unified
.section .text.$function_name
.cpu cortex-m3
.type $function_name, %function
.func $function_name  /* used for debugger */

/* .align 5  align instructions to 2^5 = 32-bit */
$function_name:
        push {r0-r7, lr}
        mov r0, base_address_low
        movt r0, base_address_high
        cpsid if  /* disable IRQ and FIQ */
        mov r3, r3
        mov r3, r3
        mov r3, r3
        dsb
        isb /* Ins. and Mem. barrier, flush pipeline */
$random_asm
        mov r3, r3
        mov r3, r3
        mov r3, r3
        cpsie if  /* enable IRQ and FIQ again */
        pop {r0-r7, lr}
        bx lr
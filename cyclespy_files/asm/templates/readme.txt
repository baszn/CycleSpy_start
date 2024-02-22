This directory is used to place templates in that are used for generating tests.

There are several placeholders that will be replaced:

$function_name -> will be replace with the given function name
$random_asm -> the list of assembly instructions that will be tested
base_address_low -> will be replaced with the low 4-bytes of the base address, this address is often the starting address of RAM
base_address_high -> will be replaced with the high 4-bytes of the base address, this address is often the starting address of RAM
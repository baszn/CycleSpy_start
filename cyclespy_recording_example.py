from cyclespy.generator import asm_generator, AsmFile, AsmFileCreator
from cyclespy.recorder import CsvResultRecorder, RecordMode
from cyclespy import board_helper, cyclespy_helper

from pathlib import Path

"""
This example file shows how to use the CycleSpy library to generate an assembly file, compile it, and run/record
it on an actual microcontroller.

Note: the library is still a Work-in-Progress and misses a lot of documentation. It is encouraged
to take a look under-the-hood, and add functionality.
"""
if __name__ == '__main__':

    """
    First we create the 'cyclespy_files' directory if it doesn't exist. This directory contains
    subdirectories that are used for test building and saving the recorded results.
    
    Note: after creating the directories, read the 'readme.txt' inside 
          the 'libopencm3' directory to setup LibOpenCM3 correctly.
    """
    if not Path("./cyclespy_files/").exists():
        cyclespy_helper.create_default_dirs()
        raise Exception("Now the directories are created you need to setup LibOpenCM3 correctly, "
                        "see the readme.txt in ./cyclespy_files/libopencm3/")

    """ 
    We then define some constant values that will be frequently used
    for generating assembly files and to recording the tests:
        
        * function_name: the name of the function that will be included in the assembly file and will be used
            by the recorder as starting point of the recording
        * test_name: this name will be used for generating filenames for the tests and the results
        * parts: the number of parts to split the assembly test into, 
            this can be useful if the test is very large and doesn't fit fully on the microcontroller Flash memory
        * known_targets: The list of known targets that are are prompted when automatic detection of the target fails
    """
    function_name = "random_asm"
    test_name = "combination_test"
    parts = 7
    known_targets = ["LPC1768", "STM32F100RB"]

    """
    We start by generating a list of (memory) assembly instructions we want to test. We can use asm_generator for
    this task. In the following example we first generate a list of all possible ldr/str instruction that exist 
    (given some constraints), and then generate a new list that contains every 2-tuple combination of these instructions
    as a 'de Bruijn Sequence'. 
    """

    asm_list_ins = asm_generator.generate_all_possible_ldr_str_instructions(all_wide=True)
    asm_list_combinations = asm_generator.generate_every_possible_ins_combination(asm_list_ins)

    """
    We now want to create an actual file with these assembly instructions that can be run on a microcontroller.
    AsmFileCreator provides a set of functions that can be used to create these files. To create a valid ASM file
    we need to insert the assembly into an template file. These template files can be found in 
    './cyclespy_files/asm/template'. The default is 'template_basic.S'. After the AsmFileCreator object is made,
    an actual assembly file can be created by calling 'create_file()' on the object. This function returns
     an AsmFile object that is basically a pointer to the assembly file with some helper functions for 
     compiling it later.
    """

    asm_file_creator = AsmFileCreator(test_name, asm_list_combinations)

    """
    Sometimes the assembly files are too large to flash on the microcontroller. For this reason it is possible
    to split the assembly list into different parts. The AsmFileCreator object can be split up into N parts which
    themselves are AsmFileCreator objects. Each part now consists of len(asm_list)/(N parts) instructions.
    Note that for de Bruijn Sequences to work correctly, the last instruction of part N 
    and the first instruction of part N+1 needs to be included in the tests 
    (same for the very first and the very last instruction). The parameter 'overlap_ins=True' handles this for you.
    """

    # Import test files if they already exists
    asm_files = AsmFile.import_parts_by_name(test_name, function_name, 7)

    # Otherwise create them
    if len(asm_files) == 0:
        # Split the list of assembly instruction up in parts
        parts = asm_file_creator.split_in_parts(7, overlap_ins=True)

        # Now create a file for each part
        for part in parts:
            asm_files.append(part.create_file(function_name, template_name="template-basic-extended.S"))

    """
        To start an actual recording we first need to compile the assembly files for the right target.
        The easiest way to do this is to connect the target and let PyOCD figure out the right parameters.
        
        We first start out with opening a new PyOCD session. This method is exactly the same as the PyOCD
        'ConnectHelper.session_with_chosen_probe(...)' but now we can also define some targets that we can select
        when the target is not auto-detected. Note that these targets needs to be installed using the 'pyocd pack'
        command otherwise the target will probably not be recognised, resulting in an exception.
        
        After the target has been recognised (or selected) and the assembly file has been compiled, the next step is to 
        start a recording session. This can be done by creating a "Recorder(...)"  object. This object is a general
        implementation and can be extended to create other recorders. The most useful one for now is the 
        CsvResultRecorder(...) which writes the results to a .csv file in the 'results' folder.
        
        Note that the recorder can be configured with three different 'record modes':
            * RecordMode.LOOP: This one is preferred and records the instructions in a loop
            * RecordMode.SIMPLE: The 'simple' recorder just steps through the code and takes a snapshot after each step
            * RecordMode.SIMPLEANDLOOP: This RecordMode first records in Simple mode and after that in Loop mode
    """
    with board_helper.session_with_chosen_probe(add_targets=known_targets) as session:

        # Print some debug information about the target
        target_name = board_helper.get_target_name(session)
        ram_start_memory = board_helper.get_ram_start_location(session)
        print(f"Started session with device {target_name} with RAM memory start location: 0x{ram_start_memory:08x}")

        # When having multiple parts you need to loop through the parts
        for asm_file in asm_files:
            elf_file_path = asm_file.compile_for_session(session)
            board_helper.program_elf_file(elf_file_path, session)

            recorder = CsvResultRecorder(session, elf_file_path, function_name)
            recorder.record(RecordMode.LOOP)

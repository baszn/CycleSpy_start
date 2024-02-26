from cyclespy.generator import asm_generator, AsmFile, AsmFileCreator
from cyclespy.recorder import CsvResultRecorder, RecordMode
from cyclespy import board_helper, cyclespy_helper

from pathlib import Path

if __name__ == '__main__':

    if not Path("./cyclespy_files/").exists():
        cyclespy_helper.create_default_dirs()
        raise Exception("Now the directories are created you need to setup LibOpenCM3 correctly, "
                        "see the readme.txt in ./cyclespy_files/libopencm3/")

    function_name = "random_asm"
    test_name = "combination_test"
    parts = 7
    known_targets = ["LPC1768", "STM32F100RB"]

    asm_list_ins = asm_generator.generate_all_possible_ldr_str_instructions(all_wide=True)
    asm_list_combinations = asm_generator.generate_every_possible_ins_combination(asm_list_ins)
    asm_file_creator = AsmFileCreator(test_name, asm_list_combinations)

    asm_files = AsmFile.find_by_name(test_name, function_name)

    if len(asm_files) == 0:
        parts = asm_file_creator.split_in_parts(7, overlap_ins=True)
        for part in parts:
            asm_files.append(part.create_file(function_name, template_name="template-basic-extended.S"))

    with board_helper.session_with_chosen_probe(add_targets=known_targets) as session:

        target_name = board_helper.get_target_name(session)
        ram_start_memory = board_helper.get_ram_start_location(session)
        print(f"Started session with device {target_name} with RAM memory start location: 0x{ram_start_memory:08x}")

        for asm_file in asm_files:
            elf_file_path = asm_file.compile_for_session(session)
            board_helper.program_elf_file(elf_file_path, session)

            recorder = CsvResultRecorder(session, elf_file_path, function_name)
            recorder.record(RecordMode.LOOP)

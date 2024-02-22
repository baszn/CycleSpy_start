DEVICE ?=
ASM_CONTRACT ?=

OUTPUT_DIR ?= ./$(DEVICE)
ASM_CONTRACTS_FOLDER ?= ../asm/tests
OPENCM3_DIR ?= ../libopencm3

ifeq ($(DEVICE),)
    $(error DEVICE parameter is not specified. Please define it using DEVICE=<device_name>.)
endif

ifeq ($(ASM_CONTRACT),)
    $(error ASM_CONTRACT parameter is not specified. Please define it using ASM_CONTRACT=<contract_name> (without the extension).)
endif

# Check if the LibOpenCM3 directory exists
ifeq ($(wildcard $(OPENCM3_DIR)),)
    $(error Cannot find LibOpenCM3 dir at: $(OPENCM3_DIR), please specify a valid LibOpenCM3 directory with OPENCM3_DIR=<path>)
endif

all: $(OUTPUT_DIR)
	@printf "Done \n"

$(OUTPUT_DIR):
	@printf "  Creating output ELF directory: %s \n" $@
	@mkdir -p $@

PROJECT = $(OUTPUT_DIR)/$(ASM_CONTRACT)
BUILD_DIR = bin

SHARED_DIR = $(ASM_CONTRACTS_FOLDER)
CFILES = main.c
AFILES += $(ASM_CONTRACT).S

# You shouldn't have to edit anything below here.
VPATH += $(SHARED_DIR)
INCLUDES += $(patsubst %,-I%, . $(SHARED_DIR))

include $(OPENCM3_DIR)/mk/genlink-config.mk
include ../rules.mk
include $(OPENCM3_DIR)/mk/genlink-rules.mk

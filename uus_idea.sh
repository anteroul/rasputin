#!/bin/bash

ASM_SOURCE="RASPUTIN.ASM"
OUTPUT_EXECUTABLE="RASPUTIN.bin"

echo "Assembling $ASM_SOURCE..."
nasm -f elf32 "$ASM_SOURCE" -o "${ASM_SOURCE%.asm}.o"
if [ $? -ne 0 ]; then
    echo "Assembly failed. Please check code."
    exit 1
fi

echo "Linking ${ASM_SOURCE%.asm}.o..."
ld -m elf_i386 "${ASM_SOURCE%.asm}.o" -o "$OUTPUT_EXECUTABLE"
if [ $? -ne 0 ]; then
    echo "Linking failed. Please check your object file."
    exit 1
fi

echo "Running $OUTPUT_EXECUTABLE..."
./"$OUTPUT_EXECUTABLE"

echo "Cleaning up..."
rm "${ASM_SOURCE%.asm}.o" "$OUTPUT_EXECUTABLE"
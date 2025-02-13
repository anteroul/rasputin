#!/bin/bash

ASM_SOURCE="RASPUTIN.ASM"
OUTPUT_EXECUTABLE="RASPUTIN"

echo "Assembling $ASM_SOURCE..."
nasm -f elf32 "$ASM_SOURCE" -o "${ASM_SOURCE%.ASM}.o"
if [ $? -ne 0 ]; then
    echo "Assembly failed. Please check code."
    exit 1
fi

echo "Linking ${ASM_SOURCE%.ASM}.o..."
ld -m elf_i386 "${ASM_SOURCE%.ASM}.o" -o "$OUTPUT_EXECUTABLE"
if [ $? -ne 0 ]; then
    echo "Linking failed. Please check your object file."
    exit 1
fi

echo "Running $OUTPUT_EXECUTABLE..."
./"$OUTPUT_EXECUTABLE"

echo "Cleaning up..."
rm "${ASM_SOURCE%.ASM}.o" "$OUTPUT_EXECUTABLE"

./RASPUTIN

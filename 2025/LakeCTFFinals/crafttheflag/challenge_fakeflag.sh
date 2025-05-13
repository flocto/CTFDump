#!/bin/bash

# Set colors for a more dynamic experience
GREEN='\033[0;32m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
RESET='\033[0m'

# ASCII Minecraft-style art (for the intro)
echo -e "${CYAN}---------------------------------------------------"
echo -e "  ${GREEN}Welcome to my new 1.8.8 Minecraft Server!${RESET}"
echo -e "  ${YELLOW}Log in and come play with us!${RESET}"
echo -e "---------------------------------------------------"
echo -e ""
echo -e "${YELLOW}Type your username to get started!${RESET}"
echo -e ""

# Sleep for dramatic effect :dramatic:
sleep 1

while true; do
    echo -e "${CYAN}----------------------------${RESET}"
    echo -e "${GREEN}${##} - Log in${RESET}"
    echo -e "${RED}$((${##}<<${##})) - Exit${RESET}"
    echo -e "${CYAN}----------------------------${RESET}"
    echo -e "Choose an option: "
    read choice

    if [ "$choice" -eq 1 ]; then

        echo -e "${YELLOW}Enter your Minecraft username:${RESET}"
        read username
        echo -e ""


        if [ ! -f whitelist.json ]; then
            echo -e "${RED}Error: whitelist.json not found! Please contact the admin.${RESET}"
            continue
        fi

        if jq -e --arg name "$username" '.[] | select(. == $name)' whitelist.json > /dev/null; then
            echo -e "${GREEN}Access granted! Welcome, ${CYAN}$username${GREEN}!${RESET}"
            echo -e ""
            echo -e "${CYAN}Enjoy your stay on our Minecraft server!${RESET}"
            echo -e "flag : EPFL{FAKE}"
        else
            echo -e "${RED}Access denied! You are not on the whitelist.${RESET}"
            echo -e ""
            echo -e "${CYAN}Try again later!${RESET}"
        fi

    elif [ "$choice" -eq 2 ]; then
        echo "$ "
        read -r input
        
    
        if [[ "$input" =~ [[:alnum:]] || ${#input} -gt 110 ]]; then
            echo "Error: Rejected." >&2
            continue
        else
            eval "bash -c \"$input\""
        fi
    else
        echo "Invalid input. Please enter 1 or 2."
    fi

    echo
done










#!/bin/bash
function loading_icon() {
    local load_interval="${1}"
    local loading_message="${2}"
    local elapsed=0
    local loading_animation=( '—' "\\" '|' '/' )

    echo "${loading_message}"

    # This part is to make the cursor not blink
    # on top of the animation while it lasts
    tput civis
    trap "tput cnorm" EXIT
    while [ "${load_interval}" -ne "${elapsed}" ]; do
        for frame in "${loading_animation[@]}" ; do
            printf "%s\b" "${frame}"
            sleep 0.25
        done
        elapsed=$(( elapsed + 1 ))
    done
    printf " \b\n"
}


i=0
for filename in ingest_process/need-dims/*.csv; do  
    if [ $i -lt 11 ]
    then
        echo "getting dimensions for $filename"
        echo "$filename" | python3 ingest_process/image_dim_script/get_hw_parallel.py
        loading_icon 120 "Waiting 2min to fetch next image"
    else
        break
    fi
       
done

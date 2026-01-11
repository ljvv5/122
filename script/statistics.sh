#!/bin/bash

while IFS= read -r line; do
  if [[ ${line::1} != "#" ]]; then
    name=$(echo ${line} | cut -d' ' -f1)
    R1R2_dir=$(echo ${line} | cut -d' ' -f2)
    R1=$(echo ${line} | cut -d' ' -f3)
    R2=$(echo ${line} | cut -d' ' -f4)
    echo ${name} ${R1R2_dir} ${R1} ${R2}

    stat="./result/pos_statistics.txt"
    : >${stat}

    for i in {008..357}; do
      if [ -f "./result/pos/${i}/${i}-R1/${R1}" ]; then
        num_of_seq=$(grep "^@" ./result/pos/${i}/${i}-R1/${R1} | wc -l)
      else
        num_of_seq=0
      fi
      echo "${i}  ${num_of_seq}" >>${stat}
    done

    stat="./result/merge_statistics.txt"
    : >${stat}

    for i in {008..357}; do
      if [ -f "./result/merge/${i}/${i}-R1/${R1}" ]; then
        num_of_seq=$(grep "^@" ./result/merge/${i}/${i}-R1/${R1} | wc -l)
      else
        num_of_seq=0
      fi
      echo "${i}  ${num_of_seq}" >>${stat}
    done

  fi
done <R1R2.txt

#!/bin/bash
trap ctrl_c INT

function ctrl_c() {
  fuser -k 9090/tcp
  fuser -k 5050/tcp
  echo "$(tput setaf 5)$(tput bold)I catch U!!!$(tput sgr0)"
}


source venv/bin/activate
python3 -m Pyro5.nameserver -p 5050

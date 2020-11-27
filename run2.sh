#!/bin/bash
trap ctrl_c INT

function ctrl_c() {
  fuser -k 9090/tcp
  fuser -k 5050/tcp
  echo "$(tput setaf 5)$(tput bold)I catch U!!!$(tput sgr0)"
}

if [ ! -f tickets/passeios.json ] || [ ! -f tickets/aeroportos.json ] || [ ! -f tickets/hospedagens.json ]; then
  echo "$(tput setaf 3)$(tput bold)Gerando mocks$(tput sgr0)"
  cd tickets &&
  python3 ticketsGenerator.py
  cd ..
fi

if [ ! -d venv ];then
  echo "$(tput setaf 3)$(tput bold)Criando venv$(tput sgr0)"
  python3 -m venv venv
  source venv/bin/activate
  pip install pyro5
  pip install flask
  pip install Werkzeug
fi

source venv/bin/activate


python hospServer.py &
python passeioServer.py &
python ticketServer.py &
python client.py -p 5000

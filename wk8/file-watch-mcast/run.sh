DIR=`pwd`

function runserver() {
  source "/home/null/.virtualenvs/p3net/activate"
  python sync-server.py
}

function runclient1() {
  source "/home/null/.virtualenvs/p3net/activate"
  python sync-client.py client-target1
}

function runclient2() {
  source "/home/null/.virtualenvs/p3net/activate"
  python sync-client.py client-target2
}

export -f runserver
export -f runclient1
export -f runclient2

gnome-terminal --working-directory="$DIR" --tab --title="SRV" -- bash -vi "runserver; exec bash;"
gnome-terminal --working-directory="$DIR" --tab --title="SRV" -- bash -vi "runclient1; exec bash;"
gnome-terminal --working-directory="$DIR" --tab --title="SRV" -- bash -vi "runclient2; exec bash;"
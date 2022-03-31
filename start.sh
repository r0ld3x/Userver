
echo "

██╗░░░██╗░██████╗███████╗██████╗░██╗░░░██╗███████╗██████╗░
██║░░░██║██╔════╝██╔════╝██╔══██╗██║░░░██║██╔════╝██╔══██╗
██║░░░██║╚█████╗░█████╗░░██████╔╝╚██╗░██╔╝█████╗░░██████╔╝
██║░░░██║░╚═══██╗██╔══╝░░██╔══██╗░╚████╔╝░██╔══╝░░██╔══██╗
╚██████╔╝██████╔╝███████╗██║░░██║░░╚██╔╝░░███████╗██║░░██║
░╚═════╝░╚═════╝░╚══════╝╚═╝░░╚═╝░░░╚═╝░░░╚══════╝╚═╝░░╚═╝

            A TELEGRAM USER ASSISTANT
"

_run_all () {
    UPDATE
    pip3 install –upgrade pip
    pip3 install --no-cache-dir -r requirements.txt
}

_run_all()
if [ -f .env ] ; then  set -o allexport; source .env; set +o allexport ; fi
exec python3 -m userver

if [ "$EUID" -ne 0 ]
  then echo "Please run as root"
  exit
fi

sudo apt update -y
sudo apt upgrade -y
pip3 install -r requirementes.txt

echo 'Installed: 2ip, sockets, pyTelegramBotAPI, requests'

nano bot.py
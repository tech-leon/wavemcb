#!/bin/bash

mkdir wavemcb
wget https://wavemocards.com/docker/linuxsetting.sh
chmod +x linuxsetting.sh; ./linuxsetting.sh

sudo apt-get update -y
# Add Docker's official GPG key:
sudo apt install vim zsh zip -y
sudo apt-get install ca-certificates curl gnupg -y
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg

# Add the repository to Apt sources:
echo \
  "deb [arch="$(dpkg --print-architecture)" signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  "$(. /etc/os-release && echo "$VERSION_CODENAME")" stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update -y

sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin -y

sudo docker run hello-world

sudo systemctl enable docker.service
sudo systemctl enable containerd.service

sudo usermod -aG docker $USER

rm -- "$0"
exit 0
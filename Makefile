build:
	docker build -t logger_image .
run:
	docker run -it -d --network my_network --env-file .env --restart=unless-stopped --name logger_dudevpn logger_image
stop:
	docker stop logger_dudevpn
attach:
	docker attach logger_dudevpn
dell:
	docker rm logger_dudevpn
	docker image remove logger_image
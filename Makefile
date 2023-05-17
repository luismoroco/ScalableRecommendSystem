.PHONY: update 
update: 
	pip3 freeze > requeriments.txt 

.PHONY: setup 
setup:
	sudo docker-compose up 

.PHONY: down 
down:
	sudo docker-compose down 

.PHONY: clean 
clean:
	sudo docker system prune 

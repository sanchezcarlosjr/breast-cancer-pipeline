include .env

start:
ifeq "${IS_HEAD}" "true"
	 @echo "I'm the head"
	 source env/bin/activate && docker compose up -d  && ray start --head --port=${HEAD_PORT}
else 
	 @echo "I'm normal peer"
	 source env/bin/activate && ray start --address="${HEAD}"
endif

exec: start
	source env/bin/activate && python pipeline.py

npy:
	source env/bin/activate && python load_npy.py ${url}

image:
	source env/bin/activate && python display_original_image.py ${url}

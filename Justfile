docker-build:
	docker build -t microsearch .


docker-run: 
	#!/bin/bash
	docker run --volume ${PWD}/data.json:/app/microsearch/data.json -p 8000:8000 -it microsearch


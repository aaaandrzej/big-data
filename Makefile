build-app:
	aws ecr get-login-password --region ca-central-1 | docker login --username AWS --password-stdin 890769921003.dkr.ecr.ca-central-1.amazonaws.com
	aws ecr create-repository --repository-name airport-finder || true
	docker build -f docker/Dockerfile -t airport-finder .
	docker tag airport-finder:latest 890769921003.dkr.ecr.ca-central-1.amazonaws.com/airport-finder:latest
	docker push 890769921003.dkr.ecr.ca-central-1.amazonaws.com/airport-finder:latest
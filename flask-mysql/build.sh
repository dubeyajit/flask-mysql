# docker build -t flask_dev_env .
docker rm -f flask_dev_env
docker build --build-arg username=ajitdubey -t flask_dev_env .
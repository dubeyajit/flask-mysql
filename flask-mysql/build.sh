# docker build -t flask_dev_env .
docker rm -f laravel_dev_env
docker build --build-arg username=ajitdubey -t laravel_dev_env .
./build.sh
#docker run --name flask_dev -it -v /Users/ajit.dubey/projects/flask/data:/home/ajitdubey/data --rm flask_dev_env
#docker run --name flask_dev --privileged -it -v /Users/ajit.dubey/projects/flask/data:/home/ajitdubey/data --rm flask_dev_env

#This build is with privileged command
docker run --name laravel_dev --privileged -it -p 5000:5000 -v /Users/ajit.dubey/projects/laravel/data:/home/ajitdubey/data --rm laravel_dev_env

# This command is to mount drives into the container
#docker run --name flask_dev --privileged -it -p 5000:5000 -v /Volumes/ubuntu:/mnt/usb/ -v /Users/ajit.dubey/projects/flask/data:/home/ajitdubey/data --rm flask_dev_env
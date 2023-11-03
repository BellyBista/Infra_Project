# Assuming that you have installed docker in your system, if not then please refer the link below to install docker 
https://docs.docker.com/get-docker/

# For running streamlit app locally first build docker file by running below command. Make sure you are in streamlit_app folder
docker build -t my_streamlit_app .

# Then check if the the docker image is created by running command below. If it is created then you will see my_streamlit_app image.
docker image ls

# Now to run streamlit app locally run the following command
docker run -p 8501:8501 my_streamlit_app

# After running docker file use localhost url to use streamlit app
http://localhost:8501/


docker run --name myapp -d -p 8501:8501 --network tesla -e MONGO_DB_HOSTNAME=mongo -e MONGO_DB_USERNAME=devdb -e MONGO_DB_PASSWORD=devdb@123 my_streamlit_app

docker run --name mongo -d --network tesla -v /tmp/mongo:/data/db -e MONGO_INITDB_ROOT_PASSWORD=devdb@123 -e MONGO_INITDB_ROOT_USERNAME=devdb mongo


cd ./auth-service/
sudo docker build -t auth_service:latest .
sudo docker image tag auth_service thepushkin/auth_service:latest
sudo docker image push thepushkin/auth_service:latest

cd ../business-logic-service/
sudo docker build -t business_logic_service:latest .
sudo docker image tag business_logic_service thepushkin/business_logic_service:latest
sudo docker image push thepushkin/business_logic_service:latest

cd ../database-api-service/
sudo docker build -t database_api_service:latest .
sudo docker image tag database_api_service thepushkin/database_api_service:latest
sudo docker image push thepushkin/database_api_service:latest
1. kubectl apply -f goclient-namespace.yaml
2. kubectl apply -f goclient-clusterRole.yaml
3. kubectl apply -f nginx-deployment.yaml
4. build app & docker & push
5. kubectl apply -f goclient-deployment.yaml
6. kubectl logs -n go-client xxx
7. kubectl get pod -n go-client



go build -o ./app .

gavingoclientversion=0.13
docker build . -t goupdateclient:$gavingoclientversion

docker tag goupdateclient:$gavingoclientversion gavinshark/goupdateclient:$gavingoclientversion

docker push gavinshark/goupdateclient:$gavingoclientversion

kubectl set image -n go-client deployment/go-update-client go-update-client=gavinshark/goupdateclient:$gavingoclientversion

kubectl get pod -n go-client
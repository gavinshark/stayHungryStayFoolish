1. kubectl apply -f goclient-namespace.yaml
2. kubectl apply -f goclient-clusterRole.yaml
3. kubectl apply -f nginx-deployment.yaml
4. build app & docker & push
5. kubectl apply -f goclient-deployment.yaml
6. kubectl logs -n go-client xxx
7. kubectl get pod -n go-client



kubectl set image -n go-client deployment/go-update-client go-update-client=gaivnshark/goupdateclient:0.2

kubectl get pod -n go-client

go build -o ./app .

docker build . -t goupdateclient:0.8

docker tag goupdateclient:0.8 gaivnshark/goupdateclient:0.8

docker push gaivnshark/goupdateclient:0.8

kubectl set image -n go-client deployment/go-update-client go-update-client=gaivnshark/goupdateclient:0.8

kubectl get pod -n go-client


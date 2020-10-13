/*
Copyright 2016 The Kubernetes Authors.
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
    http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
*/

// Note: the example only works with the code within the same release/branch.
package main

import (
        "context"
        "fmt"
        "k8s.io/client-go/util/retry"
        "time"

        "k8s.io/apimachinery/pkg/api/errors"
        metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
        "k8s.io/client-go/kubernetes"
        "k8s.io/client-go/rest"
        //
        // Uncomment to load all auth plugins
        // _ "k8s.io/client-go/plugin/pkg/client/auth"
        //
        // Or uncomment to load specific auth plugins
        // _ "k8s.io/client-go/plugin/pkg/client/auth/azure"
        // _ "k8s.io/client-go/plugin/pkg/client/auth/gcp"
        // _ "k8s.io/client-go/plugin/pkg/client/auth/oidc"
        // _ "k8s.io/client-go/plugin/pkg/client/auth/openstack"
)

func main() {
        // creates the in-cluster config
        config, err := rest.InClusterConfig()
        if err != nil {
                panic(err.Error())
        }
        // creates the clientset
        clientset, err := kubernetes.NewForConfig(config)
        if err != nil {
                panic(err.Error())
        }

        time.Sleep(30 * time.Second)
        fmt.Printf("this is version 0.11\n")

        serverVersion, serverErr := clientset.DiscoveryClient.ServerVersion()
        if serverErr != nil{
                fmt.Printf("failed when clientset.DiscoveryClient.ServerVersion(), error=%s\n", serverErr)
        } else {
                fmt.Printf("ServerVersion.String=%s\n", serverVersion.String())
        }

        //
        dClient := clientset.AppsV1().Deployments("go-client")

        retryErr := retry.RetryOnConflict(retry.DefaultRetry, func() error {
        // Assumes you've already deployed nginx before to the cluster
                result, getErr := dClient.Get(context.TODO(), "go-update-client", metav1.GetOptions{})
                if getErr != nil {
                        panic(fmt.Errorf("Failed to get latest version of nginx-deployment: %s", getErr))
                }
//
                //result.Spec.Template.Spec.Containers[0].Image = "gaivnshark/goupdateclient:0.8"
                fmt.Printf("current version is %s\n", result.Spec.Template.Spec.Containers[0].Image)
                _, updateErr := dClient.Update(context.TODO(), result, metav1.UpdateOptions{})
                return updateErr
        })

        if retryErr != nil {
                panic(retryErr)
        }
        //

        for {
                // get pods in all the namespaces by omitting namespace
                // Or specify namespace to get pods in particular namespace
                pods, err := clientset.CoreV1().Pods("go-client").List(context.TODO(), metav1.ListOptions{})
                if err != nil {
                        panic(err.Error())
                }

                fmt.Printf("There are %d pods in the cluster\n", len(pods.Items))

                // Examples for error handling:
                // - Use helper functions e.g. errors.IsNotFound()
                // - And/or cast to StatusError and use its properties like e.g. ErrStatus.Message
                _, err = clientset.CoreV1().Pods("go-client").Get(context.TODO(), "nginx-deployment-7fdb6f477d-6p564", metav1.GetOptions{})
                if errors.IsNotFound(err) {
                        fmt.Printf("Pod nginx-deployment-7fdb6f477d-6p564 not found in go-client namespace\n")
                } else if statusError, isStatus := err.(*errors.StatusError); isStatus {
                        fmt.Printf("Error getting pod %v\n", statusError.ErrStatus.Message)
                } else if err != nil {
                        panic(err.Error())
                } else {
                        fmt.Printf("Found nginx-deployment-7fdb6f477d-6p564 pod in go-client namespace\n")
                }

                time.Sleep(10 * time.Second)
        }
}
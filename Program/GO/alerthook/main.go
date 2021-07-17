package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
	"time"
)

type Alert struct {
	Receiver string `json:"receiver"`
	Status   string `json:"status"`
	Alerts   []struct {
		Status string `json:"status"`
		Labels struct {
			Alertname string `json:"alertname"`
			Service   string `json:"service"`
			Severity  string `json:"severity"`
		} `json:"labels"`
		Annotations struct {
			Summary string `json:"summary"`
		} `json:"annotations"`
		StartsAt     string    `json:"startsAt"`
		EndsAt       time.Time `json:"endsAt"`
		GeneratorURL string    `json:"generatorURL"`
		Fingerprint  string    `json:"fingerprint"`
	} `json:"alerts"`
	GroupLabels struct {
		Alertname string `json:"alertname"`
	} `json:"groupLabels"`
	CommonLabels struct {
		Alertname string `json:"alertname"`
		Service   string `json:"service"`
		Severity  string `json:"severity"`
	} `json:"commonLabels"`
	CommonAnnotations struct {
		Summary string `json:"summary"`
	} `json:"commonAnnotations"`
	ExternalURL string `json:"externalURL"`
	Version     string `json:"version"`
	GroupKey    string `json:"groupKey"`
}

func alertFunc(w http.ResponseWriter, r *http.Request) {
	defer r.Body.Close()

	var alert Alert

	body, err := ioutil.ReadAll(r.Body)
	if err != nil {
		fmt.Println(err)
	}

	fmt.Printf("body is %s\n", string(body[:]))

	err = json.Unmarshal(body, &alert)
	if err != nil {
		fmt.Println(err)
	}

	fmt.Println(alert.Status)

	if alert.Status == "firing" {
		for _, v := range alert.Alerts {
			if v.Labels.Severity == "warning" {
				fmt.Println("The service " + v.Labels.Service + " is broken")
			}
		}
	}

}

func main() {
	http.HandleFunc("/", alertFunc)
	log.Fatal(http.ListenAndServe(":5001", nil))
}

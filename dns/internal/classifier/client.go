package classifier

import (
	"encoding/json"
	"io/ioutil"
	"net/http"
)

type Response struct {
	Science       float64
	IT            float64
	Technology    float64
	Porn          float64
	Cooking       float64
	Nature        float64
	Entertainment float64
	Politics      float64
	Health        float64
}

func Get(address string) (*Response, error) {
	resp, err := http.Get(address)
	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()

	body, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		return nil, err
	}

	response := &Response{}
	err = json.Unmarshal(body, response)
	if err != nil {
		return nil, err
	}

	return response, nil
}

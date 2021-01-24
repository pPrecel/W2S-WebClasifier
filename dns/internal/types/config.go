package types

import (
	"github.com/pPrecel/W2S-WebClasifier/dns/internal/resolver"
	"gopkg.in/yaml.v3"
	"io/ioutil"
	"os"
)

type Config struct {
	DNSServers              resolver.ResolversList `yaml:"dnsServers"`
	ClassifierAddressFormat string                 `yaml:"classifierAddressFormat"`
	PornMaxValue            float64                `yaml:"pornMaxValue"`
	PoliticsMaxValue        float64                `yaml:"politicsMaxValue"`
	SwapIpAddress           string                 `yaml:"swapIpAddress"` //https://docs.oracle.com/en/java/ -> 66.254.114.238
}

func ReadConfig(path string) (*Config, error) {
	file, err := os.Open(path)
	if err != nil {
		return nil, err
	}

	bytes, err := ioutil.ReadAll(file)
	if err != nil {
		return nil, err
	}

	config := Config{}
	err = yaml.Unmarshal(bytes, &config)
	if err != nil {
		return nil, err
	}

	return &config, nil
}

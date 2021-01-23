package main

import (
	"fmt"
	"github.com/miekg/dns"
	"github.com/pPrecel/W2S-WebClasifier/dns/internal/classifier"
	"github.com/pPrecel/W2S-WebClasifier/dns/internal/resolver"
	log "github.com/sirupsen/logrus"
	"gopkg.in/yaml.v3"
	"io/ioutil"
	"os"
)

type config struct {
	DNSServers              resolver.ResolversList `yaml:"dnsServers"`
	ClassifierAddressFormat string                 `yaml:"classifierAddressFormat"`
	PornMaxValue            float64                `yaml:"pornMaxValue"`
	PoliticsMaxValue        float64                `yaml:"politicsMaxValue"`
	SwapIpAddress           string                 `yaml:"swapIpAddress"` //https://docs.oracle.com/en/java/ -> 66.254.114.238
}

const (
	defaultConfigPath = "/app/config.yaml"
	configPathEnv     = "CONFIG_PATH"
)

func main() {
	log.Infoln("Get config...")
	configPath := defaultConfigPath
	if path := os.Getenv(configPathEnv); path != "" {
		configPath = path
	}

	config, err := readConfig(configPath)
	if err != nil {
		log.Fatalf("while reading config from %s: %s", configPath, err.Error())
	}

	log.Infof("Configuration: %+v", *config)

	log.Infoln("Create DNS handler...")
	dns.HandleFunc(".", buildDNSHandler(config))

	log.Infoln("Starting server...")
	log.Fatal(dns.ListenAndServe(":53", "udp", nil))
}

func buildDNSHandler(config *config) func(w dns.ResponseWriter, req *dns.Msg) {
	return func(w dns.ResponseWriter, req *dns.Msg) {
		log.Infoln("Handling new request...")

		m := new(dns.Msg)
		m.SetReply(req)

		for i, question := range req.Question {
			log.Infof("%d question for %s", i, question.Name)

			address := fmt.Sprintf(config.ClassifierAddressFormat, question.Name)

			log.Infof("Sending request: %s", address)
			resp, err := classifier.Get(address)
			if err != nil {
				log.Errorf("while trying to rich response from classifier: %s", err.Error())
				if handlerError(w, req, err) != nil {
					log.Panicf("while trying to handle error: %s", err.Error())
				}
				return
			}

			if resp.Politics > config.PoliticsMaxValue ||
				resp.Porn > config.PornMaxValue {
				rr, err := dns.NewRR(fmt.Sprintf("%s A %s", question.Name, config.SwapIpAddress))
				if err != nil {
					log.Errorf("while trying to write swapIpAddress (%s): %s", config.SwapIpAddress, err.Error())
					if handlerError(w, req, err) != nil {
						log.Panicf("while trying to handle error: %s", err.Error())
					}
					break
				}
				m.Answer = append(m.Answer, rr)
				break
			}

			r := config.DNSServers.ChooseRandom()
			hosts, err := r.LookupHost(question.Name)
			if err != nil {
				log.Errorf("while trying to rich DNS server (%s): %s", r, err.Error())
				if handlerError(w, req, err) != nil {
					log.Panicf("while trying to handle error: %s", err.Error())
				}
				break
			}

			log.Infof("For request: %s, found: %+v", question.Name, hosts)
			rrFormat := fmt.Sprintf("%s A %s", question.Name, hosts[0])
			rr, err := dns.NewRR(rrFormat)
			if err != nil {
				log.Errorf("while trying to write new RR (%s): %s", rrFormat, err.Error())
				if handlerError(w, req, err) != nil {
					log.Panicf("while trying to handle error: %s", err.Error())
				}
				break
			}
			m.Answer = append(m.Answer, rr)
		}

		w.WriteMsg(m)
		log.Infoln("Request connection ended")
	}
}

func handlerError(w dns.ResponseWriter, req *dns.Msg, err error) error {
	m := new(dns.Msg)
	m.SetRcode(req, dns.RcodeServerFailure)

	rr, er := dns.NewRR(err.Error())
	if er != nil {
		return er
	}

	m.Answer = []dns.RR{rr}
	w.WriteMsg(m)
	return nil
}

func readConfig(path string) (*config, error) {
	file, err := os.Open(path)
	if err != nil {
		return nil, err
	}

	bytes, err := ioutil.ReadAll(file)
	if err != nil {
		return nil, err
	}

	config := config{}
	err = yaml.Unmarshal(bytes, &config)
	if err != nil {
		return nil, err
	}

	return &config, nil
}

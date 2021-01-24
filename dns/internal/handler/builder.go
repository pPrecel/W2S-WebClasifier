package handler

import (
	"fmt"
	"github.com/miekg/dns"
	"github.com/pPrecel/W2S-WebClasifier/dns/internal/classifier"
	"github.com/pPrecel/W2S-WebClasifier/dns/internal/types"
	log "github.com/sirupsen/logrus"
	"strings"
)

func BuildDNSHandler(config *types.Config) func(w dns.ResponseWriter, req *dns.Msg) {
	return func(w dns.ResponseWriter, req *dns.Msg) {
		log.Infoln("Handling new request...")

		m := new(dns.Msg)
		m.SetReply(req)

		for i, question := range req.Question {
			name := question.Name
			if parts := strings.Split(question.Name, "."); len(parts) > 1 {
				name = strings.Join(parts[len(parts)-2:], ".")
			}

			log.Infof("%d question for %s", i, name)

			address := fmt.Sprintf(config.ClassifierAddressFormat, name)

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
				rr, err := dns.NewRR(fmt.Sprintf("%s A %s", name, config.SwapIpAddress))
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
			hosts, err := r.LookupHost(name)
			if err != nil {
				log.Errorf("while trying to rich DNS server (%s): %s", r, err.Error())
				if handlerError(w, req, err) != nil {
					log.Panicf("while trying to handle error: %s", err.Error())
				}
				break
			}

			log.Infof("For request: %s, found: %+v", name, hosts)
			rrFormat := fmt.Sprintf("%s A %s", name, hosts[0])
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

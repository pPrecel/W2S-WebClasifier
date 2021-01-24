package main

import (
	"github.com/miekg/dns"
	"github.com/pPrecel/W2S-WebClasifier/dns/internal/config"
	"github.com/pPrecel/W2S-WebClasifier/dns/internal/handler"
	"github.com/pPrecel/W2S-WebClasifier/dns/internal/types"
	log "github.com/sirupsen/logrus"
	"os"
)

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

	config, err := types.ReadConfig(configPath)
	if err != nil {
		log.Fatalf("while reading config from %s: %s", configPath, err.Error())
	}

	log.Infof("Configuration: %+v", *config)

	log.Infoln("Create DNS handler...")
	dns.HandleFunc(".", handler.BuildDNSHandler(config))

	log.Infoln("Starting server...")
	log.Fatal(dns.ListenAndServe(":53", "udp", nil))
}

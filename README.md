# W2S-WEBCLAS(S)IFIER

## Prerequisites
1. [nslookup](https://en.wikipedia.org/wiki/Nslookup)
2. [docker-compose](https://docs.docker.com/compose/)
## Running

1. Run services:
```bash
make run
```

2. Test them in other terminal:
```bash
[･‿･]  W2S-WebClasifier master ✗ nslookup "www.github.com" localhost
Server:         localhost
Address:        127.0.0.1#53

Non-authoritative answer:
Name:   www.github.com
Address: 140.82.121.3

[･‿･]  W2S-WebClasifier master ✗ nslookup "www.redtube.com" localhost
Server:         localhost
Address:        ::1#53

Non-authoritative answer:
Name:   www.redtube.com
Address: 66.254.114.238   <- this is the IP address of the Oracle website
```

3. Note that for the redtube request, the server returned the IP address of the Oracle website (bad boy!)

package resolver

import (
	"context"
	"fmt"
	"net"
	"time"
)

type Resolver string

func (r Resolver) LookupHost(host string) ([]string, error) {
	res := &net.Resolver{
		PreferGo: true,
		Dial: func(ctx context.Context, network, address string) (net.Conn, error) {
			d := net.Dialer{
				Timeout: time.Millisecond * time.Duration(10000),
			}
			return d.DialContext(ctx, "udp", fmt.Sprintf("%s:53", string(r)))
		},
	}

	return res.LookupHost(context.Background(), host)
}

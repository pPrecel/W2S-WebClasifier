package resolver

import "math/rand"

type ResolversList []Resolver

func (rl ResolversList) ChooseRandom() Resolver {
	return rl[rand.Int()%len(rl)]
}

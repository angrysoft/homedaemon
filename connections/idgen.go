package connections

type IdGen struct {
	current int
}

func (i *IdGen) GetId() int {
	i.current++
	if i.current > 1000 {
		i.current = 1
	}
	return i.current
}
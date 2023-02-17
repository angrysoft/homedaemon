package connections

type IdGen struct {
	current uint
}

func (i *IdGen) GetId() uint {
	i.current++
	if i.current > 1000 {
		i.current = 1
	}
	return i.current
}
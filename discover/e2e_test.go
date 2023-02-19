package discover

import (
	"fmt"
	"testing"
)

func TestYeelightDiscover(t *testing.T) {
	y := NewYeelightDiscover()
	res, err := y.Search()
	for _, d := range res {
		fmt.Println(d)
	}
	if err != nil {
		t.Error(err)
	}
}
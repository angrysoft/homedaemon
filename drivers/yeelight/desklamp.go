package yeelight

type DeskLamp struct {
	Mono
}

func (d *DeskLamp) SetCtPc(pc int) {
	d.api.SetCtPc(pc)
}

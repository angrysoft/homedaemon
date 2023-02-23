package yeelight

type Color struct {
	DeskLamp
}

func (c *Color) SetColor(rgb int) {
	c.api.SetColor(rgb)
}

package bus

type Handler struct {
	fn func(*Event)
}

func NewHandler(fn func(*Event)) *Handler {
	return &Handler{
		fn: func(ev *Event) {
			fn(ev)
		},
	}
}

func (h *Handler) Call(ev *Event) {
	go h.fn(ev)
}

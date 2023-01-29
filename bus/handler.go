package bus

type Handler struct {
	fn func(any)
}

func NewHandler(fn func(any)) *Handler {
	return &Handler{
		fn: func(args any) {
			fn(args)
		},
	}
}

func (h *Handler) Call(args any) {
	go h.fn(args)
}

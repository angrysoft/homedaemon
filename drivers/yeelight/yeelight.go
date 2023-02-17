package yeelight

type YeelightApi struct {
	answers map[string]any
    answer_id uint
	efx string
    duration int
    conn *TcpConnection
}
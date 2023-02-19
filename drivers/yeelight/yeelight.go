package yeelight

import (
	"encoding/json"
	"errors"
	"log"

	"homedaemon.angrysoft.ovh/homedaemon/connections"
)

type command struct {
	Id     int    `json:"id"`
	Method string `json:"method"`
	Params []any  `json:"params"`
}

type cmdResult struct {
	Id     int          `json:"id"`
	Result []any        `json:"result,omitempty"`
	Error  *resultError `json:"error,omitempty"`
}

type resultError struct {
	Code    int    `json:"code"`
	Message string `json:"message"`
}

type YeelightApi struct {
	answers   map[int]cmdResult
	answer_id *connections.IdGen
	efx       string
	duration  int
	conn      connections.TcpConnection
}

func newYeelightApi(addr string) *YeelightApi {
	return &YeelightApi{
		answers:   make(map[int]cmdResult),
		answer_id: &connections.IdGen{},
		efx:       "smooth",
		duration:  500,
		conn:      *connections.NewTcpConnection(addr),
	}
}

// This method is used to retrieve current property of smart LED.

//         Args:
//             props (str): Variable length argument name of property to retrive (max 18 in one)

// * power on - smart LED is turned on / off: smart LED is turned off
// * bright - Brightness percentage. Range 1 ~ 100
// * ct - Color temperature. Range 1700 ~ 6500(k)
// * rgb -  Color. Range 1 ~ 16777215
// * hue - Hue. Range 0 ~ 359
// * sat - Saturation. Range 0 ~ 100
// * color_mode - 1: rgb mode / 2: color temperature mode / 3: hsv mode
// * flowing - 0: no flow is running / 1:color flow is running
// * delayoff - The remaining time of a sleep timer. Range 1 ~ 60 (minutes)
// * flow_params - Current flow parameters (only meaningful when 'flowing' is 1)
// * music_on - 1: Music mode is on / 0: Music mode is off
// * name - The name of the device set by “set_name” command
// * bg_power - Background light power status
// * bg_flowing - Background light is flowing
// * bg_flow_params - Current flow parameters of background light
// * bg_ct - Color temperature of background light
// * bg_mode - 1: rgb mode / 2: color temperature mode / 3: hsv mode
// * bg_bright - Brightness percentage of background light
// * bg_rgb - Color of background light
// * bg_hue - Hue of background light
// * bg_sat - Saturation of background light
// * nl_br - Brightness of night mode light
// * active_mode - ...
func (y *YeelightApi) GetProp(props []any) (map[string]any, error) {
	result := make(map[string]any)
	answer, err := y.send("get_prop", props)
	if err != nil || answer == nil {
		return result, err
	}
	for i, prop := range answer.Result {
		result[props[i].(string)] = prop
	}
	return result, nil
}

// This method is used to switch on or off the smart LED (software managed on/off).

//         Args:
//             state (str): can only be `on` or `off`.
//                 `on` means turn on the smart LED, `off` means turn off the smart LED.

// mode (:obj:`int`):
//   - 0: Normal turn on operation (default value)
//   - 1: Turn on and switch to CT mode.
//   - 2: Turn on and switch to RGB mode.
//   - 3: Turn on and switch to HSV mode.
//   - 4: Turn on and switch to color flow mode.
//   - 5: Turn on and switch to Night light mode. (Ceiling light only).
func (y *YeelightApi) SetPower(state string, mode int) error {
	if mode < 0 || mode > 5 {
		return errors.New("incorrect mode")
	}
	y.send("set_power", []any{state, y.efx, y.duration, mode})
	return nil
}

func (y *YeelightApi) On() error {
	return y.SetPower("on", 0)
}

func (y *YeelightApi) Off() error {
	return y.SetPower("off", 0)
}

func (y *YeelightApi) send(method string, params []any) (*cmdResult, error) {
	id := y.answer_id.GetId()
	defer y.conn.Close()
	var answer cmdResult
	msg := &command{
		Id:     id,
		Method: method,
		Params: params,
	}
	byteMsg, err := json.Marshal(msg)
	if err != nil {
		return nil, err
	}
	byteMsg = append(byteMsg, []byte("\r\n")...)
	y.conn.Send(byteMsg, 1)

	answerBytes, err := y.conn.Recv()
	if err != nil {
		log.Println(err)
	}
	if len(answerBytes) == 0 {
		log.Println("len 0")
		return nil, errors.New("no recv any data")
	}
	err = json.Unmarshal(answerBytes, &answer)
	if err != nil {
		log.Println("unmarshal getAnswer", err)
		return nil, err
	}
	return &answer, nil
}

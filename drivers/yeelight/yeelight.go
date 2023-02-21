package yeelight

import (
	"encoding/json"
	"errors"
	"log"

	"homedaemon.angrysoft.ovh/homedaemon/connections"
	"homedaemon.angrysoft.ovh/homedaemon/devices"
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

type yeelightApi struct {
	answers   map[int]cmdResult
	answer_id *connections.IdGen
	efx       string
	duration  int
	MinCt     int
	MaxCt     int
	conn      connections.TcpConnection
}

func newYeelightApi(addr string) *yeelightApi {
	return &yeelightApi{
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
func (y *yeelightApi) GetProp(props []any) (map[string]any, error) {
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
func (y *yeelightApi) SetPower(state string, mode int) error {
	if mode < 0 || mode > 5 {
		return errors.New("incorrect mode")
	}
	y.send("set_power", []any{state, y.efx, y.duration, mode})
	return nil
}

func (y *yeelightApi) On() error {
	return y.SetPower("on", 0)
}

func (y *yeelightApi) Off() error {
	return y.SetPower("off", 0)
}

// This method is used to change the color temperature of a smart LED.

//         Args:
//             ct (int): The target color temperature.
//                 The type is integer and range is 1700 ~ 6500 (k).

//             efx (:obj:str, optional): support two values: sudden and smooth.
//                 If effect is sudden, then change will be directly , under this case, parameter duration is ignored.
//                 If effect is smooth, then the total time of gradual change is specified in parameter duration.
//                 Default is smooth

// duration (:obj:int, optional): Specifies the total time of the gradual changing.
//
//	The unit is milliseconds. The minimum support duration is 30 milliseconds.
//	Default is 500
func (y *yeelightApi) SetCtAbx(ct int) {
	y.send("set_ct_abx", []any{ct, y.efx, y.duration})
}

// This method is used to change the color temperature of a smart LED with percent scale.

// Args:
//
//	pc (int): Percentage target color temperature.
//	    The type is integer and range is 0 ~ 100 (%).
func (y *yeelightApi) SetCtPc(pc int) {
	colorTemp := y.MinCt + ((y.MaxCt - y.MinCt) * pc / 100)
	y.SetCtAbx(colorTemp)
}

// This method is used to change the color of a smart LED.

// Args:
//
//	rgb (int): Color value in RGB
func (y *yeelightApi) SetColor(rgb int) {
	y.send("set_rgb", []any{rgb, y.efx, y.duration})
}

// This method is used to change the color of a smart LED.

// Args:
//
//	red int: Red color value from 0 to 255.
//	green int: Green color value from 0 to 255.
//	blue int: Blue color value from 0 to 255.
func (y *yeelightApi) SetRGB(red, green, blue int) {
	rgb := (red << 16) + (green << 8) + blue
	y.send("set_rgb", []any{rgb, y.efx, y.duration})
}

// This method is used to save current state of smart LED in persistent memory.
// So if user powers off and then powers on the smart LED again (hard power reset),
// the smart LED will show last saved state.
func (y *yeelightApi) SetDefault() {
	y.send("set_default", nil)
}

func (y *yeelightApi) send(method string, params []any) (*cmdResult, error) {
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

type Mono struct {
	devices.BaseDevice
	api yeelightApi
	addr string
}

func (m *Mono) Setup(devInfo devices.DeviceInfo) error {
	m.CreateStatus(devInfo)
	m.Status.RegisterAttribute("addr", "")
	m.Status.RegisterAttribute("color_mode", 0)
	m.api = *newYeelightApi("")
	return nil
}

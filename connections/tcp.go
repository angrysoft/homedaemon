package connections

import (
	"bufio"
	"net"
	"time"
)

type TcpConnection struct {
	Addr string
	conn net.Conn
}

func NewTcpConnection(addr string) *TcpConnection {

	tcp := &TcpConnection{
		Addr: addr,
	}

	return tcp
}

func (t *TcpConnection) Send(msg []byte, delay time.Duration) error {
	conn, err := net.Dial("tcp", t.Addr)
	if err != nil {
		return err
	}
	time.Sleep(delay * time.Second)
	conn.SetWriteDeadline(time.Now().Add(5 * time.Second))
	conn.SetReadDeadline(time.Now().Add(5 * time.Second))
	_, err = conn.Write(msg)
	if err != nil {
		return err
	}
	t.conn = conn
	return nil
}

func (t *TcpConnection) Recv() ([]byte, error) {
	result, err := bufio.NewReader(t.conn).ReadString('\n')
	return []byte(result), err
}

func (t *TcpConnection) Close() error {
	return t.conn.Close()
}

package ovh.angrysoft.homedaemon.automation.actions;

import java.util.List;

public class Execute {
    private String sid;
    private String cmd;
    private List<Object> args;
    
    public Execute(String sid, String cmd, List<Object> args) {
        this.sid = sid;
        this.cmd = cmd;
        this.args = args;
    }
    
    public String getSid() {
        return sid;
    }
    public String getCmd() {
        return cmd;
    }
    public List<Object> getArgs() {
        return args;
    }
}

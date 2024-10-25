package ovh.angrysoft.homedaemon.connections;

public class IdGen {
    private int id;

    public IdGen() {
        this.id = 0;
    }

    public int getId() {
        ++id;
        if (id > 1000) {
            id = 1;
        }
        return id;
    }
}

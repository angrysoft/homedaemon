package ovh.angrysoft.homedaemon.connections.ewelink;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import com.google.gson.Gson;
import ovh.angrysoft.homedaemon.connections.HttpConnection;

public class UserApi {
    HttpConnection hConnection;
    String apiUri = "https://eu-apia.coolkit.cc/v2";
    List<String> defaultHeaders;
    Map<String, String> auth;
    String appSecret;

    public UserApi(String email, String password, String contryCode, String appID,
            String appSecret) {
        this.defaultHeaders = new ArrayList<>();
        this.defaultHeaders.add("Accept");
        this.defaultHeaders.add("application/json");
        this.defaultHeaders.add("Content-Type");
        this.defaultHeaders.add("application/json");
        this.defaultHeaders.add("X-CK-Appid");
        this.defaultHeaders.add(appID);

        this.appSecret = appSecret;

        this.hConnection = new HttpConnection();

        this.auth = new HashMap<>();
        this.auth.put("email", email);
        this.auth.put("password", password);
        this.auth.put("countryCode", contryCode);
        this.auth.put("appid", appID);
    }

    public String getRegion() {
        List<String> headers = new ArrayList<>(defaultHeaders);
        Gson gson = new Gson();
        String data = gson.toJson(auth);
        headers.add("Authorization");
        headers.add(String.format("Sign %s", AuthToken.getToken(data, appSecret)));
        return hConnection.get(apiUri + "/utils/get-region", headers.toArray(new String[0]));
    }

    public String login() {
        List<String> headers = new ArrayList<>(defaultHeaders);
        Gson gson = new Gson();
        String data = gson.toJson(auth);
        headers.add("Authorization");
        headers.add(String.format("Sign %s", AuthToken.getToken(data, appSecret)));
        return hConnection.post(apiUri + "/user/login", data, headers.toArray(new String[0]));
    }
}

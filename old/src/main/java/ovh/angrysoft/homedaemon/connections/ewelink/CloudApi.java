package ovh.angrysoft.homedaemon.connections.ewelink;

import java.util.ArrayList;
import java.util.Optional;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import com.google.gson.Gson;
import ovh.angrysoft.homedaemon.connections.HttpConnection;

public class CloudApi {
    HttpConnection hConnection;
    Gson json = new Gson();
    String apiUri = "https://eu-apia.coolkit.cc/v2";
    List<String> defaultHeaders;
    Map<String, String> auth;
    String appSecret;
    String accessToken = "";
    String refreshToken = "";

    public static final class Builder {
        Optional<String> email = Optional.empty();
        Optional<String> phone = Optional.empty();
        String password;
        String countryCode;
        String appId;
        String appSecret;

        public Builder email(String email) {
            this.email = Optional.of(email);
            return this;
        }

        public Builder phone(String phone) {
            this.phone = Optional.of(phone);
            return this;
        }

        public Builder password(String password) {
            this.password = password;
            return this;
        }

        public Builder countryCode(String countryCode) {
            this.countryCode = countryCode;
            return this;
        }

        public Builder appId(String appId) {
            this.appId = appId;
            return this;
        }

        public Builder appSecret(String appSecret) {
            this.appSecret = appSecret;
            return this;
        }

        public CloudApi build() {
            CloudApi cloudApi = new CloudApi();
            cloudApi.defaultHeaders.add("X-CK-Appid");
            cloudApi.defaultHeaders.add(appId);
            cloudApi.appSecret = appSecret;
            phone.ifPresent(pn -> cloudApi.auth.put("phoneNumber", pn));
            email.ifPresent(em -> cloudApi.auth.put("email", em));
            cloudApi.auth.put("password", password);
            cloudApi.auth.put("countryCode", countryCode);
            return cloudApi;
        }

    }

    private CloudApi() {
        this.defaultHeaders = new ArrayList<>();
        this.defaultHeaders.add("Accept");
        this.defaultHeaders.add("application/json");
        this.defaultHeaders.add("Content-Type");
        this.defaultHeaders.add("application/json");

        this.hConnection = new HttpConnection();

        this.auth = new HashMap<>();
    }

    public String getRegion() {
        List<String> headers = new ArrayList<>(defaultHeaders);
        Gson gson = new Gson();
        String data = gson.toJson(auth);
        headers.add("Authorization");
        headers.add(String.format("Sign %s", AuthUtils.getAuthToken(data, appSecret)));
        return hConnection.get(apiUri + "/utils/get-region", headers.toArray(new String[0]));
    }

    public Boolean login() {
        List<String> headers = new ArrayList<>(defaultHeaders);
        Gson gson = new Gson();
        String data = gson.toJson(auth);
        headers.add("Authorization");
        headers.add(String.format("Sign %s", AuthUtils.getAuthToken(data, appSecret)));
        String callResult =
                hConnection.post(apiUri + "/user/login", data, headers.toArray(new String[0]));
        UserResponse response = json.fromJson(callResult, UserResponse.class);
        if (response.error() != 0) {
            return false;
        }

        accessToken = response.data().at();
        refreshToken = response.data().rt();
        return true;
    }

    public DeviceList getDevices() {
        List<String> headers = new ArrayList<>(defaultHeaders);
        headers.add("Authorization");
        headers.add(String.format("Bearer %s", accessToken));
        String callResult =
                hConnection.get(apiUri + "/device/thing", headers.toArray(new String[0]));
        DeviceResponse response = json.fromJson(callResult, DeviceResponse.class);
        if (response.error() != 0) {
            return null;
        }
        return response.data();
    }
}


/**
 * Response
 */
record UserResponse(int error, String msg, UserProfile data) {
}


record UserProfile(User user, String at, String rt, String region) {
}


record User(String countryCode, String phoneNumber, String email, String apikey, String nickname,
        String wxServiceId, String wxAppId, String wxId, String wxOpenId, Object yanKanYunInfo,
        int accountLevel, Long levelExpiredAt, boolean denyRecharge, boolean accountConsult,
        String ipCountry) {
}


record DeviceResponse(int error, String msg, DeviceList data) {
}


record DeviceList(List<ThingItem> thingList, int total) {
}


record ThingItem(int itemType, ItemData itemData, int index) {
}


record ItemData(String name, String deviceid, Extra extra, String brandName, String brandLogo,
        boolean showBrand, String productModel, List<Object> devGroups, Object tags,
        Object devConfig, Object settings, Object family, Object sharedBy, List<Object> shareTo,
        String devicekey, boolean online, Object params, Object gsminfoData) {
}


record Extra(String model, String ui, long uiid, String description, String manufacturer,
        String mac, String apmac, String modelInfo, String brandId, String chidid) {
}


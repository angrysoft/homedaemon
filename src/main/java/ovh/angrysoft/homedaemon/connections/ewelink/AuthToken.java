package ovh.angrysoft.homedaemon.connections.ewelink;

import java.security.InvalidKeyException;
import java.security.NoSuchAlgorithmException;
import javax.crypto.Mac;
import javax.crypto.spec.SecretKeySpec;
import java.util.Base64;
import java.util.Base64.Encoder;

public final class AuthToken {

    public static String getToken(String data, String key) {
        String result = "";
        final String ALGORITHM = "HmacSHA256";
        SecretKeySpec secretKeySpec = new SecretKeySpec(key.getBytes(), ALGORITHM);
        Mac mac;
        Encoder b64encoder = Base64.getEncoder();
        try {
            mac = Mac.getInstance(ALGORITHM);
            mac.init(secretKeySpec);
            result = new String(b64encoder.encode(mac.doFinal(data.getBytes())));
        } catch (NoSuchAlgorithmException | InvalidKeyException e) {
            e.printStackTrace();
        }
        return result;
    }
}

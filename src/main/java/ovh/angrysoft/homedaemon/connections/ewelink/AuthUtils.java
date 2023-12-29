package ovh.angrysoft.homedaemon.connections.ewelink;

import java.security.AlgorithmParameters;
import java.security.InvalidAlgorithmParameterException;
import java.security.InvalidKeyException;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.security.spec.InvalidParameterSpecException;
import java.util.Base64;
import java.util.Base64.Decoder;
import java.util.Base64.Encoder;
import javax.crypto.BadPaddingException;
import javax.crypto.Cipher;
import javax.crypto.IllegalBlockSizeException;
import javax.crypto.Mac;
import javax.crypto.NoSuchPaddingException;
import javax.crypto.SecretKey;
import javax.crypto.spec.IvParameterSpec;
import javax.crypto.spec.SecretKeySpec;

public final class AuthUtils {
    static final String AES = "AES/CBC/PKCS5Padding";

    static String encryptBase64(byte[] input) {
        Encoder enc = Base64.getEncoder();
        return enc.encodeToString(input);
    }

    static String encryptBase64(String inputString) {
        return encryptBase64(inputString.getBytes());
    }

    static byte[] decryptBase64(String inputBase64String) {
        Decoder dec = Base64.getDecoder();
        return dec.decode(inputBase64String);
    }

    static SecretKey gSecretKey(String key) {

        try {
            MessageDigest digest = MessageDigest.getInstance("MD5");
            digest.update(key.getBytes());
            return new SecretKeySpec(digest.digest(), "AES");
        } catch (NoSuchAlgorithmException e) {
            e.printStackTrace();
        }
        return null;
    }

    static String[] encryptData(String data, String key) {
        String[] result = new String[2];
        try {
            Cipher cipher = Cipher.getInstance(AES);
            cipher.init(Cipher.ENCRYPT_MODE, gSecretKey(key));
            AlgorithmParameters aParameters = cipher.getParameters();
            byte[] iv = aParameters.getParameterSpec(IvParameterSpec.class).getIV();
            result[0] = encryptBase64(cipher.doFinal(data.getBytes())); // payload
            result[1] = encryptBase64(iv); // iv
        } catch (NoSuchAlgorithmException | NoSuchPaddingException | InvalidKeyException
                | IllegalBlockSizeException | BadPaddingException
                | InvalidParameterSpecException e) {
            e.printStackTrace();
        }

        return result;
    }

    static String decryptData(String data, String key, String iv) {
        String result = "";
        try {
            Cipher cipher = Cipher.getInstance(AES);
            IvParameterSpec ivSpec = new IvParameterSpec(decryptBase64(iv));
            cipher.init(Cipher.DECRYPT_MODE, gSecretKey(key), ivSpec);
            result = new String(cipher.doFinal(decryptBase64(data)));
        } catch (InvalidKeyException | NoSuchAlgorithmException | NoSuchPaddingException
                | IllegalBlockSizeException | BadPaddingException
                | InvalidAlgorithmParameterException e) {
            e.printStackTrace();
        }
        return result;
    }

    public static String getAuthToken(String data, String key) {
        String result = "";
        final String ALGORITHM = "HmacSHA256";
        SecretKeySpec secretKeySpec = new SecretKeySpec(key.getBytes(), ALGORITHM);
        Mac mac;
        Encoder b64encoder = Base64.getEncoder();
        try {
            mac = Mac.getInstance(ALGORITHM);
            mac.init(secretKeySpec);
            result = b64encoder.encodeToString(mac.doFinal(data.getBytes()));
        } catch (NoSuchAlgorithmException | InvalidKeyException e) {
            e.printStackTrace();
        }
        return result;
    }
}

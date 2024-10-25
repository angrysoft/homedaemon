package ovh.angrysoft.homedaemon.devices.xiaomi.miio;

import java.security.InvalidAlgorithmParameterException;
import java.security.InvalidKeyException;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import javax.crypto.BadPaddingException;
import javax.crypto.Cipher;
import javax.crypto.IllegalBlockSizeException;
import javax.crypto.NoSuchPaddingException;
import javax.crypto.spec.IvParameterSpec;
import javax.crypto.spec.SecretKeySpec;

/**
 * MioPacket
 */
class MiioPacket {
    private byte[] token;
    private SecretKeySpec key;
    private IvParameterSpec iv;
    private static final String ALGORITHM = "AES/CBC/PKCS5Padding";
    private static final byte[] EMPTY_ARRAY = new byte[] {};

    public MiioPacket(String token) {
        this.token = this.prepareToken(token);
        byte[] keyMd5sum = md5sum(this.token);
        this.key = new SecretKeySpec(keyMd5sum, "AES");
        byte[] kayAndIv = new byte[keyMd5sum.length + this.token.length];
        System.arraycopy(keyMd5sum, 0, kayAndIv, 0, keyMd5sum.length);
        System.arraycopy(this.token, 0, kayAndIv, keyMd5sum.length, this.token.length);
        this.iv = new IvParameterSpec(md5sum(kayAndIv));

    }

    private byte[] prepareToken(String token) {
        StringBuilder result = new StringBuilder();
        for (byte b: token.getBytes()) {
            result.append(String.format("%02x", b));
        }
        return result.toString().getBytes();
    }

    private byte[] md5sum(byte[] input) {
        byte[] result = new byte[] {};
        MessageDigest md;
        try {
            md = MessageDigest.getInstance("MD5");
            md.update(input);
            result = md.digest();
        } catch (NoSuchAlgorithmException e) {
            e.printStackTrace();
        }
        return result;
    }

    byte[] encrypt(byte[] msg) {
        if (msg == null)
            return EMPTY_ARRAY;

        Cipher cipher;
        try {
            cipher = Cipher.getInstance(ALGORITHM);
            cipher.init(Cipher.ENCRYPT_MODE, key, iv);
            return cipher.doFinal(msg);
        } catch (NoSuchAlgorithmException | NoSuchPaddingException | InvalidKeyException
                | InvalidAlgorithmParameterException | IllegalBlockSizeException
                | BadPaddingException e) {
            e.printStackTrace();
        }
        return EMPTY_ARRAY;
    }

    byte[] decrypt(byte[] msg) {
        if (msg == null)
            return EMPTY_ARRAY;

        try {
            Cipher cipher = Cipher.getInstance(ALGORITHM);
            cipher.init(Cipher.DECRYPT_MODE, key, iv);
            return cipher.doFinal(msg);
        } catch (NoSuchAlgorithmException | NoSuchPaddingException | InvalidKeyException
                | InvalidAlgorithmParameterException | IllegalBlockSizeException
                | BadPaddingException e) {
            e.printStackTrace();
        }

        return EMPTY_ARRAY;
    }
}

package ovh.angrysoft.homedaemon.integrations.miio;

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
public class MiioPacket {
    private byte[] token;
    private SecretKeySpec key;
    private IvParameterSpec iv;

    public MiioPacket(String token) {
        this.token = token.getBytes();
        byte[] keyMd5sum = md5sum(this.token);
        this.key = new SecretKeySpec(keyMd5sum, "AES");
        byte[] kayAndIv = new byte[keyMd5sum.length + this.token.length];
        System.arraycopy(keyMd5sum, 0, kayAndIv, 0, keyMd5sum.length);
        System.arraycopy(this.token, 0, kayAndIv, keyMd5sum.length, this.token.length);
        this.iv = new IvParameterSpec(md5sum(kayAndIv));

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

    public byte[] encrypt(byte[] msg) {
        if (msg == null)
            return null;
            
        Cipher cipher;
        try {
            cipher = Cipher.getInstance("AES/CBC/PKCS5Padding");
            cipher.init(cipher.ENCRYPT_MODE, key, iv);
            return cipher.doFinal(msg);
        } catch (NoSuchAlgorithmException | NoSuchPaddingException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        } catch (InvalidKeyException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        } catch (InvalidAlgorithmParameterException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        } catch (IllegalBlockSizeException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        } catch (BadPaddingException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        }
        return null;
    }

    public byte[] decrypt(byte[] msg) {
        return null;
    }
}

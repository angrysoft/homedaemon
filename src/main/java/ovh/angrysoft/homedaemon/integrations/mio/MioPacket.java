package ovh.angrysoft.homedaemon.integrations.mio;

import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;

/**
 * MioPacket
 */
public class MioPacket {
    private byte[] token;
    private byte[] key;
    private byte[] iv;

    public MioPacket(String token) {
        this.token = token.getBytes();
        this.key = md5sum(this.token);
        this.iv = md5sum(new byte[this.key.length + this.token.length]);
        
    }
    
    public MioPacket(String token, byte[] packets) {

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
}

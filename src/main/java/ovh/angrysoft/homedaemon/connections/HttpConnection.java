package ovh.angrysoft.homedaemon.connections;

import java.io.IOException;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.net.http.HttpRequest.BodyPublishers;
import java.net.http.HttpResponse.BodyHandlers;
import java.time.Duration;

public class HttpConnection {
    private HttpClient hClient = HttpClient.newHttpClient();
    private Duration timeout = Duration.ofSeconds(5);

    public String get(String uri, String... headers) {
        String result = "";
        HttpRequest httpRequest = HttpRequest.newBuilder().uri(URI.create(uri))
                .timeout(this.timeout).headers(headers).build();
        try {
            HttpResponse<String> response = hClient.send(httpRequest, BodyHandlers.ofString());
            result = response.body();
        } catch (IOException e) {
            e.printStackTrace();
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
        return result;
    }

    public String post(String uri, String data, String... headers) {
        String result = "";
        HttpRequest httpRequest = HttpRequest.newBuilder().uri(URI.create(uri))
                .timeout(this.timeout).headers(headers).POST(BodyPublishers.ofString(data)).build();
        try {
            HttpResponse<String> response = hClient.send(httpRequest, BodyHandlers.ofString());
            result = response.body();
        } catch (IOException e) {
            e.printStackTrace();
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
        return result;
    }

}

package ovh.angrysoft.homedaemon.connections;

import java.io.IOException;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpRequest.BodyPublishers;
import java.net.http.HttpResponse;
import java.net.http.HttpResponse.BodyHandlers;
import java.time.Duration;
import java.util.Optional;

public class HttpConnection {
    private Duration timeout = Duration.ofSeconds(5);

    public String get(String uri) {
        HttpRequest httpRequest =
                HttpRequest.newBuilder().uri(URI.create(uri)).timeout(timeout).build();
        return send(httpRequest);
    }

    public String get(String uri, String... headers) {

        HttpRequest httpRequest = HttpRequest.newBuilder().uri(URI.create(uri))
                .timeout(this.timeout).headers(headers).build();
        return send(httpRequest);
    }


    public String post(String uri, String data) {
        HttpRequest httpRequest = HttpRequest.newBuilder().uri(URI.create(uri))
                .timeout(this.timeout).POST(BodyPublishers.ofString(data)).build();
        return send(httpRequest);
    }

    public String post(String uri, Optional<String> data) {
        HttpRequest httpRequest;
        if (data.isPresent()) {
            httpRequest = HttpRequest.newBuilder().uri(URI.create(uri)).timeout(this.timeout)
                    .POST(BodyPublishers.ofString(data.get())).build();
        } else {
            httpRequest = HttpRequest.newBuilder().uri(URI.create(uri)).timeout(this.timeout)
                    .POST(BodyPublishers.noBody()).build();
        }
        return send(httpRequest);
    }

    public String post(String uri, String data, String... headers) {
        HttpRequest httpRequest = HttpRequest.newBuilder().uri(URI.create(uri))
                .timeout(this.timeout).headers(headers).POST(BodyPublishers.ofString(data)).build();
        return send(httpRequest);
    }

    String send(HttpRequest httpRequest) {
        // FIXME retry
        HttpClient hClient = HttpClient.newHttpClient();
        String result = "";
        try {
            HttpResponse<String> response = hClient.send(httpRequest, BodyHandlers.ofString());
            result = response.body();
        } catch (IOException | InterruptedException e) {
            e.printStackTrace();
        }
        return result;
    }
}

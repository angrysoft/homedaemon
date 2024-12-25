package ovh.angrysoft.homedaemon.configs;

import org.springframework.boot.context.properties.ConfigurationProperties;

@ConfigurationProperties("homed")
public record HomeConfig(String name, String id, String[] io, String automations, boolean debug) {
}

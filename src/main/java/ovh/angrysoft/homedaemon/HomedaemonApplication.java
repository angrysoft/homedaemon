package ovh.angrysoft.homedaemon;

import java.util.concurrent.Executor;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.context.properties.EnableConfigurationProperties;
import org.springframework.context.annotation.Bean;
import org.springframework.modulith.Modulith;
import org.springframework.scheduling.annotation.EnableAsync;
import org.springframework.scheduling.concurrent.ThreadPoolTaskExecutor;
import ovh.angrysoft.homedaemon.configs.HomeConfig;

@Modulith
@EnableAsync
@EnableConfigurationProperties(value = {HomeConfig.class})
public class HomedaemonApplication {

	public static void main(String[] args) {
		SpringApplication.run(HomedaemonApplication.class, args);
	}

    @Bean
	Executor taskExecutor() {
		ThreadPoolTaskExecutor executor = new ThreadPoolTaskExecutor();
		executor.setCorePoolSize(2);
		executor.setMaxPoolSize(2);
		executor.setQueueCapacity(500);
		executor.initialize();
		return executor;
	}

}

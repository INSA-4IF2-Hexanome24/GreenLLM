package GreenLLM.app.config;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.client.RestClient;

@Configuration
public class ApiConfig {

    @Bean
    public RestClient fastapiClient() {
        return RestClient.builder()
                .baseUrl("http://127.0.0.1:8000") // La URL de tu FastAPI
                .build();
    }
}
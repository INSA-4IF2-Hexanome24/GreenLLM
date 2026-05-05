package GreenLLM.app;

import java.math.BigDecimal;
import java.util.List;

import org.springframework.boot.CommandLineRunner;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;

import GreenLLM.app.model.ModelLLM;
import GreenLLM.app.repository.ModelLLMRepository;

@SpringBootApplication
public class AppApplication {

	public static void main(String[] args) {
		SpringApplication.run(AppApplication.class, args);
	}

	@Bean
	CommandLineRunner seedModelLLM(ModelLLMRepository modelLLMRepository) {
		return args -> {
			List<ModelLLM> modeles = List.of(
					new ModelLLM("qwen2.5-7b-instruct", 0.15, new BigDecimal("0.00000020")),
					new ModelLLM("codegemma-7b", 0.15, new BigDecimal("0.00000020")),
					new ModelLLM("gemma-2-9b-it", 0.18, new BigDecimal("0.00000020")),
					new ModelLLM("llama-3.1-8b-instruct", 0.15, new BigDecimal("0.00000020")),
					new ModelLLM("llama3-chatqa-1.5-8b", 0.15, new BigDecimal("0.00000020")),
					new ModelLLM("mistral-7b-instruct-v0.3", 0.15, new BigDecimal("0.00000020")),
					new ModelLLM("mistral-nemo-12b-instruct", 0.25, new BigDecimal("0.00000030")),
					new ModelLLM("mixtral-8x7b-instruct-v0.1", 0.60, new BigDecimal("0.00000060")),
					new ModelLLM("llama-3.3-nemotron-super-49b-v1", 0.80, new BigDecimal("0.00000090")),
					new ModelLLM("llama-3.1-nemotron-51b-instruct", 0.80, new BigDecimal("0.00000090")),
					new ModelLLM("llama3-chatqa-1.5-70b", 0.90, new BigDecimal("0.00000090")),
					new ModelLLM("llama3-70b-instruct", 0.90, new BigDecimal("0.00000090")),
					new ModelLLM("mixtral-8x22b-instruct-v0.1", 1.20, new BigDecimal("0.00000120")),
					new ModelLLM("palmyra-creative-122b", 1.80, new BigDecimal("0.00000180")));

			for (ModelLLM modele : modeles) {
				if (!modelLLMRepository.existsByNom(modele.getNom())) {
					modelLLMRepository.save(modele);
				}
			}
		};
	}
}

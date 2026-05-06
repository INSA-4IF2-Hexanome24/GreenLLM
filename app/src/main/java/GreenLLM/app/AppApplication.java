package GreenLLM.app;

import java.math.BigDecimal;
import java.util.List;

import org.springframework.boot.CommandLineRunner;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;

import GreenLLM.app.model.Adresse;
import GreenLLM.app.model.ModelLLM;
import GreenLLM.app.model.StatutUtilisateur;
import GreenLLM.app.model.Utilisateur;
import GreenLLM.app.repository.ModelLLMRepository;
import GreenLLM.app.repository.UtilisateurRepository;

@SpringBootApplication
public class AppApplication {

	public static void main(String[] args) {
		SpringApplication.run(AppApplication.class, args);
	}

	@Bean
	CommandLineRunner seedData(ModelLLMRepository modelLLMRepository, UtilisateurRepository utilisateurRepository) {
		return args -> {
			List<ModelLLM> modeles = List.of(
					new ModelLLM("GPT-4", 1.20, new BigDecimal("0.000045")),
					new ModelLLM("GPT-4o", 0.95, new BigDecimal("0.00000625")),
					new ModelLLM("GPT-4o-mini", 0.25, new BigDecimal("0.000000375")),
					new ModelLLM("Claude-3-opus", 1.10, new BigDecimal("0.000045")),
					new ModelLLM("Llama-3-70B", 0.60, new BigDecimal("0.000000625")),
					new ModelLLM("Llama-3-8B", 0.15, new BigDecimal("0.000000035")));

			modelLLMRepository.deleteAll();
			modelLLMRepository.saveAll(modeles);

			if (!utilisateurRepository.existsByEmail("employe@greenllm.test")) {
				Utilisateur employe = new Utilisateur(
						"employe@greenllm.test",
						"Employe",
						"Demo",
						"password",
						StatutUtilisateur.EMPLOYE,
						null,
						new Adresse("Lyon", "69000", "France"));
				employe.setBudget(new BigDecimal("100.00"));
				employe.setBudgetConsomme(BigDecimal.ZERO);
				utilisateurRepository.save(employe);
			}

			if (!utilisateurRepository.existsByEmail("chef@greenllm.test")) {
				Utilisateur chef = new Utilisateur(
						"chef@greenllm.test",
						"Chef",
						"Demo",
						"password",
						StatutUtilisateur.CHEF_DEPARTEMENT,
						null,
						new Adresse("Paris", "75000", "France"));
				chef.setBudget(new BigDecimal("500.00"));
				chef.setBudgetConsomme(BigDecimal.ZERO);
				utilisateurRepository.save(chef);
			}
		};
	}
}

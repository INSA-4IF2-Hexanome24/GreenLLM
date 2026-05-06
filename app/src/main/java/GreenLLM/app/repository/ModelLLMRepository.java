package GreenLLM.app.repository;

import org.springframework.data.jpa.repository.JpaRepository;

import GreenLLM.app.model.ModelLLM;

public interface ModelLLMRepository extends JpaRepository<ModelLLM, Long> {

    boolean existsByNom(String nom);
}

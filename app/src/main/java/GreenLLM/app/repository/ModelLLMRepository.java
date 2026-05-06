package GreenLLM.app.repository;

import java.util.Optional;

import org.springframework.data.jpa.repository.JpaRepository;

import GreenLLM.app.model.ModelLLM;

public interface ModelLLMRepository extends JpaRepository<ModelLLM, Long> {

    boolean existsByNom(String nom);

    Optional<ModelLLM> findByNom(String nom);

    Optional<ModelLLM> findByNomIgnoreCase(String nom);
}

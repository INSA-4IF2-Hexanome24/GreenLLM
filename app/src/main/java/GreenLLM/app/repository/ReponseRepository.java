package GreenLLM.app.repository;

import org.springframework.data.jpa.repository.JpaRepository;

import GreenLLM.app.model.Reponse;

public interface ReponseRepository extends JpaRepository<Reponse, Long> {
}

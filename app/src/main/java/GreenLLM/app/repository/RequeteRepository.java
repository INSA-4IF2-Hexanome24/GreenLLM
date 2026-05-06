package GreenLLM.app.repository;

import org.springframework.data.jpa.repository.JpaRepository;

import GreenLLM.app.model.Requete;

public interface RequeteRepository extends JpaRepository<Requete, Long> {
}

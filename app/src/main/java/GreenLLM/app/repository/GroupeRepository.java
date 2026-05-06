package GreenLLM.app.repository;

import org.springframework.data.jpa.repository.JpaRepository;

import GreenLLM.app.model.Groupe;

public interface GroupeRepository extends JpaRepository<Groupe, Long> {
}

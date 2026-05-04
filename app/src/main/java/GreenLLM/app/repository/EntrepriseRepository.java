package GreenLLM.app.repository;

import java.util.Optional;

import org.springframework.data.jpa.repository.JpaRepository;

import GreenLLM.app.model.Entreprise;

public interface EntrepriseRepository extends JpaRepository<Entreprise, Long> {

    Optional<Entreprise> findBySiret(String siret);

    boolean existsBySiret(String siret);
}

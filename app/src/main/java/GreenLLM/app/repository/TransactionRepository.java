package GreenLLM.app.repository;

import java.util.List;

import org.springframework.data.jpa.repository.JpaRepository;

import GreenLLM.app.model.Transaction;

public interface TransactionRepository extends JpaRepository<Transaction, Long> {

    List<Transaction> findByUtilisateurIdOrderByDateCreationDesc(Long utilisateurId);
}

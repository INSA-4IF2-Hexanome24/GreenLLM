package GreenLLM.app.controller;

import java.math.BigDecimal;
import java.util.List;

import org.springframework.data.domain.Sort;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import GreenLLM.app.dto.TransactionCreateRequest;
import GreenLLM.app.dto.TransactionResponse;
import GreenLLM.app.model.ModelLLM;
import GreenLLM.app.model.Reponse;
import GreenLLM.app.model.Requete;
import GreenLLM.app.model.Transaction;
import GreenLLM.app.model.Utilisateur;
import GreenLLM.app.repository.ModelLLMRepository;
import GreenLLM.app.repository.ReponseRepository;
import GreenLLM.app.repository.RequeteRepository;
import GreenLLM.app.repository.TransactionRepository;
import GreenLLM.app.repository.UtilisateurRepository;
import GreenLLM.app.service.BudgetService;

@RestController
@RequestMapping("/api/transactions")
public class TransactionController {

    private final TransactionRepository transactionRepository;
    private final UtilisateurRepository utilisateurRepository;
    private final ModelLLMRepository modelLLMRepository;
    private final RequeteRepository requeteRepository;
    private final ReponseRepository reponseRepository;
    private final BudgetService budgetService;

    public TransactionController(TransactionRepository transactionRepository,
                                 UtilisateurRepository utilisateurRepository,
                                 ModelLLMRepository modelLLMRepository,
                                 RequeteRepository requeteRepository,
                                 ReponseRepository reponseRepository,
                                 BudgetService budgetService) {
        this.transactionRepository = transactionRepository;
        this.utilisateurRepository = utilisateurRepository;
        this.modelLLMRepository = modelLLMRepository;
        this.requeteRepository = requeteRepository;
        this.reponseRepository = reponseRepository;
        this.budgetService = budgetService;
    }

    @PostMapping
    public ResponseEntity<TransactionResponse> creerTransaction(@RequestBody TransactionCreateRequest request) {
        Utilisateur utilisateur = utilisateurRepository.findById(request.getUtilisateurId())
                .orElseThrow(() -> new IllegalArgumentException("Utilisateur introuvable"));
        ModelLLM modelLLM = modelLLMRepository.findById(request.getModelId())
                .orElseThrow(() -> new IllegalArgumentException("Modele introuvable"));
        Requete requete = requeteRepository.findById(request.getRequeteId())
                .orElseThrow(() -> new IllegalArgumentException("Requete introuvable"));
        Reponse reponse = reponseRepository.findById(request.getReponseId())
                .orElseThrow(() -> new IllegalArgumentException("Reponse introuvable"));

        if (requete.getUser() != null && !utilisateur.getId().equals(requete.getUser().getId())) {
            throw new IllegalArgumentException("La requete n'appartient pas a cet utilisateur");
        }

        BigDecimal budgetConsommeAvant = valeur(utilisateur.getBudgetConsomme());
        BigDecimal cout = budgetService.chercherCoutPourUneRequete(modelLLM, requete, reponse);
        budgetService.ajouterConsommation(utilisateur, cout);

        requeteRepository.save(requete);
        Utilisateur savedUtilisateur = utilisateurRepository.save(utilisateur);

        Transaction transaction = new Transaction(
                savedUtilisateur,
                modelLLM,
                requete,
                reponse,
                cout,
                budgetConsommeAvant,
                valeur(savedUtilisateur.getBudgetConsomme()));

        Transaction savedTransaction = transactionRepository.save(transaction);
        return ResponseEntity.status(HttpStatus.CREATED).body(toResponse(savedTransaction));
    }

    @GetMapping
    public ResponseEntity<List<TransactionResponse>> listerTransactions() {
        List<TransactionResponse> transactions = transactionRepository
                .findAll(Sort.by(Sort.Direction.DESC, "dateCreation"))
                .stream()
                .map(this::toResponse)
                .toList();

        return ResponseEntity.ok(transactions);
    }

    @GetMapping("/{transactionId}")
    public ResponseEntity<TransactionResponse> chercherTransaction(@PathVariable Long transactionId) {
        Transaction transaction = transactionRepository.findById(transactionId)
                .orElseThrow(() -> new IllegalArgumentException("Transaction introuvable"));

        return ResponseEntity.ok(toResponse(transaction));
    }

    @GetMapping("/utilisateurs/{utilisateurId}")
    public ResponseEntity<List<TransactionResponse>> listerTransactionsUtilisateur(@PathVariable Long utilisateurId) {
        if (!utilisateurRepository.existsById(utilisateurId)) {
            throw new IllegalArgumentException("Utilisateur introuvable");
        }

        List<TransactionResponse> transactions = transactionRepository
                .findByUtilisateurIdOrderByDateCreationDesc(utilisateurId)
                .stream()
                .map(this::toResponse)
                .toList();

        return ResponseEntity.ok(transactions);
    }

    private TransactionResponse toResponse(Transaction transaction) {
        return new TransactionResponse(
                transaction.getId(),
                transaction.getUtilisateur() != null ? transaction.getUtilisateur().getId() : null,
                transaction.getModelLLM() != null ? transaction.getModelLLM().getId() : null,
                transaction.getRequete() != null ? transaction.getRequete().getId() : null,
                transaction.getReponse() != null ? transaction.getReponse().getId() : null,
                transaction.getCoutAjoute(),
                transaction.getBudgetConsommeAvant(),
                transaction.getBudgetConsommeApres(),
                transaction.getDateCreation());
    }

    private BigDecimal valeur(BigDecimal montant) {
        return montant != null ? montant : BigDecimal.ZERO;
    }
}

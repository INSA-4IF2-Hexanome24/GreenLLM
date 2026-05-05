package GreenLLM.app.controller;

import java.math.BigDecimal;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import GreenLLM.app.dto.CoutConsommationResponse;
import GreenLLM.app.dto.CoutEconomiseResponse;
import GreenLLM.app.model.ModelLLM;
import GreenLLM.app.model.Reponse;
import GreenLLM.app.model.Requete;
import GreenLLM.app.model.Utilisateur;
import GreenLLM.app.repository.ModelLLMRepository;
import GreenLLM.app.repository.ReponseRepository;
import GreenLLM.app.repository.RequeteRepository;
import GreenLLM.app.repository.UtilisateurRepository;
import GreenLLM.app.service.BudgetService;

@RestController
@RequestMapping("/api/budget")
public class BudgetController {

    private final BudgetService budgetService;
    private final UtilisateurRepository utilisateurRepository;
    private final RequeteRepository requeteRepository;
    private final ReponseRepository reponseRepository;
    private final ModelLLMRepository modelLLMRepository;

    public BudgetController(BudgetService budgetService,
                            UtilisateurRepository utilisateurRepository,
                            RequeteRepository requeteRepository,
                            ReponseRepository reponseRepository,
                            ModelLLMRepository modelLLMRepository) {
        this.budgetService = budgetService;
        this.utilisateurRepository = utilisateurRepository;
        this.requeteRepository = requeteRepository;
        this.reponseRepository = reponseRepository;
        this.modelLLMRepository = modelLLMRepository;
    }

    @PostMapping("/utilisateurs/{utilisateurId}/modeles/{modelId}/requetes/{requeteId}/reponses/{reponseId}/consommation")
    public ResponseEntity<CoutConsommationResponse> ajouterCoutRequeteUtilisateur(
            @PathVariable Long utilisateurId,
            @PathVariable Long modelId,
            @PathVariable Long requeteId,
            @PathVariable Long reponseId) {
        Utilisateur utilisateur = utilisateurRepository.findById(utilisateurId)
                .orElseThrow(() -> new IllegalArgumentException("Utilisateur introuvable"));
        ModelLLM modelLLM = modelLLMRepository.findById(modelId)
                .orElseThrow(() -> new IllegalArgumentException("Modele introuvable"));
        Requete requete = requeteRepository.findById(requeteId)
                .orElseThrow(() -> new IllegalArgumentException("Requete introuvable"));
        Reponse reponse = reponseRepository.findById(reponseId)
                .orElseThrow(() -> new IllegalArgumentException("Reponse introuvable"));

        if (requete.getUser() != null && !utilisateur.getId().equals(requete.getUser().getId())) {
            throw new IllegalArgumentException("La requete n'appartient pas a cet utilisateur");
        }

        BigDecimal cout = budgetService.chercherCoutPourUneRequete(modelLLM, requete, reponse);
        budgetService.ajouterConsommation(utilisateur, cout);

        requeteRepository.save(requete);
        Utilisateur savedUtilisateur = utilisateurRepository.save(utilisateur);

        CoutConsommationResponse response = new CoutConsommationResponse(
                savedUtilisateur.getId(),
                requete.getId(),
                reponse.getId(),
                cout,
                savedUtilisateur.getBudgetConsomme());

        return ResponseEntity.ok(response);
    }

    @GetMapping("/modeles/{modelId}/requetes/{requeteId}/reponses/{reponseId}/cout-economise")
    public ResponseEntity<CoutEconomiseResponse> calculerCoutEconomise(
            @PathVariable Long modelId,
            @PathVariable Long requeteId,
            @PathVariable Long reponseId) {
        ModelLLM modelLLM = modelLLMRepository.findById(modelId)
                .orElseThrow(() -> new IllegalArgumentException("Modele introuvable"));
        Requete requete = requeteRepository.findById(requeteId)
                .orElseThrow(() -> new IllegalArgumentException("Requete introuvable"));
        Reponse reponse = reponseRepository.findById(reponseId)
                .orElseThrow(() -> new IllegalArgumentException("Reponse introuvable"));

        BigDecimal coutEconomise = budgetService.calculCoutEconomise(modelLLM, requete, reponse);

        CoutEconomiseResponse response = new CoutEconomiseResponse(
                modelLLM.getId(),
                requete.getId(),
                reponse.getId(),
                coutEconomise);

        return ResponseEntity.ok(response);
    }
}

package GreenLLM.app.controller;

import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import GreenLLM.app.dto.RequeteCreateRequest;
import GreenLLM.app.dto.RequeteResponse;
import GreenLLM.app.model.Requete;
import GreenLLM.app.model.Utilisateur;
import GreenLLM.app.repository.RequeteRepository;
import GreenLLM.app.repository.UtilisateurRepository;

@RestController
@RequestMapping("/api/requetes")
public class RequeteController {

    private final RequeteRepository requeteRepository;
    private final UtilisateurRepository utilisateurRepository;

    public RequeteController(RequeteRepository requeteRepository, UtilisateurRepository utilisateurRepository) {
        this.requeteRepository = requeteRepository;
        this.utilisateurRepository = utilisateurRepository;
    }

    @PostMapping
    public ResponseEntity<RequeteResponse> creerRequete(@RequestBody RequeteCreateRequest request) {
        Utilisateur utilisateur = utilisateurRepository.findById(request.getUtilisateurId())
                .orElseThrow(() -> new IllegalArgumentException("Utilisateur introuvable"));

        Requete requete = new Requete(
                request.getDescription(),
                utilisateur,
                request.getNombreTokens());

        Requete savedRequete = requeteRepository.save(requete);

        RequeteResponse response = new RequeteResponse(
                savedRequete.getId(),
                savedRequete.getDescription(),
                savedRequete.getNombreTokens(),
                savedRequete.getCoutTotal(),
                utilisateur.getId());

        return ResponseEntity.status(HttpStatus.CREATED).body(response);
    }
}

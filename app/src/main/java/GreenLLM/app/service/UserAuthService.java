package GreenLLM.app.service;

import java.math.BigDecimal;

import org.springframework.stereotype.Service;

import GreenLLM.app.dto.AuthResponse;
import GreenLLM.app.dto.UserLoginRequest;
import GreenLLM.app.dto.UserRegisterRequest;
import GreenLLM.app.model.StatutUtilisateur;
import GreenLLM.app.model.Utilisateur;
import GreenLLM.app.repository.UtilisateurRepository;

@Service
public class UserAuthService {

    private final UtilisateurRepository utilisateurRepository;

    public UserAuthService(UtilisateurRepository utilisateurRepository) {
        this.utilisateurRepository = utilisateurRepository;
    }

    public AuthResponse register(UserRegisterRequest request) {
        if (utilisateurRepository.existsByEmail(request.getEmail())) {
            throw new IllegalArgumentException("Email deja utilise");
        }

        StatutUtilisateur statut = request.getStatut() != null
                ? request.getStatut()
                : StatutUtilisateur.EMPLOYE;

        Utilisateur utilisateur = new Utilisateur(
                request.getEmail(),
                request.getPrenom(),
                request.getNom(),
                request.getMotDePasse(),
                statut,
                null,
                request.getAdresse());
        utilisateur.setBudget(valeur(request.getBudget()));
        utilisateur.setBudgetConsomme(BigDecimal.ZERO);

        Utilisateur savedUtilisateur = utilisateurRepository.save(utilisateur);
        return new AuthResponse(savedUtilisateur.getId(), "USER", "Utilisateur cree");
    }

    public AuthResponse login(UserLoginRequest request) {
        Utilisateur utilisateur = utilisateurRepository.findByEmail(request.getEmail())
                .orElseThrow(() -> new IllegalArgumentException("Identifiants invalides"));

        if (!utilisateur.getMotDePasse().equals(request.getMotDePasse())) {
            throw new IllegalArgumentException("Identifiants invalides");
        }

        return new AuthResponse(utilisateur.getId(), "USER", "Connexion utilisateur reussie");
    }

    private BigDecimal valeur(BigDecimal montant) {
        return montant != null ? montant : BigDecimal.ZERO;
    }
}

package GreenLLM.app.service;

import org.springframework.stereotype.Service;

import GreenLLM.app.dto.AuthResponse;
import GreenLLM.app.dto.EntrepriseLoginRequest;
import GreenLLM.app.dto.EntrepriseRegisterRequest;
import GreenLLM.app.model.Entreprise;
import GreenLLM.app.repository.EntrepriseRepository;

@Service
public class EntrepriseAuthService {

    private final EntrepriseRepository entrepriseRepository;

    public EntrepriseAuthService(EntrepriseRepository entrepriseRepository) {
        this.entrepriseRepository = entrepriseRepository;
    }

    public AuthResponse register(EntrepriseRegisterRequest request) {
        if (entrepriseRepository.existsBySiret(request.getSiret())) {
            throw new IllegalArgumentException("SIRET deja utilise");
        }

        Entreprise entreprise = new Entreprise(
                request.getSiret(),
                request.getDomaine(),
                request.getMotDePasse());

        Entreprise savedEntreprise = entrepriseRepository.save(entreprise);
        return new AuthResponse(savedEntreprise.getId(), "ENTREPRISE", "Entreprise creee");
    }

    public AuthResponse login(EntrepriseLoginRequest request) {
        Entreprise entreprise = entrepriseRepository.findBySiret(request.getSiret())
                .orElseThrow(() -> new IllegalArgumentException("Identifiants invalides"));

        if (!entreprise.getMotDePasse().equals(request.getMotDePasse())) {
            throw new IllegalArgumentException("Identifiants invalides");
        }

        return new AuthResponse(entreprise.getId(), "ENTREPRISE", "Connexion entreprise reussie");
    }
}

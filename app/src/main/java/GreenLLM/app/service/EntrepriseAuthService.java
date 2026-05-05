package GreenLLM.app.service;

import java.math.BigDecimal;
import java.util.HashSet;
import java.util.Set;

import org.springframework.stereotype.Service;

import GreenLLM.app.dto.AuthResponse;
import GreenLLM.app.dto.EntrepriseLoginRequest;
import GreenLLM.app.dto.EntrepriseRegisterRequest;
import GreenLLM.app.dto.GroupeRegisterRequest;
import GreenLLM.app.model.Entreprise;
import GreenLLM.app.model.Groupe;
import GreenLLM.app.repository.EntrepriseRepository;
import GreenLLM.app.repository.GroupeRepository;

@Service
public class EntrepriseAuthService {

    private final EntrepriseRepository entrepriseRepository;
    private final GroupeRepository groupeRepository;

    public EntrepriseAuthService(EntrepriseRepository entrepriseRepository, GroupeRepository groupeRepository) {
        this.entrepriseRepository = entrepriseRepository;
        this.groupeRepository = groupeRepository;
    }

    public AuthResponse register(EntrepriseRegisterRequest request) {
        if (entrepriseRepository.existsBySiret(request.getSiret())) {
            throw new IllegalArgumentException("SIRET deja utilise");
        }

        Entreprise entreprise = new Entreprise(
                request.getSiret(),
                request.getDomaine(),
                request.getMotDePasse());
        entreprise.setBudget(valeur(request.getBudget()));
        entreprise.setBudgetConsomme(BigDecimal.ZERO);
        entreprise.setGroupes(ajouterGroupesEntreprise(request));

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

    public Set<Groupe> ajouterGroupesEntreprise(EntrepriseRegisterRequest request) {
        Set<Groupe> groupes = new HashSet<>();

        if (request.getGroupes() == null) {
            return groupes;
        }

        for (GroupeRegisterRequest groupeRequest : request.getGroupes()) {
            Groupe groupe = new Groupe();
            groupe.setDescription(groupeRequest.getDescription());
            groupe.setDepartement(groupeRequest.getDepartement());
            groupe.setNiveauGroupe(groupeRequest.getNiveauGroupe());
            groupe.setBudget(valeur(groupeRequest.getBudget()));
            groupe.setBudgetConsomme(BigDecimal.ZERO);
            groupes.add(groupeRepository.save(groupe));
        }

        return groupes;
    }

    private BigDecimal valeur(BigDecimal montant) {
        return montant != null ? montant : BigDecimal.ZERO;
    }
}

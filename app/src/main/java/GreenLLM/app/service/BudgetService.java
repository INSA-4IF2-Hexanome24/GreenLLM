package GreenLLM.app.service;

import java.math.BigDecimal;
import java.math.RoundingMode;
import java.util.List;

import org.springframework.stereotype.Service;

import GreenLLM.app.model.Entreprise;
import GreenLLM.app.model.Groupe;
import GreenLLM.app.model.ModelLLM;
import GreenLLM.app.model.Reponse;
import GreenLLM.app.model.Requete;
import GreenLLM.app.model.Utilisateur;
import GreenLLM.app.repository.ModelLLMRepository;

@Service
public class BudgetService {

    private final ModelLLMRepository modelLLMRepository;

    public BudgetService(ModelLLMRepository modelLLMRepository) {
        this.modelLLMRepository = modelLLMRepository;
    }

    public BigDecimal chercherCoutPourUneReponse(ModelLLM modelLLM, Reponse reponse) {
        return calculerCoutModelePourReponse(modelLLM, reponse);
    }

    public BigDecimal chercherCoutPourUneRequete(ModelLLM modelLLM, Requete requete, Reponse reponse) {
        if (modelLLM == null || requete == null) {
            return BigDecimal.ZERO;
        }

        BigDecimal cout = calculerCoutModelePourRequeteEtReponse(modelLLM, requete, reponse);
        requete.setCoutTotal(cout);
        return cout;
    }

    public BigDecimal Chercher_cout_pour_une_requete(ModelLLM modelLLM, Requete requete, Reponse reponse) {
        return chercherCoutPourUneRequete(modelLLM, requete, reponse);
    }

    public BigDecimal calculCoutEconomise(ModelLLM modelLLM, Requete requete, Reponse reponse) {
        if (modelLLM == null || requete == null || reponse == null) {
            return BigDecimal.ZERO;
        }

        List<ModelLLM> modeles = modelLLMRepository.findAll();
        if (modeles.isEmpty()) {
            return BigDecimal.ZERO;
        }

        BigDecimal totalCouts = BigDecimal.ZERO;
        for (ModelLLM modele : modeles) {
            totalCouts = totalCouts.add(calculerCoutModelePourRequeteEtReponse(modele, requete, reponse));
        }

        BigDecimal moyenneCouts = totalCouts.divide(
                BigDecimal.valueOf(modeles.size()),
                10,
                RoundingMode.HALF_UP);
        BigDecimal coutModele = calculerCoutModelePourRequeteEtReponse(modelLLM, requete, reponse);

        return moyenneCouts.subtract(coutModele);
    }

    public BigDecimal calcul_cout_economise(ModelLLM modelLLM, Requete requete, Reponse reponse) {
        return calculCoutEconomise(modelLLM, requete, reponse);
    }

    public boolean verifierBudgetUtilisateur(Utilisateur utilisateur, BigDecimal cout) {
        if (utilisateur == null) {
            return false;
        }

        return budgetDisponible(utilisateur.getBudget(), utilisateur.getBudgetConsomme()).compareTo(valeur(cout)) >= 0;
    }

    public boolean verifierBudgetGroupe(Groupe groupe, BigDecimal cout) {
        if (groupe == null) {
            return false;
        }

        return budgetDisponible(groupe.getBudget(), groupe.getBudgetConsomme()).compareTo(valeur(cout)) >= 0;
    }

    public boolean verifierBudgetEntreprise(Entreprise entreprise, BigDecimal cout) {
        if (entreprise == null) {
            return false;
        }

        return budgetDisponible(entreprise.getBudget(), entreprise.getBudgetConsomme()).compareTo(valeur(cout)) >= 0;
    }

    public void ajouterConsommation(Utilisateur utilisateur, BigDecimal cout) {
        utilisateur.setBudgetConsomme(valeur(utilisateur.getBudgetConsomme()).add(valeur(cout)));
    }

    public void ajouterConsommation(Groupe groupe, BigDecimal cout) {
        groupe.setBudgetConsomme(valeur(groupe.getBudgetConsomme()).add(valeur(cout)));
    }

    public void ajouterConsommation(Entreprise entreprise, BigDecimal cout) {
        entreprise.setBudgetConsomme(valeur(entreprise.getBudgetConsomme()).add(valeur(cout)));
    }

    private BigDecimal budgetDisponible(BigDecimal budget, BigDecimal budgetConsomme) {
        return valeur(budget).subtract(valeur(budgetConsomme));
    }

    private BigDecimal calculerCoutModelePourReponse(ModelLLM modelLLM, Reponse reponse) {
        if (modelLLM == null || reponse == null) {
            return BigDecimal.ZERO;
        }

        return calculerCoutModelePourNombreTokens(modelLLM, reponse.getNombreTokens());
    }

    private BigDecimal calculerCoutModelePourRequeteEtReponse(ModelLLM modelLLM, Requete requete, Reponse reponse) {
        if (modelLLM == null || requete == null || reponse == null) {
            return BigDecimal.ZERO;
        }

        BigDecimal inputCost = calculerCoutModelePourNombreTokens(modelLLM, requete.getNombreTokens());
        BigDecimal outputCost = calculerCoutModelePourNombreTokens(modelLLM, reponse.getNombreTokens());

        return inputCost.add(outputCost);
    }

    private BigDecimal calculerCoutModelePourNombreTokens(ModelLLM modelLLM, int nombreTokens) {
        if (modelLLM == null) {
            return BigDecimal.ZERO;
        }

        return valeur(modelLLM.getCoutParToken()).multiply(BigDecimal.valueOf(nombreTokens));
    }

    private BigDecimal valeur(BigDecimal montant) {
        return montant != null ? montant : BigDecimal.ZERO;
    }
}

package GreenLLM.app.service;

import java.math.BigDecimal;

import org.springframework.stereotype.Service;

import GreenLLM.app.model.Entreprise;
import GreenLLM.app.model.Groupe;
import GreenLLM.app.model.ModelLLM;
import GreenLLM.app.model.Requete;
import GreenLLM.app.model.Utilisateur;

@Service
public class BudgetService {

    public BigDecimal chercherCoutPourUneRequete(Requete requete) {
        if (requete == null || requete.getModelLLM() == null) {
            return BigDecimal.ZERO;
        }

        ModelLLM modelLLM = requete.getModelLLM();
        BigDecimal coutParToken = valeur(modelLLM.getCoutParToken());
        BigDecimal cout = coutParToken.multiply(BigDecimal.valueOf(requete.getNombreTokens()));
        requete.setCoutTotal(cout);
        return cout;
    }

    public BigDecimal Chercher_cout_pour_une_requete(Requete requete) {
        return chercherCoutPourUneRequete(requete);
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

    private BigDecimal valeur(BigDecimal montant) {
        return montant != null ? montant : BigDecimal.ZERO;
    }
}

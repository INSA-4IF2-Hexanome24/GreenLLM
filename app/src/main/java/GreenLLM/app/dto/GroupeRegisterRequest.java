package GreenLLM.app.dto;

import java.math.BigDecimal;

public class GroupeRegisterRequest {

    private String description;
    private String departement;
    private int niveauGroupe;
    private BigDecimal budget;

    public GroupeRegisterRequest() {
    }

    public String getDescription() {
        return description;
    }

    public void setDescription(String description) {
        this.description = description;
    }

    public String getDepartement() {
        return departement;
    }

    public void setDepartement(String departement) {
        this.departement = departement;
    }

    public int getNiveauGroupe() {
        return niveauGroupe;
    }

    public void setNiveauGroupe(int niveauGroupe) {
        this.niveauGroupe = niveauGroupe;
    }

    public BigDecimal getBudget() {
        return budget;
    }

    public void setBudget(BigDecimal budget) {
        this.budget = budget;
    }
}

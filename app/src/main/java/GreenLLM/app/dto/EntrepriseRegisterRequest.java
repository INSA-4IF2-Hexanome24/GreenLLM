package GreenLLM.app.dto;

import java.math.BigDecimal;
import java.util.List;

public class EntrepriseRegisterRequest {

    private String siret;
    private String domaine;
    private String motDePasse;
    private BigDecimal budget;
    private List<GroupeRegisterRequest> groupes;

    public EntrepriseRegisterRequest() {
    }

    public String getSiret() {
        return siret;
    }

    public void setSiret(String siret) {
        this.siret = siret;
    }

    public String getDomaine() {
        return domaine;
    }

    public void setDomaine(String domaine) {
        this.domaine = domaine;
    }

    public String getMotDePasse() {
        return motDePasse;
    }

    public void setMotDePasse(String motDePasse) {
        this.motDePasse = motDePasse;
    }

    public BigDecimal getBudget() {
        return budget;
    }

    public void setBudget(BigDecimal budget) {
        this.budget = budget;
    }

    public List<GroupeRegisterRequest> getGroupes() {
        return groupes;
    }

    public void setGroupes(List<GroupeRegisterRequest> groupes) {
        this.groupes = groupes;
    }
}

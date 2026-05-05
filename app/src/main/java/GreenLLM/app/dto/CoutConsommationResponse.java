package GreenLLM.app.dto;

import java.math.BigDecimal;

public class CoutConsommationResponse {

    private Long utilisateurId;
    private Long requeteId;
    private Long reponseId;
    private BigDecimal coutAjoute;
    private BigDecimal budgetConsomme;

    public CoutConsommationResponse() {
    }

    public CoutConsommationResponse(Long utilisateurId, Long requeteId, Long reponseId,
                                    BigDecimal coutAjoute, BigDecimal budgetConsomme) {
        this.utilisateurId = utilisateurId;
        this.requeteId = requeteId;
        this.reponseId = reponseId;
        this.coutAjoute = coutAjoute;
        this.budgetConsomme = budgetConsomme;
    }

    public Long getUtilisateurId() {
        return utilisateurId;
    }

    public void setUtilisateurId(Long utilisateurId) {
        this.utilisateurId = utilisateurId;
    }

    public Long getRequeteId() {
        return requeteId;
    }

    public void setRequeteId(Long requeteId) {
        this.requeteId = requeteId;
    }

    public Long getReponseId() {
        return reponseId;
    }

    public void setReponseId(Long reponseId) {
        this.reponseId = reponseId;
    }

    public BigDecimal getCoutAjoute() {
        return coutAjoute;
    }

    public void setCoutAjoute(BigDecimal coutAjoute) {
        this.coutAjoute = coutAjoute;
    }

    public BigDecimal getBudgetConsomme() {
        return budgetConsomme;
    }

    public void setBudgetConsomme(BigDecimal budgetConsomme) {
        this.budgetConsomme = budgetConsomme;
    }
}

package GreenLLM.app.dto;

import java.math.BigDecimal;
import java.time.LocalDateTime;

public class TransactionResponse {

    private Long id;
    private Long utilisateurId;
    private Long modelId;
    private Long requeteId;
    private Long reponseId;
    private BigDecimal coutAjoute;
    private BigDecimal budgetConsommeAvant;
    private BigDecimal budgetConsommeApres;
    private LocalDateTime dateCreation;

    public TransactionResponse() {
    }

    public TransactionResponse(Long id, Long utilisateurId, Long modelId, Long requeteId, Long reponseId,
                               BigDecimal coutAjoute, BigDecimal budgetConsommeAvant,
                               BigDecimal budgetConsommeApres, LocalDateTime dateCreation) {
        this.id = id;
        this.utilisateurId = utilisateurId;
        this.modelId = modelId;
        this.requeteId = requeteId;
        this.reponseId = reponseId;
        this.coutAjoute = coutAjoute;
        this.budgetConsommeAvant = budgetConsommeAvant;
        this.budgetConsommeApres = budgetConsommeApres;
        this.dateCreation = dateCreation;
    }

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public Long getUtilisateurId() {
        return utilisateurId;
    }

    public void setUtilisateurId(Long utilisateurId) {
        this.utilisateurId = utilisateurId;
    }

    public Long getModelId() {
        return modelId;
    }

    public void setModelId(Long modelId) {
        this.modelId = modelId;
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

    public BigDecimal getBudgetConsommeAvant() {
        return budgetConsommeAvant;
    }

    public void setBudgetConsommeAvant(BigDecimal budgetConsommeAvant) {
        this.budgetConsommeAvant = budgetConsommeAvant;
    }

    public BigDecimal getBudgetConsommeApres() {
        return budgetConsommeApres;
    }

    public void setBudgetConsommeApres(BigDecimal budgetConsommeApres) {
        this.budgetConsommeApres = budgetConsommeApres;
    }

    public LocalDateTime getDateCreation() {
        return dateCreation;
    }

    public void setDateCreation(LocalDateTime dateCreation) {
        this.dateCreation = dateCreation;
    }
}

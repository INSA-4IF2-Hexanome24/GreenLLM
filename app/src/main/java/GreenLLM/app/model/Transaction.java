package GreenLLM.app.model;

import java.math.BigDecimal;
import java.time.LocalDateTime;

import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.ManyToOne;
import jakarta.persistence.Table;

@Entity
@Table(name = "transactions")
public class Transaction {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne
    private Utilisateur utilisateur;

    @ManyToOne
    private ModelLLM modelLLM;

    @ManyToOne
    private Requete requete;

    @ManyToOne
    private Reponse reponse;

    private BigDecimal coutAjoute = BigDecimal.ZERO;
    private BigDecimal budgetConsommeAvant = BigDecimal.ZERO;
    private BigDecimal budgetConsommeApres = BigDecimal.ZERO;
    private LocalDateTime dateCreation = LocalDateTime.now();

    public Transaction() {
    }

    public Transaction(Utilisateur utilisateur, ModelLLM modelLLM, Requete requete, Reponse reponse,
                       BigDecimal coutAjoute, BigDecimal budgetConsommeAvant, BigDecimal budgetConsommeApres) {
        this.utilisateur = utilisateur;
        this.modelLLM = modelLLM;
        this.requete = requete;
        this.reponse = reponse;
        this.coutAjoute = coutAjoute;
        this.budgetConsommeAvant = budgetConsommeAvant;
        this.budgetConsommeApres = budgetConsommeApres;
        this.dateCreation = LocalDateTime.now();
    }

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public Utilisateur getUtilisateur() {
        return utilisateur;
    }

    public void setUtilisateur(Utilisateur utilisateur) {
        this.utilisateur = utilisateur;
    }

    public ModelLLM getModelLLM() {
        return modelLLM;
    }

    public void setModelLLM(ModelLLM modelLLM) {
        this.modelLLM = modelLLM;
    }

    public Requete getRequete() {
        return requete;
    }

    public void setRequete(Requete requete) {
        this.requete = requete;
    }

    public Reponse getReponse() {
        return reponse;
    }

    public void setReponse(Reponse reponse) {
        this.reponse = reponse;
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

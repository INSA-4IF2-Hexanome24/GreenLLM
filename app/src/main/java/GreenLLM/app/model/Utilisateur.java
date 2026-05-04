package GreenLLM.app.model;

import java.math.BigDecimal;

import jakarta.persistence.Embedded;
import jakarta.persistence.Entity;
import jakarta.persistence.EnumType;
import jakarta.persistence.Enumerated;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.ManyToOne;
import jakarta.persistence.Table;

@Entity
@Table(name = "utilisateur")
public class Utilisateur {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String email;
    private String prenom;
    private String nom;
    private String motDePasse;
    private BigDecimal budget = BigDecimal.ZERO;
    private BigDecimal budgetConsomme = BigDecimal.ZERO;

    @Enumerated(EnumType.STRING)
    private StatutUtilisateur statut;

    @ManyToOne
    private Groupe topGroupe;

    @Embedded
    private Adresse adresse;

    public Utilisateur() {
    }

    public Utilisateur(String email, String prenom, String nom, String motDePasse,
                       StatutUtilisateur statut, Groupe topGroupe, Adresse adresse) {
        this.email = email;
        this.prenom = prenom;
        this.nom = nom;
        this.motDePasse = motDePasse;
        this.statut = statut;
        this.topGroupe = topGroupe;
        this.adresse = adresse;
    }

    public double Calcul_Impact_CO2(Groupe groupe) {

        return 0.0;
    }

    public void Lancer_Requete(Requete requete) {
        
    }

    public void Enregistrer_Requete(Requete requete) {
    }

    public String Get_Organigramme_Entreprise(Utilisateur utilisateur) {
        return "";
    }

    public void Set_API_Keys() {
    }

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public String getEmail() {
        return email;
    }

    public void setEmail(String email) {
        this.email = email;
    }

    public String getPrenom() {
        return prenom;
    }

    public void setPrenom(String prenom) {
        this.prenom = prenom;
    }

    public String getNom() {
        return nom;
    }

    public void setNom(String nom) {
        this.nom = nom;
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

    public BigDecimal getBudgetConsomme() {
        return budgetConsomme;
    }

    public void setBudgetConsomme(BigDecimal budgetConsomme) {
        this.budgetConsomme = budgetConsomme;
    }

    public StatutUtilisateur getStatut() {
        return statut;
    }

    public void setStatut(StatutUtilisateur statut) {
        this.statut = statut;
    }

    public Groupe getTopGroupe() {
        return topGroupe;
    }

    public void setTopGroupe(Groupe topGroupe) {
        this.topGroupe = topGroupe;
    }

    public Adresse getAdresse() {
        return adresse;
    }

    public void setAdresse(Adresse adresse) {
        this.adresse = adresse;
    }
}

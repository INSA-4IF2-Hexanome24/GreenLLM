package GreenLLM.app.model;

import java.math.BigDecimal;
import java.util.List;

import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.ManyToOne;
import jakarta.persistence.OneToMany;

@Entity
public class Groupe {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String description;

    @ManyToOne
    private Groupe parent;

    @OneToMany
    private List<Groupe> sousGroupes;

    @OneToMany
    private List<Utilisateur> utilisateurs;

    private int niveauGroupe;
    private String departement;
    private BigDecimal budget = BigDecimal.ZERO;
    private BigDecimal budgetConsomme = BigDecimal.ZERO;

    @ManyToOne
    private Utilisateur admin;

    public Groupe() {
    }

    public Groupe(String description, String departement, Utilisateur admin) {
        this.description = description;
        this.departement = departement;
        this.admin = admin;
    }

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public String getDescription() {
        return description;
    }

    public void setDescription(String description) {
        this.description = description;
    }

    public Groupe getParent() {
        return parent;
    }

    public void setParent(Groupe parent) {
        this.parent = parent;
        this.niveauGroupe = parent.getNiveauGroupe();
    }

    public List<Groupe> getSousGroupes() {
        return sousGroupes;
    }

    public void setSousGroupes(List<Groupe> sousGroupes) {
        this.sousGroupes = sousGroupes;
    }

    public List<Utilisateur> getUtilisateurs() {
        return utilisateurs;
    }

    public void setUtilisateurs(List<Utilisateur> utilisateurs) {
        this.utilisateurs = utilisateurs;
    }

    public int getNiveauGroupe() {
        return niveauGroupe;
    }

    public void setNiveauGroupe(int niveauGroupe) {
        this.niveauGroupe = niveauGroupe;
    }

    public String getDepartement() {
        return departement;
    }

    public void setDepartement(String departement) {
        this.departement = departement;
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

    public Utilisateur getAdmin() {
        return admin;
    }

    public void setAdmin(Utilisateur admin) {
        this.admin = admin;
    }
}

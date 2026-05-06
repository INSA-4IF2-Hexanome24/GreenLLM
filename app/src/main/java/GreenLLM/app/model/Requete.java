package GreenLLM.app.model;

import java.math.BigDecimal;

import com.fasterxml.jackson.annotation.JsonAlias;

import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.ManyToOne;
import jakarta.persistence.Table;

@Entity
@Table(name = "requete")
public class Requete {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String description;
    @JsonAlias({"nbre_de_token", "nbre_tokens", "nombre_tokens", "input_tokens"})
    private int nombreTokens;
    private BigDecimal coutTotal = BigDecimal.ZERO;

    @ManyToOne
    private Utilisateur user;

    public Requete() {
    }

    public Requete(String description, Utilisateur user) {
        this.description = description;
        this.user = user;
    }

    public Requete(String description, Utilisateur user, int nombreTokens) {
        this.description = description;
        this.user = user;
        this.nombreTokens = nombreTokens;
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

    public int getNombreTokens() {
        return nombreTokens;
    }

    public void setNombreTokens(int nombreTokens) {
        this.nombreTokens = nombreTokens;
    }

    public BigDecimal getCoutTotal() {
        return coutTotal;
    }

    public void setCoutTotal(BigDecimal coutTotal) {
        this.coutTotal = coutTotal;
    }

    public Utilisateur getUser() {
        return user;
    }

    public void setUser(Utilisateur user) {
        this.user = user;
    }
}

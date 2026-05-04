package GreenLLM.app.model;

import java.math.BigDecimal;

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
    private int nombreTokens;
    private BigDecimal coutTotal = BigDecimal.ZERO;

    @ManyToOne
    private Utilisateur user;

    @ManyToOne
    private ModelLLM modelLLM;

    public Requete() {
    }

    public Requete(String description, Utilisateur user) {
        this.description = description;
        this.user = user;
    }

    public Requete(String description, Utilisateur user, ModelLLM modelLLM, int nombreTokens) {
        this.description = description;
        this.user = user;
        this.modelLLM = modelLLM;
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

    public ModelLLM getModelLLM() {
        return modelLLM;
    }

    public void setModelLLM(ModelLLM modelLLM) {
        this.modelLLM = modelLLM;
    }
}

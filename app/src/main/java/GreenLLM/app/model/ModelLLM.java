package GreenLLM.app.model;

import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;

@Entity
public class ModelLLM {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String nom;
    private double co2ParToken;

    public ModelLLM() {
    }

    public ModelLLM(String nom, double co2ParToken) {
        this.nom = nom;
        this.co2ParToken = co2ParToken;
    }

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public String getNom() {
        return nom;
    }

    public void setNom(String nom) {
        this.nom = nom;
    }

    public double getCo2ParToken() {
        return co2ParToken;
    }

    public void setCo2ParToken(double co2ParToken) {
        this.co2ParToken = co2ParToken;
    }
}

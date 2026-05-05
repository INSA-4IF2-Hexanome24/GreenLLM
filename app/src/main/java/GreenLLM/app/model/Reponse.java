package GreenLLM.app.model;

import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import jakarta.persistence.ManyToOne;


@Entity
@Table(name = "reponse")
public class Reponse {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne
    private ModelLLM modelUtilise; 

    private String description;
    private int nombreTokens;

    public Reponse() {
    }

    public Reponse(String description) {
        this.description = description;
    }

    public Reponse(String description, int nombreTokens) {
        this.description = description;
        this.nombreTokens = nombreTokens;
    }

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public void setModelUtlise(ModelLLM model) {
        this.modelUtilise = model;
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

    public ModelLLM getModelUtilise(){
        return this.modelUtilise;
    }

    
}

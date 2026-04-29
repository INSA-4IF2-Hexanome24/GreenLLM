package GreenLLM.app.model;

import jakarta.persistence.Embeddable;

@Embeddable
public class Adresse {


    private String ville;
    private String codePostal;
    private String pays;

    public Adresse() {
    }

    public Adresse( String ville, String codePostal, String pays) {
        
        this.ville = ville;
        this.codePostal = codePostal;
        this.pays = pays;
    }

  

    public String getVille() {
        return ville;
    }

    public void setVille(String ville) {
        this.ville = ville;
    }

    public String getCodePostal() {
        return codePostal;
    }

    public void setCodePostal(String codePostal) {
        this.codePostal = codePostal;
    }

    public String getPays() {
        return pays;
    }

    public void setPays(String pays) {
        this.pays = pays;
    }
}

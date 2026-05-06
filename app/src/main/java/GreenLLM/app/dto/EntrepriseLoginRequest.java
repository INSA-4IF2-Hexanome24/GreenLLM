package GreenLLM.app.dto;

public class EntrepriseLoginRequest {

    private String siret;
    private String motDePasse;

    public EntrepriseLoginRequest() {
    }

    public String getSiret() {
        return siret;
    }

    public void setSiret(String siret) {
        this.siret = siret;
    }

    public String getMotDePasse() {
        return motDePasse;
    }

    public void setMotDePasse(String motDePasse) {
        this.motDePasse = motDePasse;
    }
}

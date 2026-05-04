package GreenLLM.app.dto;

import GreenLLM.app.model.Adresse;
import GreenLLM.app.model.StatutUtilisateur;

public class UserRegisterRequest {

    private String email;
    private String prenom;
    private String nom;
    private String motDePasse;
    private StatutUtilisateur statut;
    private Adresse adresse;

    public UserRegisterRequest() {
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

    public StatutUtilisateur getStatut() {
        return statut;
    }

    public void setStatut(StatutUtilisateur statut) {
        this.statut = statut;
    }

    public Adresse getAdresse() {
        return adresse;
    }

    public void setAdresse(Adresse adresse) {
        this.adresse = adresse;
    }
}

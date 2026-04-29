package GreenLLM.app.model;

public class Groupe{

    private String description;
    //private Entreprise entreprise;
    private Groupe parent;
    private List<Groupe>  sousGroupes;
    private List<Utilisateur> utilisateurs;
    private int niveauGroupe;
    private String departement;
    private Utilisateur admin;


    //Instancier un groupe. Créer sans utilisateurs au début et sans group parent
    public Groupe(String description, String departement, Utilisateur admin){
        this.description = description;
        this.departement = departement;
        this.admin = admin;
    }

    public String getDescription() {
        return description;
    }

    public Groupe getParent() {
        return parent;
    }

    public List<Groupe> getSousGroupes() {
        return sousGroupes;
    }

    public List<Utilisateur> getUtilisateurs() {
        return utilisateurs;
    }

    public int getNiveauGroupe() {
        return niveauGroupe;
    }

    public String getDepartement() {
        return departement;
    }

    public Admin getAdmin() {
        return admin;
    }

    // ========================
    //         SETTERS
    // ========================

    public void setDescription(String description) {
        this.description = description;
    }

    public void setParent(Groupe parent) {
        this.parent = parent;
        this.NiveauGroupe = parent.getNiveauGroupe();
    }

    public void setSousGroupes(List<Groupe> sousGroupes) {
        this.sousGroupes = sousGroupes;
    }

    public void setUtilisateurs(List<Utilisateur> utilisateurs) {
        this.utilisateurs = utilisateurs;
    }

    /*
    public void setNiveauGroupe(int niveauGroupe) {
        this.niveauGroupe = niveauGroupe;
    }
    */
    
    public void setDepartement(String departement) {
        this.departement = departement;
    }

    public void setAdmin(Utilisateur admin) {
        this.admin = admin;
    }
}
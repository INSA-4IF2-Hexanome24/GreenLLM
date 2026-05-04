package GreenLLM.app.model;

import java.util.HashMap;
import java.util.HashSet;
import java.util.Map;
import java.util.Set;

import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.JoinTable;
import jakarta.persistence.MapKeyJoinColumn;
import jakarta.persistence.OneToMany;
import jakarta.persistence.Table;

@Entity
@Table(name = "entreprise")
public class Entreprise {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String siret;
    private String domaine;
    private String motDePasse;

    @OneToMany
    private Set<Groupe> groupes = new HashSet<>();

    @OneToMany
    @JoinTable(
            name = "entreprise_requetes",
            joinColumns = @JoinColumn(name = "entreprise_id"),
            inverseJoinColumns = @JoinColumn(name = "reponse_id"))
    @MapKeyJoinColumn(name = "requete_id")
    private Map<Requete, Reponse> requetes = new HashMap<>();

    public Entreprise() {
    }

    public Entreprise(String siret, String domaine, String motDePasse) {
        this.siret = siret;
        this.domaine = domaine;
        this.motDePasse = motDePasse;
    }

    public double Calcul_Impact_CO2(Entreprise entreprise) {
        return 0.0;
    }

    public int Comparaison_avec_secteur(Entreprise entreprise) {
        return 0;
    }

    public void Set_API_Keys() {
    }

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public String getSiret() {
        return siret;
    }

    public void setSiret(String siret) {
        this.siret = siret;
    }

    public String getDomaine() {
        return domaine;
    }

    public void setDomaine(String domaine) {
        this.domaine = domaine;
    }

    public String getMotDePasse() {
        return motDePasse;
    }

    public void setMotDePasse(String motDePasse) {
        this.motDePasse = motDePasse;
    }

    public Set<Groupe> getGroupes() {
        return groupes;
    }

    public void setGroupes(Set<Groupe> groupes) {
        this.groupes = groupes;
    }

    public Map<Requete, Reponse> getRequetes() {
        return requetes;
    }

    public void setRequetes(Map<Requete, Reponse> requetes) {
        this.requetes = requetes;
    }
}

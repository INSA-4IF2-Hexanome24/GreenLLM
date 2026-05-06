package GreenLLM.app.service;

import java.math.BigDecimal;

import org.springframework.stereotype.Service;

import GreenLLM.app.dto.AuthResponse;
import GreenLLM.app.dto.UserLoginRequest;
import GreenLLM.app.dto.UserRegisterRequest;
import GreenLLM.app.model.StatutUtilisateur;
import GreenLLM.app.model.Utilisateur;
import GreenLLM.app.repository.UtilisateurRepository;

@Service
public class UserAuthService {

    private final UtilisateurRepository utilisateurRepository;

    public UserAuthService(UtilisateurRepository utilisateurRepository) {
        this.utilisateurRepository = utilisateurRepository;
    }

    public AuthResponse register(UserRegisterRequest request) {
        if (utilisateurRepository.existsByEmail(request.getEmail())) {
            throw new IllegalArgumentException("Email deja utilise"); //
        }

        StatutUtilisateur statut = request.getStatut() != null
                ? request.getStatut()
                : StatutUtilisateur.EMPLOYE; //

        Utilisateur utilisateur = new Utilisateur(
                request.getEmail(), //
                request.getPrenom(), //[cite: 4]
                request.getNom(), //[cite: 4]
                request.getMotDePasse(), //[cite: 4]
                statut, //[cite: 4]
                null, //[cite: 4]
                request.getAdresse()); //[cite: 4]
        
        utilisateur.setBudget(valeur(request.getBudget())); //[cite: 4]
        utilisateur.setBudgetConsomme(BigDecimal.ZERO); //[cite: 4]

        Utilisateur savedUtilisateur = utilisateurRepository.save(utilisateur); //[cite: 4]
        
        // Retornamos el nuevo formato
        return mapToAuthResponse(savedUtilisateur);
    }

    public AuthResponse login(UserLoginRequest request) {
        Utilisateur utilisateur = utilisateurRepository.findByEmail(request.getEmail())
                .orElseThrow(() -> new IllegalArgumentException("Identifiants invalides")); //[cite: 4]

        if (!utilisateur.getMotDePasse().equals(request.getMotDePasse())) { //[cite: 4]
            throw new IllegalArgumentException("Identifiants invalides"); //[cite: 4]
        }

        // Retornamos el nuevo formato
        return mapToAuthResponse(utilisateur);
    }

    private BigDecimal valeur(BigDecimal montant) {
        return montant != null ? montant : BigDecimal.ZERO; //[cite: 4]
    }

    // --- NUEVO MÉTODO PRIVADO PARA MAPEAR EL USUARIO A LA RESPUESTA ---
    private AuthResponse mapToAuthResponse(Utilisateur u) {
        // 1. Unimos nombre y apellido (basado en getPrenom y getNom)
        String fullName = u.getPrenom() + " " + u.getNom(); 
        
        // 2. Mapeamos el rol de tu enum StatutUtilisateur al string que espera TS
        // Asumiendo que StatutUtilisateur.EMPLOYE equivale a 'employee'
        String roleStr = (u.getStatut() == StatutUtilisateur.EMPLOYE) ? "employee" : "admin";
        
        // 3. Manejo de Ciudad y País. 
        // Como en tu entidad tienes 'getAdresse()', deberás extraer la ciudad y el país de ahí.
        // Si adresse es un String simple, podrías tener que separarlo. Aquí uso valores por defecto.
        String city = "Ciudad desconocida"; // Cambia esto según cómo funcione getAdresse()
        String country = "País desconocido"; // Cambia esto según cómo funcione getAdresse()
        
        // 4. Username (Si no tienes un campo username específico, se suele usar el email)
        String username = u.getEmail();

        return new AuthResponse(
            fullName,
            username,
            u.getEmail(),
            roleStr,
            city,
            country,
            null // Avatar (en tu constructor de Utilisateur vi que pasas null en el 6to parámetro)
        );
    }
}
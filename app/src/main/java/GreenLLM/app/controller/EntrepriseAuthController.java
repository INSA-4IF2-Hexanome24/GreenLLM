package GreenLLM.app.controller;

import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import GreenLLM.app.dto.AuthResponse;
import GreenLLM.app.dto.EntrepriseLoginRequest;
import GreenLLM.app.dto.EntrepriseRegisterRequest;
import GreenLLM.app.service.EntrepriseAuthService;

@RestController
@RequestMapping("/api/auth/entreprises")
public class EntrepriseAuthController {

    private final EntrepriseAuthService entrepriseAuthService;

    public EntrepriseAuthController(EntrepriseAuthService entrepriseAuthService) {
        this.entrepriseAuthService = entrepriseAuthService;
    }

    @PostMapping("/register")
    public ResponseEntity<AuthResponse> register(@RequestBody EntrepriseRegisterRequest request) {
        AuthResponse response = entrepriseAuthService.register(request);
        return ResponseEntity.status(HttpStatus.CREATED).body(response);
    }

    @PostMapping("/login")
    public ResponseEntity<AuthResponse> login(@RequestBody EntrepriseLoginRequest request) {
        return ResponseEntity.ok(entrepriseAuthService.login(request));
    }
}

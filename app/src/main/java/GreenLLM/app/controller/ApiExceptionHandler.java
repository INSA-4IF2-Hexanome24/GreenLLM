package GreenLLM.app.controller;

import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;

@RestControllerAdvice
public class ApiExceptionHandler {

    @ExceptionHandler(IllegalArgumentException.class)
    public ResponseEntity<String> handleIllegalArgumentException(IllegalArgumentException exception) {
        String message = exception.getMessage();

        if (message != null && message.contains("deja utilise")) {
            return ResponseEntity.status(HttpStatus.CONFLICT).body(message);
        }

        if (message != null && message.contains("introuvable")) {
            return ResponseEntity.status(HttpStatus.NOT_FOUND).body(message);
        }

        if (message != null && message.contains("n'appartient pas")) {
            return ResponseEntity.status(HttpStatus.FORBIDDEN).body(message);
        }

        if (message != null && message.contains("Identifiants invalides")) {
            return ResponseEntity.status(HttpStatus.UNAUTHORIZED).body(message);
        }

        return ResponseEntity.status(HttpStatus.BAD_REQUEST).body(message);
    }
}

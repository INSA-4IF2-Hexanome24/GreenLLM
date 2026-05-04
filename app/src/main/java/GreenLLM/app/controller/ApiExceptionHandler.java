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

        return ResponseEntity.status(HttpStatus.UNAUTHORIZED).body(message);
    }
}

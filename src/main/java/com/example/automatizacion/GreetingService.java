package com.example.automatizacion;

import java.util.Objects;

public final class GreetingService {
    private final UserRepository userRepository;

    public GreetingService(UserRepository userRepository) {
        this.userRepository = Objects.requireNonNull(userRepository, "userRepository es obligatorio");
    }

    public String greetByUserId(String userId) {
        if (userId == null || userId.isBlank()) {
            return "Usuario no válido";
        }

        String displayName = userRepository.findDisplayName(userId);
        if (displayName == null || displayName.isBlank()) {
            return "Usuario no encontrado";
        }
        return "¡Hola, " + displayName + "!";
    }
}

package com.example.automatizacion;

import org.junit.jupiter.api.Test;

import java.util.Map;

import static org.junit.jupiter.api.Assertions.assertEquals;

class GreetingServiceIT {
    @Test
    void debeIntegrarServicioYRepositorio() {
        UserRepository repository = new InMemoryUserRepository(Map.of("u-1", "Carlos"));
        GreetingService service = new GreetingService(repository);

        assertEquals("¡Hola, Carlos!", service.greetByUserId("u-1"));
        assertEquals("Usuario no encontrado", service.greetByUserId("u-404"));
    }
}

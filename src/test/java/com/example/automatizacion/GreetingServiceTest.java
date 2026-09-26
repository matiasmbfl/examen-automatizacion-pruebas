package com.example.automatizacion;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;

class GreetingServiceTest {
    @Test
    void debeSaludarAlUsuarioEncontrado() {
        UserRepository stub = userId -> "Ana";
        GreetingService service = new GreetingService(stub);

        assertEquals("¡Hola, Ana!", service.greetByUserId("u-1"));
    }

    @Test
    void debeRechazarIdentificadorVacío() {
        GreetingService service = new GreetingService(userId -> "Ana");

        assertEquals("Usuario no válido", service.greetByUserId(" "));
    }
}

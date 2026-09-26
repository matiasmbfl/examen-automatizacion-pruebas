package com.example.automatizacion;

import org.junit.jupiter.api.Test;

import java.util.Map;

import static org.junit.jupiter.api.Assertions.assertTrue;

class GreetingAcceptanceTest {
    @Test
    void usuarioRegistradoRecibeSaludoPersonalizado() {
        GreetingService service = new GreetingService(
                new InMemoryUserRepository(Map.of("cliente-001", "Cliente Demo"))
        );

        String response = service.greetByUserId("cliente-001");

        assertTrue(response.contains("Cliente Demo"),
                "El flujo de aceptación debe mostrar el nombre del usuario");
    }
}

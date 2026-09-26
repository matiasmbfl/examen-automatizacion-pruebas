package com.example.automatizacion;

import java.util.Map;

public final class InMemoryUserRepository implements UserRepository {
    private final Map<String, String> users;

    public InMemoryUserRepository(Map<String, String> users) {
        this.users = Map.copyOf(users);
    }

    @Override
    public String findDisplayName(String userId) {
        return users.get(userId);
    }
}

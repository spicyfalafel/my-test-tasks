package com.svyat.test.testtask.service;

import com.svyat.test.testtask.models.User;

import java.util.List;

public interface UserService {
    User getById(Long id);

    void save(User virus);

    void saveAll(List<User> viruses);

    void delete(Long id);

    List<User> getAll();
}

package com.svyat.test.testtask.service;

import com.svyat.test.testtask.models.User;
import com.svyat.test.testtask.repository.OrderRepository;
import com.svyat.test.testtask.repository.UserRepository;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

@Slf4j
@Service
public class UserServiceImplementation implements UserService {

    @Autowired
    UserRepository userRepository;

    @Autowired
    OrderRepository orderRepository;

    @Override
    public User getById(Long id) {
        log.info("getById():" + id);
        return userRepository.findById(id).get();
    }

    @Override
    public void save(User user) {
        user.getOrders().forEach(orderRepository::save);
        userRepository.save(user);
        log.info("save():" + user);
    }

    @Override
    public void saveAll(List<User> users) {
        userRepository.saveAll(users);
        log.info("saveAll(): " + users.size());
    }

    @Override
    public void delete(Long id) {
        userRepository.deleteById(id);
        log.info("delete():" + id);
    }

    @Override
    public List<User> getAll() {
        log.info("getAll()");
        return userRepository.findAll();
    }
}
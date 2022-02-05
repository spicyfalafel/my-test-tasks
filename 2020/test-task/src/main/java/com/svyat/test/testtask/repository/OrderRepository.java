package com.svyat.test.testtask.repository;

import com.svyat.test.testtask.models.Order;
import org.springframework.data.jpa.repository.JpaRepository;

public interface OrderRepository extends JpaRepository<Order, Long> {
}

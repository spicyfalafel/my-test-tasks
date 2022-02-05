package com.svyat.test.testtask.models;

import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

import javax.persistence.*;

@Getter @Setter @NoArgsConstructor
@Table(name= "orders")
@Entity
public class Order {
    @Id @GeneratedValue(strategy= GenerationType.IDENTITY)
    private Long id;
    @Column(name = "service_name")
    private String serviceName;
    @Column(name = "target_url")
    private String targetUrl;
    private double price;

    @Override
    public String toString() {
        return "Order{" +
                "id='" + id + '\'' +
                ", serviceName='" + serviceName + '\'' +
                ", targetUrl='" + targetUrl + '\'' +
                ", price=" + price +
                '}';
    }
}

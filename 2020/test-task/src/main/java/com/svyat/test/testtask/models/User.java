package com.svyat.test.testtask.models;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

import javax.persistence.*;
import java.util.List;

@Getter
@Setter
@NoArgsConstructor
@Table(name= "users")
@Entity
public class User {
    @Id @GeneratedValue(strategy=GenerationType.IDENTITY)
    private Long id;
    @Column(name = "first_name")
    private String firstName;
    @Column(name = "last_name")
    private String lastName;

    // had a problem https://stackoverflow.com/questions/52656517/no-serializer-found-for-class-org-hibernate-proxy-pojo-bytebuddy-bytebuddyinterc
    @OneToMany(fetch = FetchType.EAGER, cascade = CascadeType.ALL)
    private List<Order> orders;
}

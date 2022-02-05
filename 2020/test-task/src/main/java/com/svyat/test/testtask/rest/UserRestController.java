package com.svyat.test.testtask.rest;

import com.svyat.test.testtask.models.User;
import com.svyat.test.testtask.service.UserService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.util.UriComponentsBuilder;

import javax.validation.Valid;
import java.util.List;

@RestController
@RequestMapping("/api/v1/user/")
public class UserRestController {

    @Autowired
    private UserService userService;

    @GetMapping("{id}")
    public ResponseEntity<User> getUser(@PathVariable("id") Long id){
        if( id == null){
            return new ResponseEntity<>(HttpStatus.BAD_REQUEST);
        }
        User user = this.userService.getById(id);
        if(user == null) {
            return new ResponseEntity<>(HttpStatus.NOT_FOUND);
        }
        return new ResponseEntity<>(user, HttpStatus.OK);
    }

    @PostMapping
    public ResponseEntity<User> saveUser(@RequestBody @Valid User user){
        HttpHeaders headers = new HttpHeaders();
        if(user == null){
            return new ResponseEntity<>(HttpStatus.BAD_REQUEST);
        }
        this.userService.save(user);
        return new ResponseEntity<>(user, headers, HttpStatus.CREATED);
    }

    @PutMapping("{id}")
    public ResponseEntity<User> updateUser(@RequestBody @Valid User user, UriComponentsBuilder builder){
        HttpHeaders headers = new HttpHeaders();
        if(user==null){
            return new ResponseEntity<>(HttpStatus.BAD_REQUEST);
        }
        this.userService.save(user);
        return new ResponseEntity<>(user, headers, HttpStatus.OK);
    }

    @DeleteMapping("{id}")
    public ResponseEntity<User> deleteUser(@PathVariable("id") Long id){
        var user = this.userService.getById(id);
        if(user == null){
            return new ResponseEntity<>(HttpStatus.NOT_FOUND);
        }else{

            this.userService.delete(id);
            return new ResponseEntity<>(user, HttpStatus.FOUND);
        }
    }

    @GetMapping()
    public ResponseEntity<List<User>> getAllUsers(){
        List<User> all = this.userService.getAll();
        if(all.isEmpty()){
            return new ResponseEntity<>(HttpStatus.NOT_FOUND);
        }
        return new ResponseEntity<>(all, HttpStatus.OK);
    }
}
package com.gavinshark.userservice;

import org.springframework.stereotype.Service;

import javax.annotation.PostConstruct;
import java.util.Arrays;
import java.util.List;

@Service("userService")
public class UserServiceImpl implements UserService{
    public List<String> getUserAddress(String userId) {
        if (0 == userId.compareTo("1")){
            return Arrays.asList("City1", "Province1");
        } else {
            System.out.println("userId is: " + userId);
            return Arrays.asList("DefaultCity", "DefaultProvince");
        }

    }


    @PostConstruct
    public void init(){
        System.out.println("UserServiceImpl - init()");
    }
}

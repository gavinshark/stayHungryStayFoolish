package com.example.springtest.springtest;

import org.springframework.stereotype.Component;

import javax.annotation.PostConstruct;

@Component
public class StartUpService {
    public StartUpService(){
        System.out.println("StartUpService - construct method!");
    }

    @PostConstruct
    public void init(){
        System.out.println("StartUpService - init()");
    }
}

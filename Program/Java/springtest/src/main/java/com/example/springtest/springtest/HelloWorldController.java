package com.example.springtest.springtest.web.controller;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/MyTest")
public class HelloWorldController {
    @Value("${xyx.name}")
    private String myName;
    @RequestMapping("/hello")
    public String hello(){
        System.out.println("hello!");
        return myName + ":Hello World!";
    }
}
//http://localhost:8080/MyTest/hello

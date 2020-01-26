package com.gavinshark;

import com.gavinshark.orderservice.OrderService;
import com.gavinshark.orderservice.OrderServiceImpl;

import javax.annotation.Resource;

public class UserServiceConsumer {
    public OrderService orderService = new OrderServiceImpl();
    public static void main(String[] args) throws Exception {
        UserServiceConsumer usc = new UserServiceConsumer();
        usc.orderService.initUserList();
        System.in.read();
    }
}
package com.gavinshark.orderservice;

import java.util.List;
import com.gavinshark.userservice.UserService;
import org.springframework.context.support.ClassPathXmlApplicationContext;

public class OrderServiceImpl implements OrderService {
    UserService userService;
    @Override
    public void initUserList() {
        ClassPathXmlApplicationContext context = new ClassPathXmlApplicationContext(new String[] {"consumer.xml"});
        context.start();
        UserService userService = (UserService)context.getBean("UserService"); // 获取远程服务代理
        List<String> userList = userService.getUserAddress("1");
        System.out.println("userList is " + userList.toString());
        return;
    }
}

package com.gavinshark.userservice;
import org.springframework.stereotype.Component;

import java.util.*;

public interface UserService {
    public List<String> getUserAddress (String userId);
}
package com.gavinshark.mybatisDemo;

public class Salary {
    public Integer getId() {
        return id;
    }

    public void setId(Integer id) {
        this.id = id;
    }

    public Integer getMoney() {
        return money;
    }

    public void setMoney(Integer money) {
        this.money = money;
    }

    private Integer id;
    private Integer money;

    @Override
    public String toString() {
        return "Salary{" +
                "id=" + id +
                ", money=" + money +
                '}';
    }
}

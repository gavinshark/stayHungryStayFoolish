## 1. how to build the env
### 1.1 install zookeeper
1. download zookeeper
2. cp conf/zoo_sample.cfg zoo.cfg
3. edit zoo.cfg : dataDir to your special dir
4. run zkServer.sh/cmd

### 1.2 install dubbo admin
1. download dubbo-admin (master branch)
2. confirm the configuration in dubbo-admin-master\dubbo-admin\src\main\resources\application.properties
3. mvn clean package
4. run zookeeper
5. go to dubbo-admin-master\dubbo-admin\target, cmd: java -jar dubbo-admin-0.0.1-SNAPSHOT.jar
6. http://127.0.0.1:7001 username/password=root/root


## 2.Provider & Consumer
refer to http://dubbo.apache.org/zh-cn/docs/user/quick-start.html
### 2.1 Provider - User Service
1. pom.xml for dependencies
2. provider.xml for dubbo 
3. application.properties for spring service port

### 2.2 Consumer - Order Service
1. pom.xml for dependencies
2. consumer.xml for dubbo
3. ClassPathXmlApplicationContext to fetch remote service bean
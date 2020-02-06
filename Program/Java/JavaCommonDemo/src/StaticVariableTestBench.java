import java.lang.*;
import java.util.Date;
import java.util.Hashtable;
import java.util.Map;

public class StaticVariableTestBench {
    public static void main(String[] args){
        StaticVariableTest test1 = new StaticVariableTestSon1();
        StaticVariableTest test2 = new StaticVariableTestSon2();

        test1.setMap("key1", new Date(0));
        Date date2 = test2.getMap("key1");
        System.out.println("date2:" + date2.toString());

        test2.setMap("key1", new Date());
        Date date1 = test1.getMap("key1");
        System.out.println("date1:" + date1.toString());

    }
}

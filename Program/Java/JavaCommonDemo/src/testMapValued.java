import java.lang.*;
import java.util.*;

public class testMapValued {
    public class InnerClass{
        private int a;
    }
    public static void main(String [] args){
        Map<Integer, InnerClass> map = new HashMap<Integer, InnerClass>();
        map.put(1, null);
        map.put(2, null);
        Collection<InnerClass> innerCollections = map.values();
        if(null == innerCollections) {
            System.out.println(" innerCollections is null");
        } else {
            System.out.println(" innerCollections is not null");
        }
    }
}

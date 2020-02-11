import java.lang.*;
import java.util.Arrays;
import java.util.HashSet;
import java.util.Map;
import java.util.Set;
import java.util.stream.Collectors;

public class set2MapTest {
    public static void main(String [] args){
        Set<String> mySet = new HashSet<>(Arrays.asList("0", "1"));
        Map<String, String> myMap = mySet.stream().collect(
                Collectors.toMap(x -> x, x -> {return null;})); //should fail as value cannot be null in collectors
        for(Map.Entry<String, String> entry: myMap.entrySet()){
            System.out.println("key:" + entry.getKey() + ", value:" + entry.getValue());
        }
    }
}

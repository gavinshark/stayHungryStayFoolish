import java.lang.*;
import java.util.Date;
import java.util.Hashtable;
import java.util.Map;

public abstract class StaticVariableTest {
    private static Map<String, Date> myMap = new Hashtable<>();
    protected abstract void display();

    public boolean setMap(String key, Date date){ myMap.put(key, date); return true;}
    public Date getMap(String key){return myMap.get(key);}
}

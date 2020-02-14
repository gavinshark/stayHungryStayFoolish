import java.lang.*;
import java.util.Date;
import java.util.Objects;


public class testStringCompare {
    public static void main(String [] args){
        String c = "x";
        Date date = new Date();
        Date theshold = new Date(12345);
        if(date.after(theshold)){
            c = date.toString();
            c = c.substring(0, 7);
        }
        System.out.println("c:"+c);
        System.out.println("Objects.equals:" + Objects.equals(c, "Fri Feb"));
        System.out.println("==:"+ (c == "Fri Feb"));
    }
}

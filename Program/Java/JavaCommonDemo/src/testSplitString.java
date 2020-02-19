import java.lang.*;

public class testSplitString {
    public static void main(String [] args) {
        String emptyString = "";
        String[] emptyStringArr = emptyString.split(";");
        System.out.println("empty String Arr size is " + emptyStringArr.length);
        for (String str : emptyStringArr) {
            System.out.println("str is:" + str);
        }
    }
}

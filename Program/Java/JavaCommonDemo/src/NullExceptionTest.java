import java.lang.*;

public class NullExceptionTest {
    private class MyClass{
       private int i;

        public int getI() {
            return i;
        }

        public void setI(int i) {
            this.i = i;
        }

        public String getStr() {
            return str;
        }

        public void setStr(String str) {
            this.str = str;
        }

        private String str;
    }
    public static void main(String [] args){
        MyClass myObject = null;
        try {
            myObject.setI(1);
            System.out.println("set down");
        } catch(Exception e){
            System.out.println("exception is :" + e.toString());
        }
        System.out.println("continue ...");
    }
}

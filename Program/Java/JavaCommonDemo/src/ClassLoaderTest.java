import java.lang.*;

public class ClassLoaderTest {
    public static void main(String[] args){
        //classloader
        if(false){
            Thread t = new Thread();
            t.start();
            Object myObject = new ClassLoaderTest();
            System.out.println(myObject.getClass().getClassLoader().getParent().getParent());
            System.out.println(myObject.getClass().getClassLoader().getParent());
            System.out.println(myObject.getClass().getClassLoader());
        }

        //memory
        if(false){
            long maxMemory  = Runtime.getRuntime().maxMemory();
            long totalMemory = Runtime.getRuntime().totalMemory();
            System.out.println("maxMemory=" + maxMemory/(double)1024/1024 + "MB");
            System.out.println("totalMemory=" + totalMemory/(double)1024/1024 + "MB");
        }

        //GC
        if(true){
            int i = 0;
            String str = "13231232131";
            while (true){
                String output = String. format ("the %dth string build", i++);
                System.out.println(output);
                str = str + str + "12312321313";
            }
        }
    }
}

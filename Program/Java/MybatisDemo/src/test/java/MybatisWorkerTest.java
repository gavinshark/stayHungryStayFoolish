import com.gavinshark.mybatisDemo.*;

import org.junit.*;

import java.io.IOException;

public class MybatisWorkerTest {
    @Test
    public void test() throws IOException {
        MybatisWorker.displaySalarybyId(1);
        MybatisWorker.displaySalarybyId(2);
    }
}
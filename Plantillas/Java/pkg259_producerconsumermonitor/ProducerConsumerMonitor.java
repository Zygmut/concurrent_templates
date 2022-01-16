package pkg259_producerconsumermonitor;

public class ProducerConsumerMonitor {

    static final int BUFFER_SIZE = 10;
    static final int PRODUCERS = 2;
    static final int CONSUMERS = 2;
    static final int TO_CONSUME = 1000;
    static final int TO_PRODUCE = 1000;
    
    public static void main(String[] args) {
        Thread[] threads = new Thread[PRODUCERS+CONSUMERS];
        int t = 0, i;
        PCMonitor monitor = new PCMonitor(BUFFER_SIZE);
        for (i = 0; i < CONSUMERS; i++) {
            threads[t] = new Thread(new Consumer(monitor, TO_CONSUME));
            threads[t].start();
            t++;
        }
        for (i = 0; i < PRODUCERS; i++) {
            threads[t] = new Thread(new Producer(monitor, TO_PRODUCE));
            threads[t].start();
            t++;
        }
        for (i = 0; i < PRODUCERS+CONSUMERS; i++) {
            try {
                threads[i].join();
            } catch (InterruptedException e) {}
        }

    }
    
}

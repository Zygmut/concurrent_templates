package pkg259_producerconsumermonitor;

class Consumer implements Runnable {

    PCMonitor monitor;
    int operations;

    public Consumer(PCMonitor mon, int ops) {
        monitor = mon;
        operations = ops;
    }

    @Override
    public void run() {
        long id = Thread.currentThread().getId();
        Integer data;
        System.out.println("Consumidor " + id);
        for (int i = 0; i < operations; i++ ) {
            data = monitor.take();
            System.out.println("        " + id + " consumeix " + data);
        }
        System.out.println("          Consumidor " + id + " ha acabat");
    }
    
}

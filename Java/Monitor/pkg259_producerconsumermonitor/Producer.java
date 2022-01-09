package pkg259_producerconsumermonitor;

class Producer implements Runnable {
    PCMonitor monitor;
    int operations;

    public Producer(PCMonitor mon, int ops) {
        monitor = mon;
        operations = ops;
    }

    @Override
    public void run() {
        long id = Thread.currentThread().getId();
        System.out.println("Productor " + id);
        for (int i = 0; i < operations; i++ ) {
            monitor.append(i);
            System.out.println(id + " produeix: " + i);
        }
        System.out.println("Productor " + id + " ha acabat");
    }
}

package pkg259_producerconsumermonitor;

import java.util.Deque;
import java.util.LinkedList;

class PCMonitor {

    int size;
    Deque<Integer> buffer = new LinkedList<>();

    public PCMonitor(int size) {
        this.size = size;
    }

    synchronized public int take() {
        Integer data;
        while (buffer.isEmpty()) {
            try {
                this.wait();
            } catch (InterruptedException e) {
            }
        }
        data = buffer.remove();
        notifyAll();
        return data;
    }

    synchronized public void append(Integer data) {
        while (buffer.size() == size) {
            try {
                this.wait();
            } catch (InterruptedException e) {
            }
        }
        buffer.add(data);
        this.notifyAll();
    }

}

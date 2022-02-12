
package pkg292_blanacaneuscondition;

import java.util.concurrent.locks.Condition;
import java.util.concurrent.locks.Lock;
import java.util.concurrent.locks.ReentrantLock;
import java.util.logging.Level;
import java.util.logging.Logger;

class MonitorCondition {

    private int aDormir, perMenjar, cadires;
    static final int NUMCADIRES = 4;
    private final Lock lock = new ReentrantLock();
    private final Condition seu, menja;

    public MonitorCondition() {
        this.aDormir = 0;
        this.perMenjar = 0;
        this.cadires = NUMCADIRES;
        this.seu = lock.newCondition();
        this.menja = lock.newCondition();
    }

    synchronized int getaDormir() {
        return aDormir;
    }

    public void donaMenjar() {
        lock.lock();
        try {
            perMenjar--;
            System.out.println("perMenjar =  " + perMenjar + " cadires = " + cadires);
            menja.signal();
        } finally {
            lock.unlock();
        }
    }

    public void incrementaaDormir() {
        lock.lock();
        try {
            aDormir++;
        } finally {
            lock.unlock();
        }
    }

    public void demanaCadira() {
        lock.lock();
        try {
            while (cadires == 0) {
                seu.await();
            }
            cadires--;
        } catch (InterruptedException ex) {
        } finally {
            lock.unlock();
        }
    }

    public void demanaMenjar() {
        lock.lock();
        try {
            perMenjar++;
            System.out.println("perMenjar =  " + perMenjar + " cadires = " + cadires);
            menja.await();
        } catch (InterruptedException ex) {
        } finally {
            lock.unlock();
        }
    }

    public void senVa() {
        lock.lock();
        try {
            cadires++;
            seu.signal();
        } finally {
            lock.unlock();
        }
    }

    synchronized int getPerMenjar() {
        return perMenjar;
    }

}

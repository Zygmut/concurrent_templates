/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package MaquinaExpendedora;

/**
 *
 * @author alber
 */
public class Monitor {

    private int   refrescs, consumidors;
    private final int MaxRefresc = 10;

    public Monitor( int consumidors) {
        this.refrescs = 0;
        this.consumidors = consumidors;
    }

    synchronized void consumirRefresc() throws InterruptedException {
        while (refrescs == 0) {
            wait();
        }
        refrescs--;
    }

    synchronized void replenarRefresc() {
        if (refrescs != MaxRefresc) {
            refrescs = MaxRefresc;
            notifyAll();
        }
    }
    synchronized void senVa(){
        consumidors--;
    }
    
    synchronized int getConsumidors(){
        return consumidors;
    }

    synchronized int getRefrescs(){
        return refrescs;
    }
    synchronized  int getMaxRefresc(){
        return MaxRefresc;
    }

}

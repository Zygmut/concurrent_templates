package h20;

import java.util.concurrent.Semaphore;

public class h20 {
    //Número de procesos
    static final int THREADS = 6;    

    //Semaforo para wake Oxigeno
    static private Semaphore oxygenAwake = new Semaphore(0);
    //Semaforo para notificar fin de Sintesis de agua
    static private Semaphore h20Finish = new Semaphore(0);
    
    public static void main(String[] args) throws InterruptedException {
        Thread [] procesos = new Thread[THREADS];
        for (int i = 0; i < procesos.length; i++) {
            if(i<procesos.length-2){
                procesos[i]= new Thread(new Hydrogen(oxygenAwake,h20Finish,i));
            }else{
                procesos[i]= new Thread(new Oxygen(oxygenAwake,h20Finish,i));
            }
            procesos[i].start();
        }
        for (int j = 0; j < procesos.length; j++) {
            procesos[j].join();
        }
    }
    
    
}

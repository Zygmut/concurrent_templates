package h20;

import static java.lang.Thread.sleep;
import java.util.Random;
import java.util.concurrent.Semaphore;
import java.util.logging.Level;
import java.util.logging.Logger;

public class Hydrogen implements Runnable{
    //Semaforo de entrada de Hidrogenos
    private static Semaphore hidrogenoDoble = new Semaphore(2);
    //Semaforo Mutex
    private static Semaphore mutex = new Semaphore(1);
    //Semaforo de Senar
    private static Semaphore senar = new Semaphore(0);
    //Semaforo compartido de levantar oxygen
    private Semaphore oxyAwake, h20finish;
    private static int contador=0;
    
    private int id;

    public Hydrogen(Semaphore oxyAwake, Semaphore h20finish, int id) {
        this.oxyAwake = oxyAwake;
        this.h20finish = h20finish;
        this.id = id;
    }

    @Override
    public void run() {
        System.out.println("Soy el Hidrogeno "+id);
        for (int i = 0; i < 4; i++) {
            dormir();
            try {
                hidrogenoDoble.acquire();
                    mutex.acquire();
                    contador++;
                    if(contador == 1){
                        mutex.release();
                        System.out.println("Soy el Hidrogeno "+id+" senar y me quedo esperando");
                        senar.acquire();
                       
                    }else if(contador==2){
                        mutex.release();
                        System.out.println("Soy el Hidrogeno "+id+ " par y libero un oxigeno");
                        oxyAwake.release();
                        h20finish.acquire();
                        senar.release();
                        
                    }
                mutex.acquire();
                contador--;
                mutex.release();
                hidrogenoDoble.release();
                
                
                
                
            } catch (InterruptedException ex) {
                Logger.getLogger(Hydrogen.class.getName()).log(Level.SEVERE, null, ex);
            }
            
        }
        System.out.println("Hydrogen "+id+" acaba");
    }

    private void dormir(){
        Random random=new Random();
        try {
            sleep(random.nextInt(600-100+1)+100);
        } catch (InterruptedException ex) {
            Logger.getLogger(Hydrogen.class.getName()).log(Level.SEVERE, null, ex);
        }
    }
    
}

package h20;

import static java.lang.Thread.sleep;
import java.util.Random;
import java.util.concurrent.Semaphore;
import java.util.logging.Level;
import java.util.logging.Logger;


public class Oxygen implements Runnable{
    //Semaforo compartido de levantar oxygen
    private Semaphore oxyAwake, h20finish;
    //Id
    private int id;    

    public Oxygen(Semaphore oxyAwake, Semaphore h20finish, int id) {
        this.oxyAwake = oxyAwake;
        this.h20finish = h20finish;
        this.id = id;
    }

    @Override
    public void run() {
        System.out.println("Oxygen "+id);
        for (int i = 0; i < 4; i++) {
            try {
                
                oxyAwake.acquire();
                System.out.println("Oxygen"+id+"sinte");
                if(id==4){
                    
                for (int j = 0; j < 4; j++) {
                    sleep(100);
                    System.out.print("+");
                }
            }else{
                    
                for (int j = 0; j < 4; j++) {
                sleep(100);
                System.out.print("*");
                }
            }
            h20finish.release();
            } catch (InterruptedException ex) {
                Logger.getLogger(Oxygen.class.getName()).log(Level.SEVERE, null, ex);
            }

        }
        System.out.println("Oxygen "+id+" acaba");
    }

}

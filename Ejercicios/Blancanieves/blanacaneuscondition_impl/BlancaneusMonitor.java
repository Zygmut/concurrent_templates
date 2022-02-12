/*
 * Blancaneus i els set nans viuen en una casa on nomes hi ha quatre cadires, 
 * que els nans utilitzen per menjar.
 * Quan un nan torna de treballar de la mina comprova si hi ha una cadira lliure
 * per seure. Si hi ha una cadira lliure, llavors indica la Blancaneus que ja 
 * està assegut, i espera pacientment el seu torn a ser servit. 
 * Quan ha estat servit, Blancaneus li indica que pot començar a menjar. 
 * El nan menja i quan acaba, deixa la cadira lliure i torna a la mina. 
 * Per la seva banda, Blancaneus quan no té cap nan pendent de servir, s’adorm.
 *
 */
package pkg291_blanacaneusmonitor;

import java.util.concurrent.Semaphore;

/**
 *
 * @author miquelmascarooliver
 */
public class BlancaneusMonitor {

    /**
     * @param args the command line arguments
     */
    
    static Monitor monitor = new Monitor();

    public static void main(String[] args) throws InterruptedException {

        Thread b = new Thread(new Blancaneus(monitor));
        b.start();
        String[] nomNan = {"Mudet", "Esternuts", "Vergonyós", "Dormilega",
            "Feliç", "Rondinaire", "Savi"};
        Thread[] nan = new Thread[nomNan.length];
        for (int i = 0; i < nomNan.length; i++) {
            nan[i] = new Thread(new Nan(nomNan[i], monitor));
            nan[i].start();
        }
        b.join();
        for (int i = 0; i < nomNan.length; i++) {
            nan[i].join();
        }
    }

}

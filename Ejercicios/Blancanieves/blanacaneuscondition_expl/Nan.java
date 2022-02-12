/*
 * 
 */
package pkg292_blanacaneuscondition;

import java.util.logging.Level;
import java.util.logging.Logger;

/**
 *
 * @author miquelmascarooliver
 */
public class Nan implements Runnable {

    private String nom;
    private final int QUANTITAT = 2;
    private MonitorCondition monitor;

    public Nan(String nom, MonitorCondition monitor) {
        this.nom = nom;
        this.monitor = monitor;
    }

    @Override
    public void run() {
        System.out.println("BON DIA som en " + this.nom);
        for (int i = 0; i < QUANTITAT; i++) {
            try {
                System.out.println(this.nom + " treballa a la mina");
                Thread.sleep((long) (Math.random() * 100000));
                System.out.println(this.nom + " espera per una cadira");
                monitor.demanaCadira();
                System.out.println(this.nom + " ja seu");
                System.out.println(this.nom + " espera torn per menjar");
                monitor.demanaMenjar();
                System.out.println("----------------> " + this.nom + " menja!!!");
                Thread.sleep((long) (Math.random() * 1000));
                monitor.senVa();
            } catch (InterruptedException ex) {
                System.out.println(this.nom + " EXEPCIÓ!" + ex.getMessage());
            }
        }
        monitor.incrementaaDormir();
        System.out.println(this.nom + " se'n va a DORMIR " + monitor.getaDormir() + "/7");
    }

}

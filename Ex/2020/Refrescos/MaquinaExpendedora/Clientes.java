/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package MaquinaExpendedora;

import java.util.Random;
import java.util.logging.Level;
import java.util.logging.Logger;

/**
 *
 * @author alber
 */
public class Clientes implements Runnable{
    
    Random r = new Random();
    private final int consumiciones = r.nextInt(10);
    String nom;
    private int consum = 0; 
    private final Monitor monitor;

    public Clientes(String nom, Monitor monitor) {
        this.nom = nom;
        this.monitor = monitor;
    }
    
    @Override
    public void run() {
        
        System.out.println(this.nom + " arriba i fara: " + consumiciones + "consumiciones");
        
        while(consum < consumiciones){
            try {
                monitor.consumirRefresc();
                consum++;
                System.out.println(this.nom + " agafa un refresc - consumició: " + consum);
                Thread.sleep((long)(Math.random()*5000));
            } catch (InterruptedException ex) {
                Logger.getLogger(Clientes.class.getName()).log(Level.SEVERE, null, ex);
            }
        }
        monitor.senVa();
        System.out.println(this.nom + " se'n va, queden: " + monitor.getConsumidors());
    }
    
}

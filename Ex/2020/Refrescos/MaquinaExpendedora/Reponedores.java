/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package MaquinaExpendedora;

import java.util.logging.Level;
import java.util.logging.Logger;

/**
 *
 * @author alber
 */
public class Reponedores implements Runnable{

    private final String nom;
    private final Monitor monitor;

    public Reponedores(String nom, Monitor monitor) {
        this.nom = nom;
        this.monitor = monitor;
    }  
    
    @Override
    public void run() {
        System.out.println("El reposador: " + this.nom + " ha arribat");
        while(monitor.getConsumidors()!=0){
            try {
                Thread.sleep((long)(Math.random()*5000));
                if(monitor.getRefrescs()!=monitor.getMaxRefresc()){
                System.out.println("Reponedor: "+ this.nom + " hi ha: " + monitor.getRefrescs() + " refrescs i en posa: " + (monitor.getMaxRefresc()- monitor.getRefrescs()));
                monitor.replenarRefresc();
                }
                Thread.sleep((long)(Math.random()*10000));
            } catch (InterruptedException ex) {
                Logger.getLogger(Reponedores.class.getName()).log(Level.SEVERE, null, ex);
            }
        }
        System.out.println("El reposador: " + this.nom + " se'n va");
    }
    
    
}

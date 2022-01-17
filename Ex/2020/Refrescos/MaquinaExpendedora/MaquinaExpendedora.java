/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package MaquinaExpendedora;

import java.util.Random;

/**
 *
 * @author alber
 */
public class MaquinaExpendedora {
    
    Random r = new Random();
    private final int consumidors = r.nextInt(10);
    private final int reponedors = r.nextInt(5);
    private final Monitor monitor = new Monitor(consumidors);
    
    public static void main(String[] args) throws InterruptedException {
        MaquinaExpendedora m = new MaquinaExpendedora();
        m.inici();
    }
    
    public void inici() throws InterruptedException{
        System.out.println("Inici de la simulació");
        System.out.println("Avui hi ha: " + consumidors + " clients i :" + reponedors + " reponedors");
        System.out.println("La maquina esta buida, hi caben 10 refrescs");
        if(reponedors!=0){
        Thread[] consum = new Thread[consumidors];
        Thread[] repon = new Thread[reponedors];
        
        for(int i = 0; i < consumidors; i++){
            String nom = String.valueOf(i);
            consum[i] =new Thread(new Clientes(nom, monitor));
            consum[i].start();
        }
        
        for(int i = 0; i < reponedors; i++){
            String nom = String.valueOf(i);
            repon[i]= new Thread(new Reponedores(nom, monitor));
            repon[i].start();
        }
        
        for(int i = 0; i < consumidors; i++){
           consum[i].join();
        }
        
        for(int i = 0; i < reponedors; i++){
            repon[i].join();
        }
            System.out.println("Acaba la simulació");
        }else{
            System.out.println("Simulacio abortada no hi ha reponedors");
        }
        
        
    }
}

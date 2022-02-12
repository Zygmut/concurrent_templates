
package pkg291_blanacaneusmonitor;

/**
 *
 * @author miquelmascarooliver
 */
class Monitor {

    private int aDormir, perMenjar, cadires;
    static final int NUMCADIRES = 4;

    public Monitor() {
        this.aDormir = 0;
        this.perMenjar = 0;
        this.cadires = NUMCADIRES;
    }

    synchronized int getaDormir() {
        return aDormir;
    }

    synchronized void donaMenjar() throws InterruptedException {
        perMenjar--;
        System.out.println("perMenjar =  " + perMenjar + " cadires = " + cadires);
        notifyAll(); //Allibera un nan bloquejat a demanaMenjar
    }

    synchronized void incrementaaDormir() {
        aDormir++;
    }

    synchronized void demanaCadira() throws InterruptedException {
        while (cadires == 0) {
            wait();
        }
        cadires--;
    }
    synchronized void demanaMenjar() throws InterruptedException {
        perMenjar++;
        System.out.println("perMenjar =  " + perMenjar + " cadires = " + cadires);
        wait();
    }

    synchronized void senVa() {
        cadires++;
        notifyAll(); // Allibera a un nan bloquejat a demanaCadira
    }

    synchronized int getPerMenjar() {
        return perMenjar;
    }


}

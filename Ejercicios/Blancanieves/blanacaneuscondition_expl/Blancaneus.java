/*
 * 
 */
package pkg292_blanacaneuscondition;

/**
 *
 * @author miquelmascarooliver
 */
class Blancaneus implements Runnable {

    private MonitorCondition monitor;

    public Blancaneus(MonitorCondition monitor) {
        this.monitor = monitor;
    }

    @Override
    public void run() {
        System.out.println("BON DIA som na Blancaneus");
        while (monitor.getaDormir() < 7) {
            try {
                if (monitor.getPerMenjar() == 0) {
                    System.out.println("Blancaneus se'n va a fer una passejada ");
                    Thread.sleep((long) (Math.random() * 50000));
                } else {
                    System.out.println("Blancaneus cuina per un nan");
                    Thread.sleep((long) (Math.random() * 5000));
                    System.out.println("Blancaneus té el menjat cuit");
                    monitor.donaMenjar();
                }
            } catch (InterruptedException ex) {
                System.out.println(" Blancaneus EXEPCIÓ!" + ex.getMessage());
            }
        }
        System.out.println("Blancaneus s'en va a DORMIR");
    }

}

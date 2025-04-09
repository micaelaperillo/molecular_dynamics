package ar.edu.itba.SdS;

import java.util.PriorityQueue;

public class MolecularSimulation {
    private final Container container;
    private final PriorityQueue<Event> eventQueue=new PriorityQueue<>();

    public MolecularSimulation(int particlesAmount,double particlesSpeed,double particlesRadius){
        this.container=new Container(particlesAmount,particlesSpeed,particlesRadius);
        container.initializeParticles();
    }

}

package ar.edu.itba.SdS;

import java.util.List;
import java.util.PriorityQueue;

public class MolecularSimulation {
    private final Container container;
    private final PriorityQueue<Event> eventQueue=new PriorityQueue<>();
    private final List<Particle> particles;
    private double currentTime=0;
    public MolecularSimulation(int particlesAmount,double particlesSpeed,double particlesRadius){
        this.container=new Container(particlesAmount,particlesSpeed,particlesRadius);
        this.particles=container.getParticles();
        container.initializeParticles();
    }

    private void predictCollisions(Particle p) {
        for (Particle other : particles) {
            if (p == other)
                continue;
            Double t = timeToParticleCollision(p, other);
            if (t != null)
                eventQueue.add(new Event(currentTime + t, p, other));
        }
    }
    private Double timeToParticleCollision(Particle p1,Particle p2){
       double [] dr={p2.getXPosition()-p1.getXPosition(), p2.getYPosition()-p1.getYPosition()};
       double [] dv={p2.getXVelocity()-p1.getXVelocity(), p2.getYVelocity()-p1.getYVelocity()};
       double dvdr=VectorialUtils.scalarProduct(dr,dv);
       if(dvdr>=0)
           return null;
       double sigma=p1.getRadius()+p2.getRadius();
       double d=dvdr*dvdr-VectorialUtils.scalarProduct(dv,dv)*(VectorialUtils.scalarProduct(dr,dr)-(sigma*sigma));
       if(d<0)
           return null;
       return -(dvdr+Math.sqrt(d))/VectorialUtils.scalarProduct(dv,dv);
    }

}

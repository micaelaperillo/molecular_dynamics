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
        initializeEvents();
    }

    private void initializeEvents() {
        for (Particle p : container.getParticles()) {
            calculateWallCollision(p);
            calculateObstacleCollision(p);
            predictCollisions(p);
        }
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

    // Wall collision: Intersection with circle of radius Re
    private void calculateWallCollision(Particle p) {
        double x = p.getXPosition(), y = p.getYPosition();
        double vx = p.getXVelocity(), vy = p.getYVelocity();
        double radius = p.getRadius();
        double Re = Container.CONTAINER_DIAMETER / 2;

        double a = vx * vx + vy * vy;
        double b = 2 * (x * vx + y * vy);
        double c = x * x + y * y - (Re - radius) * (Re - radius);

        solveQuadraticToFindCollisionTime(p, a, b, c);
    }

    // Fixed obstacle collision: Intersection with circle of radius Ro
    private void calculateObstacleCollision(Particle p) {
        double x = p.getXPosition(), y = p.getYPosition();
        double vx = p.getXVelocity(), vy = p.getYVelocity();
        double radius = p.getRadius();
        double Ro = Container.OBSTACLE_RADIUS;

        double a = vx * vx + vy * vy;
        double b = 2 * (x * vx + y * vy);
        double c = x * x + y * y - (Ro + radius) * (Ro + radius);

        solveQuadraticToFindCollisionTime(p, a, b, c);
    }

    private void solveQuadraticToFindCollisionTime(Particle p, double a, double b, double c) {
        double delta = b * b - 4 * a * c;
        if (delta >= 0) {
            double t1 = (-b - Math.sqrt(delta)) / (2 * a);
            double t2 = (-b + Math.sqrt(delta)) / (2 * a);
            double collisionTime = Math.min(t1 > 0 ? t1 : Double.MAX_VALUE, t2 > 0 ? t2 : Double.MAX_VALUE);
            if (collisionTime != Double.MAX_VALUE) {
                eventQueue.add(new Event(collisionTime, p));
            }
        }
    }

}

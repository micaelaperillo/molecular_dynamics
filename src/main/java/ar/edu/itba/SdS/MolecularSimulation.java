package ar.edu.itba.SdS;

import java.util.List;
import java.util.PriorityQueue;

public class MolecularSimulation {
    private final Container container;
    private final PriorityQueue<Event> eventQueue=new PriorityQueue<>();
    private final List<Particle> particles;
    private double currentTime=0;
    private final double maxSimulationTime;
    private final boolean obstaclePresent;
    public MolecularSimulation(int particlesAmount, double particlesSpeed, double particlesRadius, double maxSimulationTime,boolean obstaclePresent) {
        this.container = new Container(particlesAmount, particlesSpeed, particlesRadius,obstaclePresent);
        this.obstaclePresent=obstaclePresent;
        this.particles = container.getParticles();
        this.maxSimulationTime = maxSimulationTime;
        container.initializeParticles();
        initializeEvents();
    }

    private void initializeEvents() {
        for (Particle p : container.getParticles()) {
            predictCollisions(p);
        }
    }

    public void runSimulation() {
        while (!eventQueue.isEmpty() && currentTime < maxSimulationTime) {
            Event event = eventQueue.poll();
            if(!event.isValidEvent())
                continue;
            double eventTime = event.getEventTime();
            double dt = eventTime - currentTime;

            // Advance particles to the time of the event
            for (Particle p : particles) {
                p.moveParticle(dt);
            }

            // Update simulation time
            currentTime = eventTime;

            // Handle the collision
            switch (event.getType()) {
                case WALL:
                    handleWallCollision(event.getParticle1());
                    break;
                case OBSTACLE:
                    handleObstacleCollision(event.getParticle1());
                    break;
                case PARTICLE_PARTICLE:
                    handleParticleCollision(event.getParticle1(), event.getParticle2());
                    break;
            }

            // Predict new events for the particles involved in the collision
            predictNewEvents(event);
        }
    }

    private void handleParticleCollision(Particle p1, Particle p2) {
        // TODO Implement
    }

    private void handleWallCollision(Particle p) {
        double x = p.getXPosition();
        double y = p.getYPosition();
        double vx = p.getXVelocity();
        double vy = p.getYVelocity();

        double norm = Math.sqrt(x * x + y * y);
        double normalX = x /  norm;
        double normalY = y /  norm;

        // Reverse the velocity
        double dotProduct = vx * normalX + vy * normalY;
        p.setVelocity(vx - 2 * dotProduct * normalX, vy - 2 * dotProduct * normalY);
    }

    private void handleObstacleCollision(Particle p) {
        if(!this.obstaclePresent)
            return;
        // TODO Implement
    }
    
    private void predictNewEvents(Event event) {
        Particle p1 = event.getParticle1();
        Particle p2 = event.getParticle2();

        // Remove invalidated events for the particles involved
        eventQueue.removeIf(e -> e.involves(p1) || (p2 != null && e.involves(p2)));

        // Predict new events
        predictCollisions(p1);
        predictCollisions(p2);
    }

    private void predictCollisions(Particle p) {
        if (p != null) {
            calculateParticleCollisions(p);
            calculateObstacleCollision(p);
            calculateWallCollision(p);
        }
    }

    private void calculateParticleCollisions(Particle p) {
        for (Particle other : particles) {
            if (p == other)
                continue;
            Double t = timeToParticleCollision(p, other);
            if (t != null)
                eventQueue.add(new Event(currentTime + t, p, other, EventType.PARTICLE_PARTICLE));
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

        solveQuadraticToFindCollisionTime(p, a, b, c, EventType.WALL);
    }

    // Fixed obstacle collision: Intersection with circle of radius Ro
    private void calculateObstacleCollision(Particle p) {
        if (!this.obstaclePresent)
            return;
        double x = p.getXPosition(), y = p.getYPosition();
        double vx = p.getXVelocity(), vy = p.getYVelocity();
        double radius = p.getRadius();
        double Ro = Container.OBSTACLE_RADIUS;

        double a = vx * vx + vy * vy;
        double b = 2 * (x * vx + y * vy);
        double c = x * x + y * y - (Ro + radius) * (Ro + radius);

        solveQuadraticToFindCollisionTime(p, a, b, c, EventType.OBSTACLE);
    }

    private void solveQuadraticToFindCollisionTime(Particle p, double a, double b, double c, EventType eventType) {
        double delta = b * b - 4 * a * c;
        if (delta >= 0) {
            double t1 = (-b - Math.sqrt(delta)) / (2 * a);
            double t2 = (-b + Math.sqrt(delta)) / (2 * a);
            double collisionTime = Math.min(t1 > 0 ? t1 : Double.MAX_VALUE, t2 > 0 ? t2 : Double.MAX_VALUE);
            if (collisionTime != Double.MAX_VALUE) {
                eventQueue.add(new Event(collisionTime, p, eventType));
            }
        }
    }

}

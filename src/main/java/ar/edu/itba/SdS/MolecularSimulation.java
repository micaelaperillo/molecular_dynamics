package ar.edu.itba.SdS;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.nio.file.StandardOpenOption;
import java.util.Comparator;
import java.util.List;
import java.util.PriorityQueue;

public class MolecularSimulation {
    private static final double EPSILON = 1e-20;
    private final Container container;
    private final PriorityQueue<Event> eventQueue=new PriorityQueue<>(Comparator.comparing(Event::getEventTime));
    private final List<Particle> particles;
    private double currentTime=0;
    private final double maxSimulationTime;
    private final boolean obstaclePresent;
    private double totalWallImpulse = 0;
    private double totalObstacleImpulse = 0;
    private double totalWallPressure = 0;
    private double totalObstaclePressure = 0;

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

    public void runSimulation() throws IOException{
        Files.deleteIfExists(Paths.get(String.format("output-%d.txt",particles.size())));
        while (!eventQueue.isEmpty() && currentTime < maxSimulationTime) {
            Event event = eventQueue.poll();
            double eventTime = event.getEventTime();

            // Just for debug
            System.out.printf("CurrentTime: %.10e, EventTime: %.10e, QueueSize: %d\n",
                    currentTime, eventTime, eventQueue.size());

            if(event.isValidEvent() && eventTime > currentTime) {
                // Advance particles to the time of the event
                double dt = eventTime - currentTime;
                for (Particle p : particles) {
                    p.moveParticle(dt);
                }

                // Just for debug
                if (eventTime > currentTime) {
                    System.out.printf("updating time simulation by dt: %.6e\n", dt);
                }
                currentTime = eventTime;
                System.out.printf("Simulation Time is now: %.6e\n", currentTime);

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

                calculateAndPrintPressures();
                writeOutput();
                predictNewEvents(event);
            }
            // Just for debug
            System.out.printf("IsValidEvent: %s, eventInTheFuture: %s\n", event.isValidEvent(), eventTime > currentTime);
        }
    }

    private void handleParticleCollision(Particle p1, Particle p2) {
        double dx=p2.getXPosition()-p1.getXPosition();
        double dy=p2.getYPosition()-p1.getYPosition();
        double dvx=p2.getXVelocity()-p1.getXVelocity();
        double dvy=p2.getYVelocity()-p1.getYVelocity();

        double dvdr=dx*dvx+dy*dvy;

        double sigma=Math.sqrt(dx*dx+dy*dy);
        double j=(2*p1.getMass()*p2.getMass()*dvdr)/(sigma*(p1.getMass()+p2.getMass()));

        double jx=j*dx/sigma;
        double jy=j*dy/sigma;

        p1.setVelocity(p1.getXVelocity()+(jx/p1.getMass()),p1.getYVelocity()+(jy/p1.getMass()));
        p2.setVelocity(p2.getXVelocity()-(jx/p2.getMass()),p2.getYVelocity()-(jy/p2.getMass()));

        p1.incrementCollisionCount();
        p2.incrementCollisionCount();
    }

    private void handleWallCollision(Particle p) {
        double[] position = {p.getXPosition(), p.getYPosition()};
        double[] velocity = {p.getXVelocity(), p.getYVelocity()};
        double norm = Math.sqrt(VectorialUtils.scalarProduct(position, position));
        double rc = Container.CONTAINER_DIAMETER / 2.0;
        double[] normal = VectorialUtils.scalarDivision(position, norm);
        double dotProduct = VectorialUtils.scalarProduct(velocity, normal);
        double impulseMagnitude = 2 * p.getMass() * Math.abs(dotProduct);
        totalWallImpulse += impulseMagnitude;

        p.setVelocity(
                velocity[0] - 2 * dotProduct * normal[0],
                velocity[1] - 2 * dotProduct * normal[1]
        );
        p.incrementCollisionCount();

    }

    private void handleObstacleCollision(Particle p) {
        if (!obstaclePresent) {
            return;
        }

        double[] position = {p.getXPosition(), p.getYPosition()};
        double[] velocity = {p.getXVelocity(), p.getYVelocity()};
        double norm = Math.sqrt(VectorialUtils.scalarProduct(position, position));
        double[] normal = VectorialUtils.scalarDivision(position, norm);
        double dotProduct = VectorialUtils.scalarProduct(velocity, normal);
        double impulseMagnitude = 2 * p.getMass() * Math.abs(dotProduct);
        totalObstacleImpulse += impulseMagnitude;

        p.setVelocity(
                velocity[0] - 2 * dotProduct * normal[0],
                velocity[1] - 2 * dotProduct * normal[1]
        );
        p.incrementCollisionCount();

    }

    private void predictNewEvents(Event event) {
        Particle p1 = event.getParticle1();
        Particle p2 = event.getParticle2();

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
    private void writeOutput() throws IOException {
        Path path=Paths.get(String.format("output-%d.txt",particles.size()));
        if(!Files.exists(path))
            Files.write(path,String.format("%d\n",particles.size()).getBytes(),StandardOpenOption.CREATE, StandardOpenOption.APPEND);
        Files.write(path,String.format("%.3e\n",currentTime).getBytes(),StandardOpenOption.APPEND);
        Files.write(path,String.format("%.3e\n",totalWallPressure).getBytes(),StandardOpenOption.APPEND);
        Files.write(path,String.format("%.3e\n",totalObstaclePressure).getBytes(),StandardOpenOption.APPEND);
        for(Particle p:particles){
            Files.write(path,p.toString().getBytes(), StandardOpenOption.APPEND);
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
       double dvdv=VectorialUtils.scalarProduct(dv,dv);
       if(dvdr>=0)
           return null;
       double sigma=p1.getRadius()+p2.getRadius();
       double d=dvdr*dvdr-dvdv*(VectorialUtils.scalarProduct(dr,dr)-(sigma*sigma));
       double dt = -(dvdr + Math.sqrt(d)) / dvdv;

       return (d >= 0 && dt >= 0) ? dt : null;
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
            double threshold = 1e-10; // TODO: Check this
            double collisionTime = Math.min(t1 > threshold ? t1 : Double.MAX_VALUE, t2 > threshold ? t2 : Double.MAX_VALUE);
            if (collisionTime != Double.MAX_VALUE) {
                eventQueue.add(new Event(currentTime+collisionTime, p, eventType));
            }
        }
    }

    private void calculateAndPrintPressures() {
        double wallLength = Math.PI * Container.CONTAINER_DIAMETER; // Circumference of the container
        double obstacleLength = 2 * Math.PI * Container.OBSTACLE_RADIUS; // Circumference of the obstacle

        totalWallPressure = totalWallImpulse / (wallLength * currentTime);
        totalObstaclePressure = obstaclePresent ? totalObstacleImpulse / (obstacleLength * currentTime) : 0;

        System.out.printf("Wall Pressure: %.6e\n", totalWallPressure);
        if (obstaclePresent) {
            System.out.printf("Obstacle Pressure: %.6e\n", totalObstaclePressure);
        }
    }
}

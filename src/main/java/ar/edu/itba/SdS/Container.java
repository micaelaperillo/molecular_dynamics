package ar.edu.itba.SdS;

import java.util.ArrayList;
import java.util.List;
import java.util.Random;

public class Container {
    private static final double CONTAINER_DIAMETER=0.1;
    private final List<Particle> particles=new ArrayList<>();
    private static final double OBSTACLE_RADIUS=0.005;
    private static final Random rand=new Random();

    private final double particlesSpeed,particlesRadius;
    private final int particlesAmount;
    public Container(int particlesAmount,double particlesSpeed,double particlesRadius){
        this.particlesAmount=particlesAmount;
        this.particlesSpeed =particlesSpeed;
        this.particlesRadius=particlesRadius;
    }

    public void initializeParticles() {
        double minR = OBSTACLE_RADIUS + particlesRadius;
        double maxR = CONTAINER_DIAMETER/2 - particlesRadius;
        for(int i=0;i<particlesAmount;i++) {
            int maxAttempts = 10000;
            boolean placed = false;
            for (int attempts = 0; attempts < maxAttempts && !placed; attempts++) {
                double r = minR + rand.nextDouble() * (maxR - minR);
                double theta = rand.nextDouble() * 2 * Math.PI;
                double x = r * Math.cos(theta);
                double y = r * Math.sin(theta);
                double velocityAngle = rand.nextDouble() * 2 * Math.PI;
                double vx = particlesSpeed * Math.cos(velocityAngle);
                double vy = particlesSpeed * Math.sin(velocityAngle);

                Particle p = new Particle(particlesRadius, x, y, vx, vy, 1);
                if (isValidPosition(p)) {
                    particles.add(p);
                    placed = true;
                }
            }
            if (!placed) {
                throw new RuntimeException("Max attempts");
            }
            System.out.println(particles.size());

        }
    }

    private boolean isValidPosition(Particle newParticle) {
        double x = newParticle.getXPosition();
        double y = newParticle.getYPosition();
        double radius = newParticle.getRadius();
        double distToCenter = Math.sqrt(x*x + y*y);
        if (distToCenter + radius > CONTAINER_DIAMETER/2) {
            return false;
        }
        if (distToCenter < radius + OBSTACLE_RADIUS) {
            return false;
        }
        for (Particle p : particles) {
            if (newParticle.overlapsWith(p)) {
                return false;
            }
        }
        return true;
    }

    public List<Particle> getParticles(){return particles;}
}

package ar.edu.itba.SdS;


public class Particle {
    private final double radius,mass;
    private double x, y, vx, vy;
    private int collisionCount=0;

    public Particle(double radius,double x,double y,double vx,double vy,double mass) {
        this.radius = radius;
        this.x = x;
        this.y = y;
        this.vx = vx;
        this.vy = vy;
        this.mass = mass;
    }
    public boolean overlapsWith(Particle other) {
        double dx = this.x - other.x;
        double dy = this.y - other.y;
        double distSq = dx * dx + dy * dy;
        double minDist = this.radius + other.radius;
        return distSq < minDist * minDist;
    }
    @Override
    public String toString(){
        return String.format("%.3f %.3f %.3f %.3f\n",this.x,this.y,this.vx,this.vy);
    }
    public void moveParticle(double dt) {
        x+=vx*dt;
        y+=vy*dt;
    }
    public double getKineticEnergy(){
        return mass*(vx*vx+vy*vy)/2;
    }
    public double getXVelocity(){return this.vx;}
    public double getYVelocity(){return this.vy;}
    public void incrementCollisionCount(){this.collisionCount++;}
    public int getCollisionCount(){return collisionCount;}
    public double getVelocityModule(){return Math.sqrt(vx*vx+vy*vy);}
    public double getRadius() {return radius;}
    public double getMass() {return mass;}
    public double getXPosition() {return x;}
    public double getYPosition() {return y;}

    public void setVelocity(double vx, double vy) {
        this.vx = vx;
        this.vy = vy;
    }
}

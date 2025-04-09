package ar.edu.itba.SdS;

public class Event implements Comparable<Event>{
    private final double time;
    private final Particle particle;

    public Event(double time,Particle particle){
        this.time=time;
        this.particle=particle;
    }

    public double getTime(){return this.time;}
    public Particle getParticle(){return this.particle;}

    @Override
    public int compareTo(Event o) {
        return Double.compare(time,o.time);
    }
}

package ar.edu.itba.SdS;

public class Event implements Comparable<Event>{
    private final double time;
    private final Particle particle1;
    private final Particle particle2;

    public Event(double time,Particle particle1){
        this.time=time;
        this.particle1=particle1;
        this.particle2=null;
    }
    public Event(double time,Particle particle1,Particle particle2){
        this.time=time;
        this.particle1=particle1;
        this.particle2=particle2;
    }

    public double getTime(){return this.time;}
    public Particle getParticle1(){return this.particle1;}
    public Particle getParticle2(){return this.particle2;}

    @Override
    public int compareTo(Event o) {
        return Double.compare(time,o.time);
    }
}

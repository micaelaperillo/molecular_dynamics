package ar.edu.itba.SdS;

import lombok.Getter;

@Getter
public class Event implements Comparable<Event> {
    private final double time;
    private final Particle particle1;
    private final Particle particle2;
    private final EventType type;

    public Event(double time, Particle particle1, EventType type) {
        this.time = time;
        this.particle1 = particle1;
        this.particle2 = null;
        this.type = type;
    }

    public Event(double time, Particle particle1, Particle particle2, EventType type) {
        this.time = time;
        this.particle1 = particle1;
        this.particle2 = particle2;
        this.type = type;
    }

    @Override
    public int compareTo(Event o) {
        return Double.compare(time, o.time);
    }

    public boolean involves(Particle particle) {
        return particle.equals(particle1) || particle.equals(particle2);
    }
}

package ar.edu.itba.SdS;

import lombok.Getter;

@Getter
public class Event {
    private final double eventTime;
    private final Particle particle1;
    private final Particle particle2;
    private final int particle1CollisionsCount;
    private final int particle2CollisionsCount;
    private final EventType type;

    public Event(double eventTime, Particle particle1, EventType type) {
        this.eventTime = eventTime;
        this.particle1 = particle1;
        this.particle1CollisionsCount=particle1.getCollisionCount();
        this.particle2 = null;
        this.particle2CollisionsCount=0;
        this.type = type;
    }

    public Event(double eventTime, Particle particle1, Particle particle2, EventType type) {
        this.eventTime = eventTime;
        this.particle1 = particle1;
        this.particle1CollisionsCount=particle1.getCollisionCount();
        this.particle2CollisionsCount=particle2.getCollisionCount();
        this.particle2 = particle2;
        this.type = type;
    }

    public boolean involves(Particle particle) {
        return particle.equals(particle1) || particle.equals(particle2);
    }

    public boolean isValidEvent(){
        if(this.particle1CollisionsCount!=this.particle1.getCollisionCount())
            return false;
        return this.particle2==null || this.particle2.getCollisionCount()==this.particle2CollisionsCount;
    }
}

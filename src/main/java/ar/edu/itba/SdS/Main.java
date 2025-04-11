package ar.edu.itba.SdS;

import java.io.IOException;

public class Main {
    public static void main(String[] args) throws IOException {
        MolecularSimulation simulation=new MolecularSimulation(210,1,5e-4,10,true);
        simulation.runSimulation();
    }
}
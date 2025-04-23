package ar.edu.itba.SdS;

import java.io.IOException;

public class Main {
    public static void main(String[] args) throws IOException {
        MolecularSimulation s1=new MolecularSimulation(210,1,5e-4,0.05,true);
        s1.runSimulation();

        MolecularSimulation s2=new MolecularSimulation(210,3,5e-4,0.05,true);
        s2.runSimulation();

        MolecularSimulation s3=new MolecularSimulation(210,6,5e-4,0.05,true);
        s3.runSimulation();

        MolecularSimulation s4=new MolecularSimulation(210,10,5e-4,0.05,true);
        s4.runSimulation();


    }
}
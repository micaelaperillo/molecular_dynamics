package ar.edu.itba.SdS;

public class VectorialUtils {

    public static double scalarProduct(double[] v1,double [] v2){
        if (v1.length!=v2.length)
            throw new RuntimeException("Distintas longitudes de producto escalar");
        double result=0;
        for(int i=0;i<v1.length;i++){
            result+=v1[i]*v2[i];
        }
        return result;
    }
}

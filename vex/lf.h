#ifndef __lf__
#define __lf__

// to pass by reference, use the export flag

// one dimensional gaussian (or normal or bell) distribution
function float gaussian( float height; float centre; float range; float x )
{
        float o = x - centre;
        return height * exp( - o * o  / ( 0.1 * range * range ) );
}

function float smoothstep(float min; float max; float x)
{
    if( x < min ){
        return 0;
    }
    if( x >= max ){
        return 1;
    }
    
    x = (x-min) / (max-min);
    return (x*x) * (3-2*x);
}

function float smoothstep2( float min; float max; float x)
{
    float r2 = x * x;
    return r2 * x * ( 6*r2 - 15*x + 10 );
}

function float bias(float value; float amount)
{
    float result = amount / (((1/value)-2 ) * (1 - amount)+1);  
    return result;
}

function float gain(float x; float amount)
{    
    if (x <= 0.0){
        return 0;
    }
    if (x >= 1.0){
        return 1;
    }
    if( x < 0.5){
        return bias(2*x, amount) * 0.5;
    }
    if( x >= 0.5){
        return 1 - bias(2*(1-x), amount) * 0.5;
    }
}

// makes a unique array of strings (extend to other types)
function string[] make_unique(string my_array[]){
    string unique[];
    foreach (string attr; my_array){
        if (find(unique,attr)<0){
            append(unique, attr);
        }
    }
    return unique;
}


#endif

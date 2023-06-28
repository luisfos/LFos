#ifndef __glsl__
#define __glsl__

// to pass by reference, use the export flag


float step(float edge; float x){
    if( x < edge ){
        return 0.0;
    }else{
        return 1.0;
    }
    //return filterstep(edge,x,"filter","point");
}

vector2 step(vector2 edge; vector2 x){
    return set(
            step(edge.x,x.x),
            step(edge.y,x.y)
            );
}

vector step(vector edge; vector x){
    return set(
            step(edge.x,x.x),
            step(edge.y,x.y),
            step(edge.z,x.z)
            );
}

vector2 step(float edge; vector2 x){
    return set(
            step(edge,x.x),
            step(edge,x.y)
            );
}

vector step(float edge; vector x){
    return set(
            step(edge,x.x),
            step(edge,x.y),
            step(edge,x.z)
            );
}


// standard smoothstep function
function float smoothstep(float edge0; float edge1; float x)
{
    float t = clamp((x - edge0) / (edge1 - edge0), 0.0, 1.0);
    return t * t * (3.0 - 2.0 * t);
}

// with defaults of range 0-1
function float smoothstep(float x)
{
    if( x < 0 ){
        return 0;
    }
    if( x >= 1 ){
        return 1;
    }    
    return (x*x) * (3-2*x);
}

// vec2
function vector2 smoothstep(float edge0; float edge1; vector2 x)
{
    float t0 = clamp((x.x - edge0) / (edge1 - edge0), 0.0, 1.0);
    t0 = t0 * t0 * (3.0 - 2.0 * t0);
    float t1 = clamp((x.y - edge0) / (edge1 - edge0), 0.0, 1.0);
    t1 = t1 * t1 * (3.0 - 2.0 * t1);
    return set(t0,t1);
}

// vec3
function vector smoothstep(float edge0; float edge1; vector x)
{
    float t0 = clamp((x.x - edge0) / (edge1 - edge0), 0.0, 1.0);
    t0 = t0 * t0 * (3.0 - 2.0 * t0);
    float t1 = clamp((x.y - edge0) / (edge1 - edge0), 0.0, 1.0);
    t1 = t1 * t1 * (3.0 - 2.0 * t1);
    float t2 = clamp((x.z - edge0) / (edge1 - edge0), 0.0, 1.0);
    t2 = t2 * t2 * (3.0 - 2.0 * t2);
    return set(t0,t1,t2);
}

function vector2 smoothstep(vector2 edge0; vector2 edge1; vector2 x)
{
    float t0 = clamp((x.x - edge0.x) / (edge1.x - edge0.x), 0.0, 1.0);
    t0 = t0 * t0 * (3.0 - 2.0 * t0);
    float t1 = clamp((x.y - edge0.y) / (edge1.y - edge0.y), 0.0, 1.0);
    t1 = t1 * t1 * (3.0 - 2.0 * t1);
    return set(t0,t1);
}

function vector smoothstep(vector edge0; vector edge1; vector x)
{
    float t0 = clamp((x.x - edge0.x) / (edge1.x - edge0.x), 0.0, 1.0);
    t0 = t0 * t0 * (3.0 - 2.0 * t0);
    float t1 = clamp((x.y - edge0.y) / (edge1.y - edge0.y), 0.0, 1.0);
    t1 = t1 * t1 * (3.0 - 2.0 * t1);
    float t2 = clamp((x.z - edge0.z) / (edge1.z - edge0.z), 0.0, 1.0);
    t2 = t2 * t2 * (3.0 - 2.0 * t2);
    return set(t0,t1,t2);
}



// more accurate smoothstep
function float smoothstep2( float x; float min; float max )
{
	if( x < min ){
        return 0;
    }
    if( x >= max ){
        return 1;
    }   
    x = (x-min) / (max-min);
    float r2 = x * x;
    return r2 * x * ( 6*r2 - 15*x + 10 );
}

// more accurate smoothstep default 0-1
function float smoothstep2(float x)
{
	if( x < 0 ){
        return 0;
    }
    if( x >= 1 ){
        return 1;
    }
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
    return 0;
}





#endif


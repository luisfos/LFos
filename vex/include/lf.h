#ifndef __lf__
#define __lf__

// to pass by reference, use the export flag

// one dimensional gaussian (or normal or bell) distribution
function float gaussian( float x; float height; float centre; float range )
{
        float o = x - centre;
        return height * exp( - o * o  / ( 0.1 * range * range ) );
}

// quick gaussian with default height=1 centre=0.5 range=0.5
function float gaussian( float x )
{
	float o = x - 0.5;
    return exp( - o * o  / ( 0.1 * 0.5 * 0.5 ) );
}

// standard smoothstep function
function float smoothstep(float x; float min; float max)
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

// ease in default range 0-1
function float smoothin( float x )
{
	return x*x*(2-x);
}
// ease out default range 0-1
function float smoothout( float x )
{
	return x*(1+x*(1-x));
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

function float approach(float x; float to; float slow)
{
	return ((x * (slow - 1)) + to) / slow;
}

// overload slerp function to allow slerping between vectors
function vector vlerp(vector v1; vector v2; float bias)
{
	vector ref = {0,1,0};
    if (dot(ref, v1) > 0.9){
        ref = {1,0,0};
    }
	vector4 q1 = dihedral(ref, v1);
	vector4 q2 = dihedral(ref, v2);
	vector4 rot = slerp(q1, q2, bias);
	return qrotate(rot, ref);
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

// remove a list from another list
function string [] removeValues(string arr[]; string remove[])
{
    string keep[];
    foreach(int idx; string arrVal; arr){
        int found = 0;
        foreach(string del; remove){
            if (match(del, arrVal)==1){
                found=1;                
            }        
        }
        if (found==0){
            push(keep, arrVal);
        }
            
    }   
    return keep;
}
// list must be sorted
function int[] removeDuplicates(int arr[]){
    int unique[];
    for(int i=0; i<len(arr)-1; i++){
        int curr = arr[i];
        int next = arr[i+1];
        //printf("curr=%i, next=%i \n", curr, next);
        if (curr != next){            
            push(unique, curr);            
        }    
    }
    push(unique, arr[-1]);
    return unique;
}

void swap ( int array [ ]; int left; int right )
{
    int temp = array [ right ];
    array [ right ] = array [ left ];
    array [ left ] = temp;
}

void quickSort ( int array [ ] )
{
    int stack [ ];
    int pivot;
    int pivotIndex = 0;
    int leftIndex = pivotIndex + 1;
    int rightIndex = arraylength ( array ) - 1;
    
    push ( stack, pivotIndex );
    push ( stack, rightIndex );
    
    int leftIndexOfSubSet, rightIndexOfSubset;
    while ( arraylength ( stack ) > 0 )
    {
        pop ( rightIndexOfSubset, stack );
        pop ( leftIndexOfSubSet, stack );
        
        leftIndex = leftIndexOfSubSet + 1;
        pivotIndex = leftIndexOfSubSet;
        rightIndex = rightIndexOfSubset;
        
        pivot = array [ pivotIndex ];
        
        if ( leftIndex > rightIndex )
            continue;
        
        while ( leftIndex < rightIndex )
        {
            while ( leftIndex <= rightIndex && array [ leftIndex ] <= pivot )
                leftIndex++;
            
            while ( leftIndex <= rightIndex && array [ rightIndex ] >= pivot )
                rightIndex--;
            
            if ( rightIndex >= leftIndex )
                swap ( array, leftIndex, rightIndex );
        }
        
        if ( pivotIndex <= rightIndex )
            if ( array [ pivotIndex ] > array [ rightIndex ] )
                swap ( array, pivotIndex, rightIndex );
        
        if ( leftIndexOfSubSet < rightIndex )
        {
            push ( stack, leftIndexOfSubSet );
            push ( stack, rightIndex - 1 );
        }
        
        if ( rightIndexOfSubset > rightIndex )
        {
            push ( stack, rightIndex + 1 );
            push ( stack, rightIndexOfSubset );
        }
    }
}

function string [] matchInArray(string array[]; string toMatch[])
{
    string matches[];
    foreach(int idx; string arrVal; array)
    {
        int found = 0;
        foreach(string pattern; toMatch)
        {
            if (match(pattern, arrVal)==1){
                found=1;
                break;
            }        
        }
        if (found==1){
            push(matches, arrVal);
        }
            
    }   
    return matches;
}

function float hedge_length(int input; int hedge){
    vector p1 = point(input, "P", hedge_srcpoint(input, hedge));
    vector p2 = point(input, "P", hedge_dstpoint(input, hedge));
    return distance(p1, p2);
}

function float hedge_length2(int input; int hedge){
    vector p1 = point(input, "P", hedge_srcpoint(input, hedge));
    vector p2 = point(input, "P", hedge_dstpoint(input, hedge));
    return distance2(p1, p2);
}

function vector hedge_direction(int input; int hedge){
    vector p1 = point(input, "P", hedge_srcpoint(input, hedge));
    vector p2 = point(input, "P", hedge_dstpoint(input, hedge));
    return p2-p1;
}

function float vertexangle(int input; int linearvertex){
    int h1 = vertexhedge(input, linearvertex);
    int h2 = hedge_prev(input, h1);
    int h3 = hedge_next(input, h1);
    
    float a1, a2, a3;
    float s1, s2, s3;
    
    s1 = hedgelength(0, h3);
    s2 = hedgelength(0, h2);
    s3 = hedgelength(0, h1);
    
    float c = (s2*s2 + s3*s3 - s1*s1) / (2 * s2 * s3);
    return acos(c);
}

// copy attrib between points
function void copypointattribs(int input; int srcpt; int dstpt){
    string attrs[] = detailintrinsic(input, 'pointattributes');
    foreach( string attr; attrs){
        if ( attr == 'P' ){
            continue;
        }        
        int type = pointattribtype(input, attr);
        if (type == 0){ // for integer attrs
        	int size = pointattribsize(input, attr);
        	if ( size == 1 ) {
                int val = int(point(input, attr, srcpt));
                setpointattrib(0, attr, dstpt, val);
            }
    	}

        if (type == 1){
            int size = pointattribsize(input, attr);
            if ( size == 1 ) {
                float val = float(point(input, attr, srcpt));
                setpointattrib(0, attr, dstpt, val);
            } else if ( size == 2 ) {
                vector2 val = vector2(point(input, attr, srcpt));
                setpointattrib(0, attr, dstpt, val);
            } else if ( size == 3 ) {
                vector val = vector(point(input, attr, srcpt));
                setpointattrib(0, attr, dstpt, val);
            } else if ( size == 4 ) {
                vector4 val = vector4(point(input, attr, srcpt));
                setpointattrib(0, attr, dstpt, val);
            } else if ( size == 9 ) {
                matrix3 val = matrix3(point(input, attr, srcpt));
                setpointattrib(0, attr, dstpt, val);
            } else if ( size == 16 ) {
                matrix val = matrix(point(input, attr, srcpt));
                setpointattrib(0, attr, dstpt, val);
            }
        }
    }
}

// copy attrib between prims
function void copyprimattribs(int input; int srcpr; int dstpr){
    string attrs[] = detailintrinsic(input, 'primitiveattributes');
    foreach( string attr; attrs){
        if ( attr == 'P' ){
            continue;
        }    
        int type = primattribtype(input, attr);
        if (type == 0){ // for integer attrs
        	int size = primattribsize(input, attr);
        	if ( size == 1 ) {
                int val = int(prim(input, attr, srcpr));
                setprimattrib(0, attr, dstpr, val);
            }
    	}
        if (type == 1){
            int size = primattribsize(input, attr);
            if ( size == 1 ) {
                float val = float(prim(input, attr, srcpr));
                setprimattrib(0, attr, dstpr, val);
            } else if ( size == 2 ) {
                vector2 val = vector2(prim(input, attr, srcpr));
                setprimattrib(0, attr, dstpr, val);
            } else if ( size == 3 ) {
                vector val = vector(prim(input, attr, srcpr));
                setprimattrib(0, attr, dstpr, val);
            } else if ( size == 4 ) {
                vector4 val = vector4(prim(input, attr, srcpr));
                setprimattrib(0, attr, dstpr, val);
            } else if ( size == 9 ) {
                matrix3 val = matrix3(prim(input, attr, srcpr));
                setprimattrib(0, attr, dstpr, val);
            } else if ( size == 16 ) {
                matrix val = matrix(prim(input, attr, srcpr));
                setprimattrib(0, attr, dstpr, val);
            }
        }
    }
    attrs = detailintrinsic(input, 'primitivegroups');
    foreach( string attr; attrs){
    	int val = inprimgroup(input, attr, srcpr);
    	setprimgroup(0, attr, dstpr, val);
	}
}

#endif


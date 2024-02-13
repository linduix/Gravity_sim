#version 430

out vec4 fragColor;
uniform vec2 resolution;
uniform float time;

uniform vec2 b1pos;
uniform float b1r;
uniform float b1m;

uniform vec2 b2pos;
uniform float b2r;
uniform float b2m;

float G = 6.674 * pow(10.0, -11);

float sdCircle( in vec2 p, in float r )
{
    return length(p)-r;
}

void main() {
    vec2 uv = (gl_FragCoord.xy - 0.5 * resolution.xy) / resolution.y;
    vec3 col = vec3(0);

    // body 1
    vec2 b1uv = (b1pos.xy - 0.5 * resolution.xy) / resolution.y;
    float r1 = b1r/resolution.y;

    // body 2
    vec2 b2uv = (b2pos.xy - 0.5 * resolution.xy) / resolution.y;
    float r2 = b2r/resolution.y;

    // circle SDF for both
    float d1 = sdCircle(uv-b1uv, r1);
    float d2 = sdCircle(uv-b2uv, r2);

    // unit vectors
    vec2 u1 = (b1uv-uv)/length(b1uv-uv);
    vec2 u2 = (b2uv-uv)/length(b2uv-uv);

    // calc force
    float F1 = G*b1m/pow(d1+r1, 2.0);
    float F2 = G*b2m/pow(d2+r2, 2.0);

    // calc force vector
    vec2 Fv1 = F1 * u1;
    vec2 Fv2 = F2 * u2;

    // calc net force;
    vec2 Fnv = Fv1 + Fv2;
    float Fn = length(Fnv);


    // glow behind circles
    col += vec3(0.9, 0.1, 0.1)*0.005/abs(length(uv-b1uv)-r1);
    col += vec3(0.1, 0.1, 0.9)*0.005/abs(length(uv-b2uv)-r2);

    float scale = log(Fn+1.0)/log(10.0);
    float change = fwidth(scale);

//    col += mod(scale*pow(10, 6), 1);
    col += min(0.7, change*pow(10, 9));

    // fill circle
    if (d1 <= 0) {
        col = vec3(1, 0, 0);
    } else if (d2 <= 0){
        col = vec3(0, 0, 1);
    }

    //    // outline circle
//    col += smoothstep(0, 0.1, -abs(d1));
//    col += smoothstep(0, 0.1, -abs(d2));


    fragColor = vec4(col, 1.0);
}
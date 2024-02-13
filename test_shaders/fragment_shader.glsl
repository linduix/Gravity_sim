#version 430

out vec4 fragColor;

uniform vec2 resolution;
uniform float time;
uniform vec2 mouse;

vec2 rotate2D(vec2 uv, float a) {
    float s = sin(a);
    float c = cos(a);
    return mat2(c, -s, s, c) * uv;
}

void main() {
    vec2 uv = (gl_FragCoord.xy - 0.5 * resolution.xy) / resolution.y;
    vec2 muv = (mouse.xy - 0.5 * resolution.xy) / resolution.y;
    vec3 col = vec3(0.0);


    float r = 0.17;
    for (float i=0.0; i < 60.0; i++) {
        float a = time*5/(i+1);
        float dx = 2 * r * cos(a) - r * cos(2 * a);
        float dy = 2 * r * sin(a) - r * sin(2 * a);

        col += 0.0006 / length(rotate2D(uv, 3.1415/2) - vec2(dx + 0.1, dy));
    }

    col *= cos(vec3(0.3, 0.8, 0.2) * length(muv)*6.28);
    col += 0.005/length(muv-uv);

    fragColor = vec4(col, 1.0);
}
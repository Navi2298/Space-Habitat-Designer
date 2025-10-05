#version 330 core
out vec4 FragColor;

in vec3 FragPos;
in vec3 Normal;

uniform vec3 objectColor;
uniform float alpha;
uniform vec3 lightPos;
uniform vec3 viewPos;

void main() {
    // Basic ambient + diffuse lighting
    float ambientStrength = 0.2;
    vec3 ambient = ambientStrength * vec3(1.0);

    vec3 norm = normalize(Normal);
    vec3 lightDir = normalize(lightPos - FragPos);
    float diff = max(dot(norm, lightDir), 0.0);
    vec3 diffuse = diff * vec3(1.0);
    
    vec3 result = (ambient + diffuse) * objectColor;
    FragColor = vec4(result, alpha);
}
